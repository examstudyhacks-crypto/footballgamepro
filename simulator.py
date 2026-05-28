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


def player_pool(team: dict) -> List[dict]:
    """Return a weighted player pool.

    National teams ship with real-player cores and ratings. Club/custom teams fall
    back to deterministic generated depth so every team can still produce scorers,
    assists, cards and injuries.
    """
    players = team.get("players") or []
    if players:
        return players

    random.seed(team["name"])
    generated = [{"name": team.get("star_player") or f"{team['name']} Star", "position": "ST", "rating": team.get("overall", 75) + 3}]
    while len(generated) < 13:
        generated.append({
            "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "position": random.choice(["ST", "LW", "RW", "AM", "CM", "DM", "CB", "FB", "GK"]),
            "rating": max(55, min(94, int(random.gauss(team.get("overall", 74), 4)))),
        })
    random.seed()
    return generated


def _attacking_weight(player: dict) -> float:
    pos = player.get("position", "CM")
    base = max(1, player.get("rating", 75) - 58)
    pos_bonus = {"ST": 2.8, "FW": 2.5, "LW": 2.2, "RW": 2.2, "AM": 1.9, "CM": 1.1, "DM": .65, "WB": .55, "FB": .45, "CB": .28, "GK": .05}
    return base * pos_bonus.get(pos, 1.0)


def _assist_weight(player: dict) -> float:
    pos = player.get("position", "CM")
    base = max(1, player.get("rating", 75) - 58)
    pos_bonus = {"AM": 2.6, "CM": 2.0, "RW": 2.1, "LW": 2.1, "DM": 1.2, "ST": 1.0, "FW": 1.1, "WB": 1.4, "FB": 1.3, "CB": .35, "GK": .02}
    return base * pos_bonus.get(pos, 1.0)


def pick_goal_scorer(team: dict) -> str:
    pool = player_pool(team)
    weights = [_attacking_weight(p) for p in pool]
    return random.choices(pool, weights=weights, k=1)[0]["name"]


def pick_assister(team: dict, scorer: str) -> str:
    pool = [p for p in player_pool(team) if p["name"] != scorer]
    if not pool:
        return scorer
    weights = [_assist_weight(p) for p in pool]
    return random.choices(pool, weights=weights, k=1)[0]["name"]


def pick_card_or_injury_player(team: dict) -> str:
    pool = player_pool(team)
    weights = []
    for player in pool:
        pos = player.get("position", "CM")
        rating = player.get("rating", 75)
        contact_bonus = {"CB": 2.2, "DM": 2.0, "FB": 1.7, "WB": 1.5, "CM": 1.25, "ST": 1.0, "FW": 1.0, "LW": .9, "RW": .9, "AM": .9, "GK": .25}.get(pos, 1.0)
        weights.append(max(1, rating - 60) * contact_bonus)
    return random.choices(pool, weights=weights, k=1)[0]["name"]


def team_power(team: dict) -> float:
    """Weighted team strength used by the winner model.

    Ratings matter strongly, but the match engine still leaves room for
    pressure swings, red-hot finishing and late cup upsets.
    """
    players = player_pool(team)
    star = max((p.get("rating", team.get("overall", 75)) for p in players), default=team.get("overall", 75))
    depth = sum(p.get("rating", 75) for p in players[:8]) / max(1, min(8, len(players)))
    return (
        team.get("attack", 75) * 0.34
        + team.get("midfield", 75) * 0.26
        + team.get("defence", 75) * 0.24
        + team.get("overall", 75) * 0.10
        + star * 0.04
        + depth * 0.02
    )


def expected_goals(home: dict, away: dict, neutral: bool = False) -> Tuple[float, float]:
    home_adv = 0.22 if not neutral else 0.0
    hp = team_power(home)
    ap = team_power(away)
    home_quality = (home["attack"] * 0.54 + home["midfield"] * 0.28 - away["defence"] * 0.40 - away["midfield"] * 0.12)
    away_quality = (away["attack"] * 0.54 + away["midfield"] * 0.28 - home["defence"] * 0.40 - home["midfield"] * 0.12)
    strength_edge = (hp - ap) / 46
    # Keep randomness, but not so much that ratings feel meaningless.
    home_xg = 1.22 + home_adv + (home_quality / 58) + strength_edge + random.gauss(0, 0.14)
    away_xg = 1.05 + (away_quality / 58) - strength_edge + random.gauss(0, 0.14)
    return clamp(home_xg, 0.12, 4.7), clamp(away_xg, 0.12, 4.4)


