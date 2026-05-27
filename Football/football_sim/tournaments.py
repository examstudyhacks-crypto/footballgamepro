"""Tournament construction and progression helpers."""
from __future__ import annotations

import random
import uuid
from copy import deepcopy
from typing import Dict, List, Tuple

from .data import CONTINENTAL, team_lookup
from .simulator import empty_standing, merge_counter, simulate_match, sorted_table, update_standings


def make_match(home: str, away: str) -> dict:
    return {"id": str(uuid.uuid4()), "home": home, "away": away, "played": False, "result": None}


def round_robin_schedule(team_names: List[str], double_round: bool = False) -> List[List[dict]]:
    teams = team_names[:]
    if len(teams) % 2:
        teams.append("BYE")
    n = len(teams)
    rounds = []
    rotation = teams[:]
    for round_idx in range(n - 1):
        matches = []
        for i in range(n // 2):
            home = rotation[i]
            away = rotation[n - 1 - i]
            if home == "BYE" or away == "BYE":
                continue
            if round_idx % 2:
                home, away = away, home
            matches.append(make_match(home, away))
        rounds.append(matches)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]
    if double_round:
        reverse = [[make_match(m["away"], m["home"]) for m in md] for md in rounds]
        rounds += reverse
    return rounds


def swiss_like_schedule(team_names: List[str], matchdays: int = 8) -> List[List[dict]]:
    """Create unique pairings per matchday.

    This is game-friendly rather than a complete UEFA draw engine. It keeps the
    user experience faithful: one league table, 36 teams, 8/6 matchdays, then
    knockout play-offs and round of 16.
    """
    base = team_names[:]
    random.shuffle(base)
    all_rounds = round_robin_schedule(base, double_round=False)
    return all_rounds[:matchdays]


