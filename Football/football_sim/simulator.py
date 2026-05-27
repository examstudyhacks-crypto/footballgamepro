"""Football simulation engine."""
from __future__ import annotations

import json
import math
import random
import uuid
from copy import deepcopy
from datetime import datetime
from typing import Dict, List, Tuple


FIRST_NAMES = [
    "Alex", "Ben", "Carlos", "Diego", "Ethan", "Felix", "Gabriel", "Hugo", "Ivan", "Jamal",
    "Kai", "Leo", "Mateo", "Nico", "Oscar", "Rafael", "Sam", "Theo", "Victor", "Yusuf",
]
LAST_NAMES = [
    "Adams", "Costa", "Silva", "Fernandes", "Martínez", "Kovač", "Wilson", "Garcia", "Mbaye", "Rossi",
    "Walker", "Mendes", "Nakamura", "Petrov", "Santos", "Diallo", "Bennett", "Khan", "Schmidt", "Romero",
]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def poisson(lam: float) -> int:
    """Small pure-Python Poisson sampler for football goals."""
    lam = clamp(lam, 0.05, 5.0)
    limit = math.exp(-lam)
    k = 0
    p = 1.0
    while p > limit:
        k += 1
        p *= random.random()
    return k - 1


def player_pool(team: dict) -> List[str]:
    random.seed(team["name"])
    names = [team.get("star_player") or f"{team['name']} Star"]
    while len(names) < 13:
        names.append(f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}")
    random.seed()
    return names


def pick_goal_scorer(team: dict) -> str:
    pool = player_pool(team)
    weights = [8, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1, 1, 1]
    return random.choices(pool, weights=weights, k=1)[0]


def pick_assister(team: dict, scorer: str) -> str:
    pool = [p for p in player_pool(team) if p != scorer]
    return random.choice(pool[:10])


def expected_goals(home: dict, away: dict, neutral: bool = False) -> Tuple[float, float]:
    home_adv = 0.18 if not neutral else 0.0
    home_quality = (home["attack"] * 0.50 + home["midfield"] * 0.30 - away["defence"] * 0.38 - away["midfield"] * 0.12)
    away_quality = (away["attack"] * 0.50 + away["midfield"] * 0.30 - home["defence"] * 0.38 - home["midfield"] * 0.12)
    home_xg = 1.28 + home_adv + (home_quality / 55) + random.gauss(0, 0.18)
    away_xg = 1.08 + (away_quality / 55) + random.gauss(0, 0.18)
    return clamp(home_xg, 0.15, 4.4), clamp(away_xg, 0.15, 4.1)