def _yellow_card_count() -> int:
    """Low-noise card model: realistic enough, but not cards everywhere."""
    return random.choices([0, 1, 2, 3], weights=[42, 38, 17, 3], k=1)[0]


def _team_match_numbers(team: dict, opponent: dict, xg: float, goals: int, possession: int) -> dict:
    """Create believable football box-score stats from team quality and xG."""
    quality_edge = (team.get("attack", 75) + team.get("midfield", 75) - opponent.get("defence", 75) - opponent.get("midfield", 75)) / 25
    shots = int(round(clamp((xg * 4.3) + random.gauss(4.9 + quality_edge, 1.7), 2, 24)))
    shots_on_target = int(round(clamp(goals + random.gauss(max(1.2, xg * 1.6), 1.05), goals, min(shots, 13))))
    big_chances = int(clamp(round(xg + goals + random.choice([-1, 0, 0, 1])), 0, 8))
    corners = int(clamp(round((shots * 0.28) + random.gauss(1.5, 1.2)), 0, 13))
    fouls = int(clamp(round(random.gauss(9.4, 2.8) + max(0, opponent.get("midfield", 75) - team.get("midfield", 75)) / 18), 4, 22))
    pass_accuracy = int(clamp(round(73 + (team.get("midfield", 75) - 70) * 0.42 + (possession - 50) * 0.18 + random.gauss(0, 2.5)), 62, 93))
    keeper_saves = 0  # Filled after both sides are known.
    return {
        "possession": possession,
        "shots": shots,
        "shots_on_target": shots_on_target,
        "big_chances": big_chances,
        "corners": corners,
        "fouls": fouls,
        "pass_accuracy": pass_accuracy,
        "keeper_saves": keeper_saves,
    }


def _build_match_stats(home: dict, away: dict, home_xg: float, away_xg: float, home_goals: int, away_goals: int) -> dict:
    midfield_edge = home.get("midfield", 75) - away.get("midfield", 75)
    overall_edge = home.get("overall", 75) - away.get("overall", 75)
    home_possession = int(clamp(round(50 + midfield_edge * 0.38 + overall_edge * 0.13 + random.gauss(0, 3.8)), 34, 66))
    away_possession = 100 - home_possession
    home_stats = _team_match_numbers(home, away, home_xg, home_goals, home_possession)
    away_stats = _team_match_numbers(away, home, away_xg, away_goals, away_possession)
    home_stats["keeper_saves"] = max(0, away_stats["shots_on_target"] - away_goals)
    away_stats["keeper_saves"] = max(0, home_stats["shots_on_target"] - home_goals)
    return {home["name"]: home_stats, away["name"]: away_stats}


def _pick_outfield_player(team: dict) -> str:
    pool = [p for p in player_pool(team) if p.get("position") != "GK"] or player_pool(team)
    weights = [max(1, p.get("rating", 75) - 58) for p in pool]
    return random.choices(pool, weights=weights, k=1)[0]["name"]


def _pick_goalkeeper(team: dict) -> str:
    keepers = [p for p in player_pool(team) if p.get("position") == "GK"]
    if keepers:
        return max(keepers, key=lambda p: p.get("rating", 0))["name"]
    return f"{team.get('name', 'Team')} goalkeeper"