def knockout_pairs(teams: List[str], seeded: bool = True) -> List[dict]:
    names = teams[:]
    if seeded:
        left = names[: len(names) // 2]
        right = names[len(names) // 2 :][::-1]
        pairs = zip(left, right)
    else:
        random.shuffle(names)
        pairs = zip(names[::2], names[1::2])
    return [make_match(a, b) for a, b in pairs]


def init_state(name: str, teams: List[dict], schedule: List[List[dict]], mode: str, config: dict | None = None) -> dict:
    team_names = [t["name"] for t in teams]
    return {
        "name": name,
        "mode": mode,
        "config": config or {},
        "teams": teams,
        "team_names": team_names,
        "team_lookup": {t["name"]: t for t in teams},
        "stage": "league" if schedule else "knockout",
        "matchday_index": 0,
        "schedule": schedule,
        "knockout_rounds": [],
        "standings": {name: empty_standing(name) for name in team_names},
        "top_scorers": {},
        "top_assisters": {},
        "history": [],
        "champion": None,
    }


def create_uefa_tournament(competition: str) -> dict:
    lookup = team_lookup()
    cfg = CONTINENTAL[competition]
    teams = [deepcopy(lookup[name]) for name in cfg["teams"]]
    schedule = swiss_like_schedule([t["name"] for t in teams], cfg["league_rounds"])
    return init_state(competition, teams, schedule, "uefa", {"league_rounds": cfg["league_rounds"], "source": "UEFA 2025/26 seed"})


def create_league(name: str, teams: List[dict], double_round: bool = False) -> dict:
    schedule = round_robin_schedule([t["name"] for t in teams], double_round=double_round)
    return init_state(name, teams, schedule, "league", {"double_round": double_round})


def create_knockout(name: str, teams: List[dict]) -> dict:
    state = init_state(name, teams, [], "knockout", {})
    state["stage"] = "knockout"
    state["knockout_rounds"] = [{"name": round_name(len(teams)), "matches": knockout_pairs([t["name"] for t in teams], seeded=False), "complete": False}]
    return state


def create_cup(name: str, teams: List[dict], groups: int = 4) -> dict:
    random.shuffle(teams)
    group_map: Dict[str, List[dict]] = {chr(65 + i): [] for i in range(groups)}
    for idx, team in enumerate(teams):
        group_map[chr(65 + (idx % groups))].append(team)
    schedule = []
    group_tables = {}
    for group_name, group_teams in group_map.items():
        group_tables[group_name] = {t["name"]: empty_standing(t["name"]) for t in group_teams}
        for md_idx, md in enumerate(round_robin_schedule([t["name"] for t in group_teams], double_round=False)):
            while len(schedule) <= md_idx:
                schedule.append([])
            for match in md:
                match["group"] = group_name
                schedule[md_idx].append(match)
    state = init_state(name, teams, schedule, "cup", {"groups": groups})
    state["group_tables"] = group_tables
    return state


def round_name(team_count: int) -> str:
    return {
        32: "Round of 32",
        24: "Knockout Play-offs",
        16: "Round of 16",
        8: "Quarter-finals",
        4: "Semi-finals",
        2: "Final",
    }.get(team_count, f"Last {team_count}")


def simulate_matchday(state: dict, team_db: Dict[str, dict]) -> Tuple[dict, List[dict]]:
    if state["stage"] != "league" or state["matchday_index"] >= len(state["schedule"]):
        return state, []
    matchday = state["schedule"][state["matchday_index"]]
    results = []
    for match in matchday:
        if match["played"]:
            continue
        result = simulate_match(team_db[match["home"]], team_db[match["away"]], knockout=False)
        match["played"] = True
        match["result"] = result
        if state["mode"] == "cup" and "group" in match:
            update_standings(state["group_tables"][match["group"]], result)
        else:
            update_standings(state["standings"], result)
        merge_counter(state["top_scorers"], result["scorers"])
        merge_counter(state["top_assisters"], result["assisters"])
        state["history"].append(result)
        results.append(result)
    state["matchday_index"] += 1
    if state["matchday_index"] >= len(state["schedule"]):
        prepare_knockout_after_league(state)
    return state, results


def prepare_knockout_after_league(state: dict) -> None:
    if state["mode"] == "league":
        state["stage"] = "complete"
        table = sorted_table(state["standings"])
        state["champion"] = table[0]["Team"] if table else None
        return

    if state["mode"] == "cup":
        qualifiers = []
        for group_name, table in state.get("group_tables", {}).items():
            qualifiers.extend([row["Team"] for row in sorted_table(table)[:2]])
        state["stage"] = "knockout"
        state["knockout_rounds"].append({"name": round_name(len(qualifiers)), "matches": knockout_pairs(qualifiers, seeded=True), "complete": False})
        return

    if state["mode"] == "uefa":
        table = sorted_table(state["standings"])
        top8 = [r["Team"] for r in table[:8]]
        playoff = [r["Team"] for r in table[8:24]]
        state["stage"] = "knockout"
        state["config"]["top8_waiting"] = top8
        state["knockout_rounds"].append({"name": "Knockout Play-offs", "matches": knockout_pairs(playoff, seeded=True), "complete": False})


def simulate_knockout_round(state: dict, team_db: Dict[str, dict]) -> Tuple[dict, List[dict]]:
    if state["stage"] != "knockout" or not state["knockout_rounds"]:
        return state, []
    current = state["knockout_rounds"][-1]
    if current.get("complete"):
        return state, []
    results = []
    winners = []
    for match in current["matches"]:
        if match["played"]:
            continue
        result = simulate_match(team_db[match["home"]], team_db[match["away"]], knockout=True, neutral=(current["name"] == "Final"))
        match["played"] = True
        match["result"] = result
        merge_counter(state["top_scorers"], result["scorers"])
        merge_counter(state["top_assisters"], result["assisters"])
        state["history"].append(result)
        results.append(result)
        winners.append(result["winner"])
    current["complete"] = True

    if len(winners) == 1:
        state["stage"] = "complete"
        state["champion"] = winners[0]
        return state, results

    if state["mode"] == "uefa" and current["name"] == "Knockout Play-offs":
        next_teams = state["config"].get("top8_waiting", []) + winners
        # Top 8 are treated as seeded; playoff winners are drawn against them.
        next_round = {"name": "Round of 16", "matches": knockout_pairs(next_teams, seeded=True), "complete": False}
    else:
        next_round = {"name": round_name(len(winners)), "matches": knockout_pairs(winners, seeded=True), "complete": False}
    state["knockout_rounds"].append(next_round)
    return state, results


def upcoming_matches(state: dict) -> List[dict]:
    if state["stage"] == "league" and state["matchday_index"] < len(state["schedule"]):
        return state["schedule"][state["matchday_index"]]
    if state["stage"] == "knockout" and state["knockout_rounds"]:
        return [m for m in state["knockout_rounds"][-1]["matches"] if not m["played"]]
    return []
