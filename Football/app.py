from __future__ import annotations

import json
from copy import deepcopy
from typing import List

import pandas as pd
import streamlit as st

from football_sim.data import CONTINENTAL, TEAMS
from football_sim.simulator import dumps_state, loads_state, sorted_table, top_list, simulate_match
from football_sim.tournaments import (
    create_cup,
    create_knockout,
    create_league,
    create_uefa_tournament,
    simulate_knockout_round,
    simulate_matchday,
    upcoming_matches,
)

st.set_page_config(
    page_title="Football Simulator Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
:root {
    --bg-card: rgba(15, 23, 42, 0.86);
    --border: rgba(148, 163, 184, 0.25);
    --text-soft: #cbd5e1;
    --accent: #22c55e;
    --accent-2: #38bdf8;
}
.stApp {
    background: radial-gradient(circle at top left, rgba(34,197,94,.22), transparent 28%),
                radial-gradient(circle at top right, rgba(56,189,248,.2), transparent 30%),
                linear-gradient(135deg, #020617 0%, #08111f 48%, #0f172a 100%);
    color: #f8fafc;
}
.block-container { padding-top: 1.8rem; padding-bottom: 3rem; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(2,6,23,.96), rgba(15,23,42,.94));
    border-right: 1px solid rgba(148,163,184,.18);
}
.hero {
    padding: 2rem;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(34,197,94,.18), rgba(56,189,248,.12)), rgba(15,23,42,.72);
    border: 1px solid rgba(148, 163, 184, .25);
    box-shadow: 0 22px 70px rgba(0,0,0,.32);
    margin-bottom: 1.2rem;
}
.hero h1 { font-size: 3rem; line-height: 1; margin: 0 0 .7rem 0; letter-spacing: -.05em; }
.hero p { color: var(--text-soft); font-size: 1.07rem; max-width: 980px; }
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 1.05rem 1.15rem;
    box-shadow: 0 12px 42px rgba(0,0,0,.26);
    margin-bottom: 1rem;
}
.mode-card {
    min-height: 158px;
    background: linear-gradient(145deg, rgba(15,23,42,.92), rgba(30,41,59,.68));
    border: 1px solid rgba(148,163,184,.24);
    border-radius: 22px;
    padding: 1.2rem;
}
.mode-card h3 { margin-top: 0; }
.scoreline {
    font-size: 1.38rem;
    font-weight: 800;
    letter-spacing: -.02em;
    color: #f8fafc;
}
.pill {
    display: inline-block;
    padding: .22rem .6rem;
    border-radius: 999px;
    background: rgba(34,197,94,.14);
    color: #bbf7d0;
    border: 1px solid rgba(34,197,94,.24);
    font-size: .82rem;
    margin: .15rem .18rem .15rem 0;
}
.danger-pill { background: rgba(239,68,68,.14); color: #fecaca; border-color: rgba(239,68,68,.25); }
.info-pill { background: rgba(56,189,248,.14); color: #bae6fd; border-color: rgba(56,189,248,.25); }
.stButton>button {
    border-radius: 14px;
    border: 1px solid rgba(148,163,184,.22);
    font-weight: 700;
    min-height: 42px;
}
.stButton>button[kind="primary"] {
    background: linear-gradient(135deg, #16a34a, #0ea5e9);
    border: 0;
}
[data-testid="stMetric"] {
    background: rgba(15,23,42,.74);
    border: 1px solid rgba(148,163,184,.2);
    border-radius: 18px;
    padding: .85rem;
}
hr { border-color: rgba(148,163,184,.16); }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def init() -> None:
    if "team_db" not in st.session_state:
        st.session_state.team_db = {team["name"]: deepcopy(team) for team in TEAMS}
    if "game" not in st.session_state:
        st.session_state.game = None
    if "last_results" not in st.session_state:
        st.session_state.last_results = []
    if "quick_match_result" not in st.session_state:
        st.session_state.quick_match_result = None


def card(title: str, body: str, pill: str | None = None) -> None:
    pill_html = f"<span class='pill'>{pill}</span>" if pill else ""
    st.markdown(f"<div class='card'><h3>{title}</h3>{pill_html}<p>{body}</p></div>", unsafe_allow_html=True)


def hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>⚽ Football Simulator Pro</h1>
            <p>
            Build custom teams, run real 2025/26 European competitions, create leagues or cups,
            and simulate football one matchday or knockout round at a time. Every match generates
            scorelines, xG, scorers, assists, cards, injuries, tables, brackets and save files.
            </p>
            <span class="pill">Text-based football universe</span>
            <span class="pill info-pill">Streamlit-ready</span>
            <span class="pill">No paid API required</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_teams_by_names(names: List[str]) -> List[dict]:
    return [deepcopy(st.session_state.team_db[n]) for n in names if n in st.session_state.team_db]


def teams_dataframe(teams: List[dict]) -> pd.DataFrame:
    cols = ["name", "country", "league", "overall", "attack", "midfield", "defence", "star_player"]
    return pd.DataFrame([{c: t.get(c) for c in cols} for t in teams]).rename(
        columns={
            "name": "Team",
            "country": "Country",
            "league": "League",
            "overall": "OVR",
            "attack": "ATT",
            "midfield": "MID",
            "defence": "DEF",
            "star_player": "Star Player",
        }
    )


def show_results(results: List[dict]) -> None:
    if not results:
        st.info("No results yet. Simulate the next matchday or round when you are ready.")
        return
    for r in results:
        winner = f" · Winner: {r['winner']}" if r.get("winner") else ""
        st.markdown(
            f"<div class='card'><div class='scoreline'>{r['home']} {r['home_goals']}–{r['away_goals']} {r['away']}</div>"
            f"<span class='pill info-pill'>xG {r['home_xg']}–{r['away_xg']}</span>"
            f"<span class='pill'>{r['played_at']}</span>{winner}<hr/>",
            unsafe_allow_html=True,
        )
        with st.expander("View match details", expanded=False):
            for event in r["events"]:
                st.write(event)
        st.markdown("</div>", unsafe_allow_html=True)


def show_tables(game: dict) -> None:
    if game["mode"] == "cup" and game.get("group_tables"):
        tabs = st.tabs([f"Group {g}" for g in sorted(game["group_tables"].keys())])
        for tab, group_name in zip(tabs, sorted(game["group_tables"].keys())):
            with tab:
                st.dataframe(pd.DataFrame(sorted_table(game["group_tables"][group_name])), hide_index=True, use_container_width=True)
    else:
        table = sorted_table(game["standings"])
        if table:
            st.dataframe(pd.DataFrame(table), hide_index=True, use_container_width=True)
        else:
            st.info("No league table yet.")


def show_bracket(game: dict) -> None:
    if not game.get("knockout_rounds"):
        st.info("No knockout bracket yet. Finish the league/group stage first or create a knockout tournament.")
        return
    for rnd in game["knockout_rounds"]:
        st.markdown(f"### {rnd['name']}")
        rows = []
        for m in rnd["matches"]:
            if m["played"] and m.get("result"):
                r = m["result"]
                score = f"{r['home_goals']}–{r['away_goals']}"
                winner = r.get("winner") or "—"
            else:
                score = "v"
                winner = "Pending"
            rows.append({"Home": m["home"], "Score": score, "Away": m["away"], "Winner": winner})
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


def show_stats(game: dict) -> None:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Top scorers")
        rows = top_list(game.get("top_scorers", {}), 12)
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True) if rows else st.caption("No goals yet.")
    with c2:
        st.markdown("### Top assisters")
        rows = top_list(game.get("top_assisters", {}), 12)
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True) if rows else st.caption("No assists yet.")


def setup_real_continental() -> None:
    st.markdown("## 1. Play a Real Continental Tournament")
    competition = st.selectbox("Choose competition", list(CONTINENTAL.keys()))
    st.caption("Seeded with 2025/26 league-phase teams. The format uses league phase → play-offs → round of 16 → final.")
    preview = get_teams_by_names(CONTINENTAL[competition]["teams"])
    with st.expander("Preview teams and ratings"):
        st.dataframe(teams_dataframe(preview), hide_index=True, use_container_width=True)
    if st.button("Create continental tournament", type="primary"):
        st.session_state.game = create_uefa_tournament(competition)
        st.session_state.last_results = []
        st.success(f"Created {competition}. Simulate one matchday at a time.")


def setup_custom() -> None:
    st.markdown("## 2. Create a Custom League/Tournament")
    all_names = sorted(st.session_state.team_db.keys())
    name = st.text_input("Competition name", value="My Custom Football Universe")
    fmt = st.selectbox("Format", ["Standard League", "Straight Knockout", "Cup: Groups + Knockout"])
    selected = st.multiselect("Select real teams", all_names, default=all_names[:8])

    st.markdown("### Add a custom team")
    with st.form("custom_team_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            team_name = st.text_input("Team name")
            country = st.text_input("Country", value="Custom")
            league = st.text_input("League", value="Custom League")
            star = st.text_input("Star player", value="Generated Hero")
        with c2:
            attack = st.slider("Attack", 50, 99, 75)
            midfield = st.slider("Midfield", 50, 99, 75)
            defence = st.slider("Defence", 50, 99, 75)
        submitted = st.form_submit_button("Add custom team")
        if submitted and team_name:
            overall = round((attack * .34) + (midfield * .33) + (defence * .33))
            st.session_state.team_db[team_name] = {
                "id": team_name.lower().replace(" ", "-"),
                "name": team_name,
                "country": country,
                "league": league,
                "attack": attack,
                "midfield": midfield,
                "defence": defence,
                "overall": overall,
                "star_player": star,
            }
            st.success(f"Added {team_name}. Select it from the real/custom team list above.")

    teams = get_teams_by_names(selected)
    if selected:
        st.dataframe(teams_dataframe(teams), hide_index=True, use_container_width=True)

    min_teams = 2 if fmt == "Straight Knockout" else 3
    if fmt == "Cup: Groups + Knockout":
        groups = st.slider("Number of groups", 2, 8, 4)
    else:
        groups = 0
    double_round = st.checkbox("Double round-robin", value=False, disabled=(fmt != "Standard League"))

    if st.button("Create custom competition", type="primary"):
        if len(teams) < min_teams:
            st.error(f"Pick at least {min_teams} teams.")
        elif fmt == "Straight Knockout" and len(teams) & (len(teams) - 1) != 0:
            st.error("Straight knockout works best with 2, 4, 8, 16 or 32 teams.")
        elif fmt == "Cup: Groups + Knockout" and len(teams) < groups * 2:
            st.error("Use at least two teams per group.")
        else:
            if fmt == "Standard League":
                game = create_league(name, teams, double_round=double_round)
            elif fmt == "Straight Knockout":
                game = create_knockout(name, teams)
            else:
                game = create_cup(name, teams, groups=groups)
            st.session_state.game = game
            st.session_state.last_results = []
            st.success(f"Created {name}.")


def quick_match() -> None:
    st.markdown("## 3. Quick Match")
    names = sorted(st.session_state.team_db.keys())
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        home = st.selectbox("Home team", names, index=names.index("Arsenal") if "Arsenal" in names else 0)
    with c2:
        away_default = names.index("Real Madrid") if "Real Madrid" in names else min(1, len(names) - 1)
        away = st.selectbox("Away team", names, index=away_default)
    with c3:
        knockout = st.checkbox("Knockout rules", value=False)
    if st.button("Simulate quick match", type="primary"):
        if home == away:
            st.error("Pick two different teams.")
        else:
            st.session_state.quick_match_result = simulate_match(
                st.session_state.team_db[home], st.session_state.team_db[away], knockout=knockout
            )
    if st.session_state.quick_match_result:
        show_results([st.session_state.quick_match_result])


def setup_screen() -> None:
    hero()
    st.markdown("## Choose your starting mode")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='mode-card'><h3>🏆 Real Continental Tournament</h3><p>Champions League, Europa League or Conference League with 2025/26 teams.</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='mode-card'><h3>🛠️ Custom Competition</h3><p>Create leagues, cups and knockout brackets using real and fictional teams.</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='mode-card'><h3>⚡ Quick Match</h3><p>Pick any two teams for an instant realistic text-based simulation.</p></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["1. Real Continental", "2. Custom", "3. Quick Match"])
    with tab1:
        setup_real_continental()
    with tab2:
        setup_custom()
    with tab3:
        quick_match()


def play_screen(game: dict) -> None:
    hero()
    st.markdown(f"## {game['name']}")
    status = game["stage"].replace("_", " ").title()
    m_remaining = len(upcoming_matches(game))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Stage", status)
    c2.metric("Teams", len(game["teams"]))
    c3.metric("Next fixtures", m_remaining)
    c4.metric("Champion", game.get("champion") or "TBD")

    if game["stage"] == "league":
        st.markdown(f"### Upcoming Matchday {game['matchday_index'] + 1}")
        rows = [{"Home": m["home"], "Away": m["away"], "Group": m.get("group", "—")} for m in upcoming_matches(game)]
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Quick Simulate Matchday", type="primary"):
                st.session_state.game, st.session_state.last_results = simulate_matchday(game, st.session_state.team_db)
                st.rerun()
        with col2:
            st.caption("This only simulates the next matchday. It will not simulate ahead without you pressing the button again.")

    elif game["stage"] == "knockout":
        current = game["knockout_rounds"][-1]
        st.markdown(f"### Upcoming {current['name']}")
        rows = [{"Home": m["home"], "Away": m["away"]} for m in upcoming_matches(game)]
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Simulate Knockout Round", type="primary"):
                st.session_state.game, st.session_state.last_results = simulate_knockout_round(game, st.session_state.team_db)
                st.rerun()
        with col2:
            st.caption("This simulates one knockout round only, then pauses for your next command.")

    elif game["stage"] == "complete":
        st.success(f"Tournament complete. Champion: {game.get('champion', 'Unknown')}")
        if st.button("Start a new game"):
            st.session_state.game = None
            st.session_state.last_results = []
            st.rerun()

    st.markdown("---")
    tab_results, tab_table, tab_bracket, tab_stats, tab_teams, tab_save = st.tabs(
        ["Results", "Tables", "Bracket", "Stats", "Teams", "Save / Load"]
    )
    with tab_results:
        show_results(st.session_state.last_results or game.get("history", [])[-12:])
    with tab_table:
        show_tables(game)
    with tab_bracket:
        show_bracket(game)
    with tab_stats:
        show_stats(game)
    with tab_teams:
        st.dataframe(teams_dataframe(game["teams"]), hide_index=True, use_container_width=True)
    with tab_save:
        save_text = dumps_state(game)
        st.download_button("Download save file", save_text, file_name="football_simulator_save.json", mime="application/json")
        uploaded = st.file_uploader("Load save file", type=["json"])
        if uploaded is not None:
            try:
                st.session_state.game = loads_state(uploaded.read().decode("utf-8"))
                st.session_state.last_results = []
                st.success("Save loaded. Use the buttons above to continue.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not load save: {exc}")


def sidebar() -> None:
    st.sidebar.title("⚽ Simulator Control")
    st.sidebar.caption("One matchday or knockout round at a time.")
    if st.sidebar.button("Reset active game"):
        st.session_state.game = None
        st.session_state.last_results = []
        st.session_state.quick_match_result = None
        st.rerun()
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Team database")
    countries = sorted({t["country"] for t in st.session_state.team_db.values()})
    country = st.sidebar.selectbox("Filter by country", ["All"] + countries)
    teams = list(st.session_state.team_db.values())
    if country != "All":
        teams = [t for t in teams if t["country"] == country]
    st.sidebar.caption(f"{len(teams)} teams available")
    st.sidebar.dataframe(teams_dataframe(teams).head(10), hide_index=True, use_container_width=True)


def main() -> None:
    init()
    sidebar()
    if st.session_state.game is None:
        setup_screen()
    else:
        play_screen(st.session_state.game)


if __name__ == "__main__":
    main()