def _add_open_play_details(event_objects: list, team: dict, opponent: dict, team_stats: dict, opponent_stats: dict, team_goals: int, opponent_goals: int) -> None:
    """Add useful match detail without flooding the feed with card events."""
    team_name = team["name"]
    opponent_name = opponent["name"]
    attacking_player = _pick_outfield_player(team)
    goalkeeper = _pick_goalkeeper(opponent)

    if team_stats["shots_on_target"] > team_goals:
        minute = random.randint(15, 82)
        event_objects.append({
            "minute": minute,
            "text": f"🧤 {minute}' {opponent_name}: {goalkeeper} makes an important save from {attacking_player}",
            "type": "save",
        })
    if team_stats["big_chances"] >= 2 and random.random() < 0.55:
        minute = random.randint(20, 86)
        event_objects.append({
            "minute": minute,
            "text": f"🔥 {minute}' {team_name}: big chance for {attacking_player}, but the finish is just off target",
            "type": "chance",
        })
    if team_stats["corners"] >= 5 and random.random() < 0.45:
        defender = pick_card_or_injury_player(opponent)
        minute = random.randint(25, 88)
        event_objects.append({
            "minute": minute,
            "text": f"🚩 {minute}' {team_name}: spell of corner pressure, {defender} clears under pressure",
            "type": "pressure",
        })
    if team_stats["possession"] >= 57 and random.random() < 0.55:
        minute = random.randint(12, 72)
        event_objects.append({
            "minute": minute,
            "text": f"🎛️ {minute}' {team_name}: controlling midfield with {team_stats['possession']}% possession",
            "type": "control",
        })
    if abs(team_goals - opponent_goals) <= 1 and random.random() < 0.40:
        minute = random.randint(70, 90)
        event_objects.append({
            "minute": minute,
            "text": f"⏳ {minute}' {team_name}: late pressure as the game opens up",
            "type": "late",
        })


def minute_label(minute: int) -> str:
    if 91 <= minute <= 99:
        return f"90+{minute - 90}"
    if minute == 121:
        return "Pens"
    return str(minute)


def add_goal_event(goal_events: list, team: dict, minute: int, tag: str = "") -> None:
    scorer = pick_goal_scorer(team)
    assister = pick_assister(team, scorer) if random.random() < 0.76 else None
    goal_events.append((minute, team["name"], scorer, assister, tag))


