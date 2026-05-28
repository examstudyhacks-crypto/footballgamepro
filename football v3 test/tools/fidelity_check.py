"""Built-in full fidelity check for Football Simulator Pro.

Run from the repo root with:
    python tools/fidelity_check.py

It uses only Python standard library + the local app modules, so it works even
on the no-requirements Streamlit Cloud build.
"""
from __future__ import annotations

import ast
import random
import sys
from copy import deepcopy
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from football_sim.data import CONTINENTAL, DOMESTIC, INTERNATIONAL, TEAMS  # noqa: E402
from football_sim.simulator import dumps_state, loads_state, simulate_match  # noqa: E402
from football_sim.tournaments import (  # noqa: E402
    create_cup,
    create_international_tournament,
    create_premier_league,
    create_fa_cup,
    create_knockout,
    create_league,
    create_uefa_tournament,
    simulate_knockout_round,
    simulate_matchday,
    upcoming_matches,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_to_end(game: dict, team_db: dict[str, dict], max_steps: int = 350) -> dict:
    steps = 0
    while game["stage"] != "complete" and steps < max_steps:
        if game["stage"] == "league":
            before = len(game.get("history", []))
            game, results = simulate_matchday(game, team_db)
            require(results or game["stage"] == "complete", f"No league results produced in {game['name']}")
            require(len(game.get("history", [])) >= before, f"History regressed in {game['name']}")
        elif game["stage"] == "knockout":
            game, results = simulate_knockout_round(game, team_db)
            require(results, f"No knockout results produced in {game['name']}")
            require(all(r.get("winner") for r in results), f"Knockout result missing winner in {game['name']}")
        else:
            raise AssertionError(f"Unknown stage {game['stage']} in {game['name']}")
        steps += 1
    require(game["stage"] == "complete", f"{game['name']} did not complete within {max_steps} steps")
    require(game.get("champion"), f"{game['name']} completed without a champion")
    require(game["champion"] in {t["name"] for t in game["teams"]}, f"Champion not in tournament teams for {game['name']}")
    require(game.get("history"), f"{game['name']} has no match history")
    reloaded = loads_state(dumps_state(game))
    require(reloaded["champion"] == game["champion"], f"Save/load champion mismatch for {game['name']}")
    return game


def check_data_integrity() -> None:
    names = [t["name"] for t in TEAMS]
    require(len(names) == len(set(names)), "Duplicate team names found")
    require(len(TEAMS) >= 180, "Team database is smaller than expected")
    for t in TEAMS:
        for key in ["attack", "midfield", "defence", "overall"]:
            require(isinstance(t.get(key), int), f"{t.get('name')} missing integer {key}")
            require(40 <= t[key] <= 99, f"{t['name']} {key} out of range: {t[key]}")
        require(t.get("star_player"), f"{t['name']} missing star player")
    team_names = set(names)
    for comp, cfg in CONTINENTAL.items():
        missing = [name for name in cfg["teams"] if name not in team_names]
        require(not missing, f"{comp} missing teams: {missing[:5]}")
    for comp, cfg in INTERNATIONAL.items():
        missing = [name for name in cfg["teams"] if name not in team_names]
        require(not missing, f"{comp} missing teams: {missing[:5]}")
    for comp, cfg in DOMESTIC.items():
        missing = [name for name in cfg["teams"] if name not in team_names]
        require(not missing, f"{comp} missing teams: {missing[:5]}")
    for t in TEAMS:
        for key in ["flag", "abbr", "crest_primary", "crest_secondary"]:
            require(t.get(key), f"{t['name']} missing branding key {key}")


def check_match_engine(team_db: dict[str, dict]) -> None:
    result = simulate_match(team_db["England"], team_db["France"], knockout=True, neutral=True)
    require(result["home"] == "England" and result["away"] == "France", "Quick match team names wrong")
    require(isinstance(result["home_goals"], int) and isinstance(result["away_goals"], int), "Goals are not integers")
    require(result.get("winner") in {"England", "France"}, "Knockout quick match missing valid winner")
    require(result.get("events"), "Quick match has no event log")
    require("home_xg" in result and "away_xg" in result, "Quick match missing xG")
    require(result.get("match_stats"), "Quick match missing detailed match stats")
    require(result.get("timeline"), "Quick match missing structured live timeline")
    require("home_power" in result and "away_power" in result, "Quick match missing power ratings")
    for team_name in ["England", "France"]:
        stats = result["match_stats"].get(team_name, {})
        for key in ["possession", "shots", "shots_on_target", "big_chances", "corners", "fouls", "pass_accuracy", "keeper_saves"]:
            require(key in stats, f"{team_name} missing match stat: {key}")

    # Discipline should be present sometimes, but no longer dominate every timeline.
    sample = [simulate_match(team_db["England"], team_db["France"], neutral=True) for _ in range(120)]
    avg_cards = sum(len(r.get("cards", [])) for r in sample) / len(sample)
    require(avg_cards < 2.6, f"Average cards too high after lower-noise card model: {avg_cards:.2f}")


def check_tournaments(team_db: dict[str, dict]) -> None:
    for comp in INTERNATIONAL:
        game = create_international_tournament(comp)
        require(len(game["teams"]) == len(INTERNATIONAL[comp]["teams"]), f"{comp} team count mismatch")
        require(upcoming_matches(game), f"{comp} has no opening fixtures")
        completed = run_to_end(game, team_db)
        require(completed.get("knockout_rounds"), f"{comp} never created knockouts")

    for comp in CONTINENTAL:
        game = create_uefa_tournament(comp)
        require(len(game["teams"]) == 36, f"{comp} should start with 36 teams")
        require(upcoming_matches(game), f"{comp} has no opening fixtures")
        completed = run_to_end(game, team_db)
        require(completed.get("knockout_rounds"), f"{comp} never created knockouts")

    domestic_makers: list[Callable[[], dict]] = [create_premier_league, create_fa_cup]
    for maker in domestic_makers:
        game = maker()
        require(upcoming_matches(game), f"{game['name']} has no opening fixtures")
        completed = run_to_end(game, team_db, max_steps=420)
        require(completed.get("champion"), f"{game['name']} missing champion")

    custom_names = [
        "Arsenal",
        "Real Madrid",
        "Barcelona",
        "Bayern Munich",
        "Liverpool",
        "Paris Saint-Germain",
        "Inter Milan",
        "Man City",
    ]
    custom_teams = [deepcopy(team_db[name]) for name in custom_names]
    makers: list[Callable[[], dict]] = [
        lambda: create_league("Fidelity Custom League", deepcopy(custom_teams), double_round=False),
        lambda: create_knockout("Fidelity Custom Knockout", deepcopy(custom_teams)),
        lambda: create_cup("Fidelity Custom Cup", deepcopy(custom_teams), groups=2),
    ]
    for maker in makers:
        game = maker()
        require(upcoming_matches(game), f"{game['name']} has no opening fixtures")
        run_to_end(game, team_db)


def check_app_html_source() -> None:
    source = (ROOT / "app.py").read_text(encoding="utf-8")
    require("def render_html" in source, "render_html helper missing")
    require("dedent(markup).strip()" in source, "HTML dedent/strip safeguard missing")
    require('" ".join(line.strip()' in source, "HTML single-line mobile render safeguard missing")
    require("<div class='fixture-grid'>" in source, "Fixture card renderer missing")
    require("next-action-card" in source, "Mobile next-action guidance card missing")
    require("results_continue" in source, "Results-tab continue button missing")
    require("teams_dataframe(" not in source, "Old pandas teams_dataframe call still present")
    require("DeltaGenerator" not in source, "App source should not intentionally render DeltaGenerator objects")
    require("--text-soft: #e2e8f0" in source, "Bright text CSS variables missing")
    require("mini-stat-grid" in source, "Mobile match stat cards missing")
    require("match_stats_rows" in source, "Detailed match stats table renderer missing")
    require("def live_broadcast" in source, "Live broadcast renderer missing")
    require("mobile-action-bar" in source, "Mobile bottom action menu missing")
    require("Watch Live" in source, "Watch Live button missing")
    require("create_premier_league" in source and "create_fa_cup" in source, "Domestic mode hooks missing")
    require('div[data-baseweb="select"]' in source, "Dropdown contrast CSS missing")

    tree = ast.parse(source)
    for node in ast.walk(tree):
        # Streamlit magic can render the result of expression-level ternaries such as
        # st.dataframe(...) if rows else st.caption(...), leaking DeltaGenerator reprs.
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.IfExp):
            raise AssertionError(f"Expression ternary can leak Streamlit DeltaGenerator at line {node.lineno}")


def main() -> None:
    random.seed(20260527)
    team_db = {t["name"]: deepcopy(t) for t in TEAMS}
    check_data_integrity()
    check_match_engine(team_db)
    check_tournaments(team_db)
    check_app_html_source()
    print("FULL FIDELITY CHECK PASSED")
    print(f"Teams checked: {len(TEAMS)}")
    print(f"International modes checked: {', '.join(INTERNATIONAL.keys())}")
    print(f"UEFA modes checked: {', '.join(CONTINENTAL.keys())}")
    print(f"Domestic modes checked: {', '.join(DOMESTIC.keys())}")
    print("Quick match, Premier League, FA Cup, live timeline, mobile contrast, bottom menu, save/load and HTML source checks passed.")


if __name__ == "__main__":
    main()