def simulate_match(home: dict, away: dict, knockout: bool = False, neutral: bool = False) -> dict:
    home_xg, away_xg = expected_goals(home, away, neutral)
    home_goals = poisson(home_xg)
    away_goals = poisson(away_xg)

    events = []
    scorer_counts: Dict[str, int] = {}
    assister_counts: Dict[str, int] = {}
    card_log = []
    injury_log = []

    goal_events = []
    for _ in range(home_goals):
        minute = random.randint(2, 90)
        scorer = pick_goal_scorer(home)
        assister = pick_assister(home, scorer) if random.random() < 0.76 else None
        goal_events.append((minute, home["name"], scorer, assister))
    for _ in range(away_goals):
        minute = random.randint(2, 90)
        scorer = pick_goal_scorer(away)
        assister = pick_assister(away, scorer) if random.random() < 0.76 else None
        goal_events.append((minute, away["name"], scorer, assister))

    for minute, team_name, scorer, assister in sorted(goal_events, key=lambda item: item[0]):
        if assister:
            text = f"⚽ {minute}' {team_name}: {scorer} (assist: {assister})"
            assister_counts[f"{assister} — {team_name}"] = assister_counts.get(f"{assister} — {team_name}", 0) + 1
        else:
            text = f"⚽ {minute}' {team_name}: {scorer}"
        events.append(text)
        scorer_counts[f"{scorer} — {team_name}"] = scorer_counts.get(f"{scorer} — {team_name}", 0) + 1

    for team in [home, away]:
        yellows = random.randint(0, 4)
        for _ in range(yellows):
            minute = random.randint(8, 90)
            player = random.choice(player_pool(team))
            card_log.append({"team": team["name"], "player": player, "minute": minute, "card": "Yellow"})
            if random.random() < 0.012:
                card_log.append({"team": team["name"], "player": player, "minute": min(90, minute + random.randint(5, 30)), "card": "Red"})
        if random.random() < 0.08:
            minute = random.randint(10, 88)
            player = random.choice(player_pool(team))
            severity = random.choice(["minor knock", "hamstring strain", "ankle injury", "shoulder injury"])
            injury_log.append({"team": team["name"], "player": player, "minute": minute, "injury": severity})

    for c in sorted(card_log, key=lambda x: x["minute"]):
        icon = "🟨" if c["card"] == "Yellow" else "🟥"
        events.append(f"{icon} {c['minute']}' {c['team']}: {c['player']} {c['card'].lower()} card")
    for i in sorted(injury_log, key=lambda x: x["minute"]):
        events.append(f"🚑 {i['minute']}' {i['team']}: {i['player']} — {i['injury']}")

    extra = None
    penalties = None
    winner = None
    if knockout:
        if home_goals > away_goals:
            winner = home["name"]
        elif away_goals > home_goals:
            winner = away["name"]
        else:
            # Extra time first, then penalties if needed.
            et_home = poisson(0.35 + (home["overall"] - away["overall"]) / 180)
            et_away = poisson(0.35 + (away["overall"] - home["overall"]) / 180)
            home_goals += et_home
            away_goals += et_away
            extra = {"home": et_home, "away": et_away}
            if et_home or et_away:
                events.append(f"⏱️ Extra time: {home['name']} {et_home}–{et_away} {away['name']}")
            if home_goals > away_goals:
                winner = home["name"]
            elif away_goals > home_goals:
                winner = away["name"]
            else:
                hp = random.randint(3, 5)
                ap = random.randint(3, 5)
                while hp == ap:
                    hp = random.randint(3, 7)
                    ap = random.randint(3, 7)
                penalties = {"home": hp, "away": ap}
                winner = home["name"] if hp > ap else away["name"]
                events.append(f"🥅 Penalties: {home['name']} {hp}–{ap} {away['name']} — {winner} advance")

    if not events:
        events.append("Tense tactical battle with no major goals — both sides cancelled each other out.")

    return {
        "id": str(uuid.uuid4()),
        "home": home["name"],
        "away": away["name"],
        "home_goals": home_goals,
        "away_goals": away_goals,
        "home_xg": round(home_xg, 2),
        "away_xg": round(away_xg, 2),
        "events": events,
        "cards": card_log,
        "injuries": injury_log,
        "scorers": scorer_counts,
        "assisters": assister_counts,
        "winner": winner,
        "extra_time": extra,
        "penalties": penalties,
        "played_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


def empty_standing(team: str) -> dict:
    return {"Team": team, "P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0}


def update_standings(standings: Dict[str, dict], result: dict) -> None:
    h, a = result["home"], result["away"]
    hg, ag = result["home_goals"], result["away_goals"]
    for team in [h, a]:
        standings.setdefault(team, empty_standing(team))
    standings[h]["P"] += 1
    standings[a]["P"] += 1
    standings[h]["GF"] += hg
    standings[h]["GA"] += ag
    standings[a]["GF"] += ag
    standings[a]["GA"] += hg
    if hg > ag:
        standings[h]["W"] += 1
        standings[a]["L"] += 1
        standings[h]["Pts"] += 3
    elif ag > hg:
        standings[a]["W"] += 1
        standings[h]["L"] += 1
        standings[a]["Pts"] += 3
    else:
        standings[h]["D"] += 1
        standings[a]["D"] += 1
        standings[h]["Pts"] += 1
        standings[a]["Pts"] += 1
    for team in [h, a]:
        standings[team]["GD"] = standings[team]["GF"] - standings[team]["GA"]


def sorted_table(standings: Dict[str, dict]) -> List[dict]:
    return sorted(standings.values(), key=lambda r: (r["Pts"], r["GD"], r["GF"], r["W"], r["Team"]), reverse=True)


def merge_counter(target: Dict[str, int], source: Dict[str, int]) -> None:
    for key, value in source.items():
        target[key] = target.get(key, 0) + value


def top_list(counter: Dict[str, int], limit: int = 10) -> List[dict]:
    rows = [{"Player": k, "Total": v} for k, v in counter.items()]
    return sorted(rows, key=lambda r: r["Total"], reverse=True)[:limit]


def dumps_state(state: dict) -> str:
    return json.dumps(state, ensure_ascii=False, indent=2)


def loads_state(text: str) -> dict:
    return json.loads(text)