def simulate_match(home: dict, away: dict, knockout: bool = False, neutral: bool = False) -> dict:
    home_xg, away_xg = expected_goals(home, away, neutral)
    home_goals = poisson(home_xg)
    away_goals = poisson(away_xg)

    scorer_counts: Dict[str, int] = {}
    assister_counts: Dict[str, int] = {}
    card_log = []
    injury_log = []
    event_objects = []

    goal_events = []
    for _ in range(home_goals):
        add_goal_event(goal_events, home, random.randint(2, 89))
    for _ in range(away_goals):
        add_goal_event(goal_events, away, random.randint(2, 89))

    # Late drama model. Strong teams are still favoured, but the last 15 minutes
    # can produce realistic pressure swings and rare underdog/cup upsets.
    hp = team_power(home)
    ap = team_power(away)
    gap = abs(hp - ap)
    favourite = home if hp >= ap else away
    underdog = away if favourite is home else home
    fav_goals = home_goals if favourite is home else away_goals
    dog_goals = away_goals if favourite is home else home_goals
    if dog_goals <= fav_goals and random.random() < clamp(0.19 - (gap * 0.006), 0.045, 0.18):
        minute = random.randint(78, 95)
        add_goal_event(goal_events, underdog, minute, "late_underdog")
        if underdog is home:
            home_goals += 1
        else:
            away_goals += 1
    if dog_goals == fav_goals and random.random() < clamp(0.09 - (gap * 0.004), 0.025, 0.085):
        minute = random.randint(87, 95)
        add_goal_event(goal_events, underdog, minute, "stoppage_upset")
        if underdog is home:
            home_goals += 1
        else:
            away_goals += 1
    elif abs(home_goals - away_goals) == 1 and random.random() < 0.09:
        # The trailing team throws everything forward late on.
        chaser = home if home_goals < away_goals else away
        minute = random.randint(84, 95)
        add_goal_event(goal_events, chaser, minute, "late_pressure")
        if chaser is home:
            home_goals += 1
        else:
            away_goals += 1

    for minute, team_name, scorer, assister, tag in sorted(goal_events, key=lambda item: item[0]):
        label = minute_label(minute)
        prefix = "⚽"
        if tag == "late_underdog":
            prefix = "⚽🔥"
        elif tag == "stoppage_upset":
            prefix = "⚽💥"
        elif tag == "late_pressure":
            prefix = "⚽⏳"
        if assister:
            text = f"{prefix} {label}' {team_name}: {scorer} (assist: {assister})"
            assister_counts[f"{assister} — {team_name}"] = assister_counts.get(f"{assister} — {team_name}", 0) + 1
        else:
            text = f"{prefix} {label}' {team_name}: {scorer}"
        event_objects.append({"minute": minute, "text": text, "type": "goal", "team": team_name, "player": scorer, "assist": assister, "tag": tag})
        scorer_counts[f"{scorer} — {team_name}"] = scorer_counts.get(f"{scorer} — {team_name}", 0) + 1

    match_stats = _build_match_stats(home, away, home_xg, away_xg, home_goals, away_goals)
    _add_open_play_details(event_objects, home, away, match_stats[home["name"]], match_stats[away["name"]], home_goals, away_goals)
    _add_open_play_details(event_objects, away, home, match_stats[away["name"]], match_stats[home["name"]], away_goals, home_goals)

    for team in [home, away]:
        yellows = _yellow_card_count()
        for _ in range(yellows):
            minute = random.randint(12, 90)
            player = pick_card_or_injury_player(team)
            card_log.append({"team": team["name"], "player": player, "minute": minute, "card": "Yellow"})
            # Reds are deliberately rare so matches are not dominated by discipline.
            if random.random() < 0.004:
                red_minute = min(90, minute + random.randint(6, 28))
                card_log.append({"team": team["name"], "player": player, "minute": red_minute, "card": "Red"})
        if random.random() < 0.07:
            minute = random.randint(18, 88)
            player = pick_card_or_injury_player(team)
            severity = random.choice(["minor knock", "hamstring strain", "ankle injury", "shoulder injury"])
            injury_log.append({"team": team["name"], "player": player, "minute": minute, "injury": severity})

    for c in card_log:
        icon = "🟨" if c["card"] == "Yellow" else "🟥"
        event_objects.append({
            "minute": c["minute"],
            "text": f"{icon} {c['minute']}' {c['team']}: {c['player']} {c['card'].lower()} card",
            "type": "card",
        })
    for i in injury_log:
        event_objects.append({
            "minute": i["minute"],
            "text": f"🚑 {i['minute']}' {i['team']}: {i['player']} — {i['injury']}",
            "type": "injury",
        })

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
                event_objects.append({
                    "minute": 105,
                    "text": f"⏱️ Extra time: {home['name']} {et_home}–{et_away} {away['name']}",
                    "type": "extra_time",
                })
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
                event_objects.append({
                    "minute": 121,
                    "text": f"🥅 Penalties: {home['name']} {hp}–{ap} {away['name']} — {winner} advance",
                    "type": "penalties",
                })

    # Keep box-score stats consistent after extra time goals.
    for team_name, goals in [(home["name"], home_goals), (away["name"], away_goals)]:
        team_stats = match_stats[team_name]
        team_stats["shots_on_target"] = max(team_stats["shots_on_target"], goals)
        team_stats["shots"] = max(team_stats["shots"], team_stats["shots_on_target"])

    timeline = sorted(event_objects, key=lambda x: (x["minute"], x["text"]))
    events = [item["text"] for item in timeline]
    if not events:
        events.append("Tense tactical battle with no major goals — both sides cancelled each other out.")
        timeline.append({"minute": 90, "text": events[0], "type": "full_time"})

    return {
        "id": str(uuid.uuid4()),
        "home": home["name"],
        "away": away["name"],
        "home_goals": home_goals,
        "away_goals": away_goals,
        "home_xg": round(home_xg, 2),
        "away_xg": round(away_xg, 2),
        "match_stats": match_stats,
        "events": events,
        "timeline": timeline,
        "home_power": round(team_power(home), 1),
        "away_power": round(team_power(away), 1),
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
