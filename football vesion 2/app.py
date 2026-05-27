from __future__ import annotations

import json
from copy import deepcopy
from html import escape
from typing import List

import pandas as pd
import streamlit as st

from football_sim.data import CONTINENTAL, INTERNATIONAL, TEAMS
from football_sim.simulator import dumps_state, loads_state, sorted_table, top_list, simulate_match
from football_sim.tournaments import (
    create_cup,
    create_knockout,
    create_league,
    create_uefa_tournament,
    create_international_tournament,
    simulate_knockout_round,
    simulate_matchday,
    upcoming_matches,
)

st.set_page_config(
    page_title="Football Simulator Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS = """
<style>
:root {
    --bg-card: rgba(15, 23, 42, 0.88);
    --bg-card-strong: rgba(2, 6, 23, 0.92);
    --border: rgba(148, 163, 184, 0.25);
    --text-soft: #cbd5e1;
    --text-muted: #94a3b8;
    --accent: #22c55e;
    --accent-2: #38bdf8;
    --gold: #facc15;
}
.stApp {
    background:
        radial-gradient(circle at top left, rgba(34,197,94,.22), transparent 28%),
        radial-gradient(circle at top right, rgba(56,189,248,.20), transparent 30%),
        linear-gradient(135deg, #020617 0%, #08111f 48%, #0f172a 100%);
    color: #f8fafc;
}
.block-container {
    max-width: 1100px;
    padding: 1.15rem 1rem 5rem;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(2,6,23,.98), rgba(15,23,42,.96));
    border-right: 1px solid rgba(148,163,184,.18);
}
.hero {
    position: relative;
    overflow: hidden;
    padding: 1.45rem;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(34,197,94,.18), rgba(56,189,248,.12)), rgba(15,23,42,.74);
    border: 1px solid rgba(148, 163, 184, .25);
    box-shadow: 0 22px 70px rgba(0,0,0,.32);
    margin-bottom: 1rem;
}
.hero:after {
    content: "";
    position: absolute;
    width: 190px;
    height: 190px;
    right: -70px;
    top: -70px;
    border-radius: 999px;
    background: rgba(250,204,21,.12);
    border: 1px solid rgba(250,204,21,.18);
}
.hero h1 {
    font-size: clamp(2.05rem, 8vw, 3.1rem);
    line-height: .96;
    margin: 0 0 .7rem 0;
    letter-spacing: -.055em;
}
.hero p { color: var(--text-soft); font-size: clamp(.98rem, 2.8vw, 1.08rem); max-width: 880px; }
.card, .instruction-card, .mode-card, .fixture-card, .result-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 1rem;
    box-shadow: 0 12px 42px rgba(0,0,0,.25);
    margin-bottom: .85rem;
}
.instruction-grid, .mode-grid, .fixture-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: .8rem;
}
.mode-card {
    min-height: 148px;
    background: linear-gradient(145deg, rgba(15,23,42,.95), rgba(30,41,59,.70));
}
.mode-card h3, .instruction-card h4 { margin-top: 0; margin-bottom: .35rem; }
.mode-card p, .instruction-card p, .fixture-card p, .result-card p { color: var(--text-soft); margin-bottom: .25rem; }
.fixture-card { padding: .9rem; }
.fixture-vs {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: .6rem;
    font-weight: 800;
}
.fixture-vs span { flex: 1; }
.fixture-vs .away { text-align: right; }
.vs-pill {
    flex: 0 0 auto;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 30px;
    border-radius: 999px;
    background: rgba(56,189,248,.13);
    border: 1px solid rgba(56,189,248,.24);
    color: #bae6fd;
    font-size: .78rem;
}
.scoreline {
    font-size: clamp(1.12rem, 5.4vw, 1.45rem);
    font-weight: 900;
    letter-spacing: -.03em;
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
    white-space: nowrap;
}
.danger-pill { background: rgba(239,68,68,.14); color: #fecaca; border-color: rgba(239,68,68,.25); }
.info-pill { background: rgba(56,189,248,.14); color: #bae6fd; border-color: rgba(56,189,248,.25); }
.gold-pill { background: rgba(250,204,21,.14); color: #fef08a; border-color: rgba(250,204,21,.26); }
.stButton>button {
    border-radius: 16px;
    border: 1px solid rgba(148,163,184,.22);
    font-weight: 800;
    min-height: 48px;
    width: 100%;
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
.winner-card {
    position: relative;
    overflow: hidden;
    border-radius: 32px;
    padding: 1.6rem 1.1rem;
    min-height: 270px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background:
        radial-gradient(circle at top, rgba(250,204,21,.36), transparent 32%),
        radial-gradient(circle at bottom left, rgba(34,197,94,.25), transparent 35%),
        linear-gradient(145deg, rgba(15,23,42,.97), rgba(30,41,59,.86));
    border: 1px solid rgba(250,204,21,.34);
    box-shadow: 0 26px 80px rgba(0,0,0,.42);
    margin: 1rem 0;
}
.trophy {
    font-size: clamp(4rem, 22vw, 7.5rem);
    line-height: .95;
    filter: drop-shadow(0 18px 34px rgba(250,204,21,.22));
    animation: trophy-pop 900ms ease-out both, trophy-glow 2.8s ease-in-out infinite;
}
.winner-card h2 {
    margin: .4rem 0 .15rem;
    font-size: clamp(1.75rem, 8vw, 3.4rem);
    line-height: .95;
    letter-spacing: -.055em;
}
.winner-card p { color: var(--text-soft); margin: .3rem auto; max-width: 680px; }
.confetti {
    position: absolute;
    width: 9px;
    height: 15px;
    border-radius: 3px;
    opacity: .9;
    animation: fall 3.6s linear infinite;
}
.confetti.c1 { left: 8%; top: -20px; background: #22c55e; animation-delay: .1s; }
.confetti.c2 { left: 21%; top: -25px; background: #38bdf8; animation-delay: .9s; }
.confetti.c3 { left: 38%; top: -25px; background: #facc15; animation-delay: .35s; }
.confetti.c4 { left: 53%; top: -35px; background: #fb7185; animation-delay: 1.25s; }
.confetti.c5 { left: 69%; top: -30px; background: #a78bfa; animation-delay: .65s; }
.confetti.c6 { left: 86%; top: -30px; background: #34d399; animation-delay: 1.6s; }
@keyframes fall {
    0% { transform: translateY(-20px) rotate(0deg); }
    100% { transform: translateY(360px) rotate(420deg); }
}
@keyframes trophy-pop {
    0% { transform: scale(.72); opacity: 0; }
    70% { transform: scale(1.08); opacity: 1; }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes trophy-glow {
    0%, 100% { filter: drop-shadow(0 18px 34px rgba(250,204,21,.18)); }
    50% { filter: drop-shadow(0 22px 48px rgba(250,204,21,.42)); }
}
.mobile-note {
    background: rgba(56,189,248,.10);
    border: 1px solid rgba(56,189,248,.22);
    color: #dbeafe;
    border-radius: 18px;
    padding: .75rem .9rem;
    margin-bottom: .9rem;
}
@media (max-width: 760px) {
    .block-container { padding: .75rem .65rem 5.5rem; }
    .hero { padding: 1.05rem; border-radius: 22px; }
    .instruction-grid, .mode-grid, .fixture-grid { grid-template-columns: 1fr; gap: .65rem; }
    .mode-card, .instruction-card, .fixture-card, .result-card { border-radius: 18px; padding: .88rem; min-height: auto; }
    [data-testid="stHorizontalBlock"] { gap: .55rem; }
    [data-testid="stMetric"] { padding: .72rem; }
    .stTabs [data-baseweb="tab-list"] { gap: .25rem; overflow-x: auto; }
    .stTabs [data-baseweb="tab"] { padding: .45rem .7rem; }
    .winner-card { min-height: 245px; border-radius: 24px; padding: 1.15rem .8rem; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def h(value: object) -> str:
    """Escape dynamic values before inserting them into unsafe HTML blocks."""
    return escape(str(value), quote=True)


def init() -> None:
    if "team_db" not in st.session_state:
        st.session_state.team_db = {team["name"]: deepcopy(team) for team in TEAMS}
    if "game" not in st.session_state:
        st.session_state.game = None
    if "last_results" not in st.session_state:
        st.session_state.last_results = []
    if "quick_match_result" not in st.session_state:
        st.session_state.quick_match_result = None
    if "start_mode" not in st.session_state:
        st.session_state.start_mode = "🌍 World Cup / EURO"


def hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>⚽ Football Simulator Pro</h1>
            <p>
            A mobile-first text football universe. Create teams, run World Cups, EUROs, leagues, cups and European club tournaments,
            then simulate one matchday or knockout round at a time with stat-weighted winners, real-player scorers,
            assists, cards, injuries, tables and trophy celebrations.
            </p>
            <span class="pill">📱 Mobile-first</span>
            <span class="pill info-pill">One command at a time</span>
            <span class="pill">Real-player squads</span>
            <span class="pill gold-pill">Trophy winner graphic</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def instructions_panel(compact: bool = False) -> None:
    title = "How to play" if not compact else "Quick instructions"
    st.markdown(f"### {title}")
    st.markdown(
        """
        <div class="instruction-grid">
            <div class="instruction-card">
                <h4>1. Choose a mode</h4>
                <p>Start with the World Cup, EURO, a real continental club tournament, your own competition, or a quick match.</p>
            </div>
            <div class="instruction-card">
                <h4>2. Simulate safely</h4>
                <p>The game never runs ahead. Press one button to simulate the next matchday or knockout round only.</p>
            </div>
            <div class="instruction-card">
                <h4>3. Review the world</h4>
                <p>Open results, tables, brackets, player stats, teams and save/load from the tabs after each command.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not compact:
        st.markdown(
            """
            <div class="mobile-note">
                <strong>Phone tip:</strong> the sidebar starts closed. Use the top-left arrow only when you want reset,
                database filtering, or save guidance. Main controls stay in the page so it feels app-like on mobile.
            </div>
            """,
            unsafe_allow_html=True,
        )


def winner_graphic(champion: str | None, competition: str) -> None:
    if not champion:
        return
    st.markdown(
        f"""
        <div class="winner-card">
            <div class="confetti c1"></div><div class="confetti c2"></div><div class="confetti c3"></div>
            <div class="confetti c4"></div><div class="confetti c5"></div><div class="confetti c6"></div>
            <div>
                <div class="trophy">🏆</div>
                <span class="pill gold-pill">Champions crowned</span>
                <h2>{h(champion)}</h2>
                <p>{h(champion)} have won <strong>{h(competition)}</strong>. Save this universe or start a new competition.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_teams_by_names(names: List[str]) -> List[dict]:
    return [deepcopy(st.session_state.team_db[n]) for n in names if n in st.session_state.team_db]


def teams_dataframe(teams: List[dict]) -> pd.DataFrame:
    rows = []
    for t in teams:
        rows.append({
            "Team": t.get("name"),
            "Country": t.get("country"),
            "League": t.get("league"),
            "OVR": t.get("overall"),
            "ATT": t.get("attack"),
            "MID": t.get("midfield"),
            "DEF": t.get("defence"),
            "Star Player": t.get("star_player"),
            "Squad": len(t.get("players") or []),
        })
    return pd.DataFrame(rows)


def fixture_cards(fixtures: List[dict]) -> None:
    if not fixtures:
        st.info("No fixtures waiting.")
        return
    html = ["<div class='fixture-grid'>"]
    for match in fixtures[:12]:
        group = match.get("group")
        group_html = f"<span class='pill info-pill'>Group {h(group)}</span>" if group else ""
        html.append(
            f"""
            <div class="fixture-card">
                <div class="fixture-vs"><span>{h(match['home'])}</span><b class="vs-pill">v</b><span class="away">{h(match['away'])}</span></div>
                {group_html}
            </div>
            """
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)
    if len(fixtures) > 12:
        st.caption(f"Showing 12 of {len(fixtures)} fixtures. Full fixture table is below.")
        st.dataframe(
            pd.DataFrame([{"Home": m["home"], "Away": m["away"], "Group": m.get("group", "—")} for m in fixtures]),
            hide_index=True,
            use_container_width=True,
        )


def show_results(results: List[dict]) -> None:
    if not results:
        st.info("No results yet. Simulate the next matchday or round when you are ready.")
        return
    for idx, r in enumerate(results):
        winner = f"<span class='pill gold-pill'>Winner: {h(r['winner'])}</span>" if r.get("winner") else ""
        penalties = ""
        if r.get("penalties"):
            penalties = f"<span class='pill info-pill'>Pens {r['penalties']['home']}–{r['penalties']['away']}</span>"
        st.markdown(
            f"""
            <div class="result-card">
                <div class="scoreline">{h(r['home'])} {r['home_goals']}–{r['away_goals']} {h(r['away'])}</div>
                <span class="pill info-pill">xG {r['home_xg']}–{r['away_xg']}</span>
                <span class="pill">{h(r['played_at'])}</span>
                {winner}{penalties}
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander(f"View match details: {r['home']} v {r['away']}", expanded=(idx == 0 and len(results) == 1)):
            for event in r["events"]:
                st.write(event)


def show_tables(game: dict) -> None:
    if game["mode"] in ("cup", "international") and game.get("group_tables"):
        tabs = st.tabs([f"Group {g}" for g in sorted(game["group_tables"].keys())])
        for tab, group_name in zip(tabs, sorted(game["group_tables"].keys())):
            with tab:
                st.dataframe(pd.DataFrame(sorted_table(game["group_tables"][group_name])), hide_index=True, use_container_width=True)
        best_thirds = game.get("config", {}).get("best_thirds_qualified")
        if best_thirds:
            st.markdown("### Best third-placed qualifiers")
            st.dataframe(pd.DataFrame(best_thirds), hide_index=True, use_container_width=True)
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



def show_squad_browser(teams: List[dict]) -> None:
    national = [t for t in teams if t.get("players")]
    if not national:
        st.caption("No detailed squads for these teams yet. Custom and club teams use generated depth players around their star player.")
        return
    selected = st.selectbox("View player squad", [t["name"] for t in national])
    team = next(t for t in national if t["name"] == selected)
    st.markdown(f"### {selected} squad core")
    st.caption("Player ratings are editable game estimates used for weighted scorers, assists, cards and injury events.")
    st.dataframe(pd.DataFrame(team.get("players", [])), hide_index=True, use_container_width=True)


def setup_international() -> None:
    st.markdown("## 🌍 World Cup / EURO")
    competition = st.selectbox("Choose international tournament", list(INTERNATIONAL.keys()))
    cfg = INTERNATIONAL[competition]
    st.caption(cfg.get("format_note", "Group stage followed by knockout football."))
    preview = get_teams_by_names(cfg["teams"])
    with st.expander("Preview national teams, ratings and squad sizes", expanded=True):
        st.dataframe(teams_dataframe(preview), hide_index=True, use_container_width=True)
    with st.expander("Preview real-player squad cores"):
        show_squad_browser(preview)
    if st.button("Create international tournament", type="primary"):
        st.session_state.game = create_international_tournament(competition)
        st.session_state.last_results = []
        st.success(f"Created {competition}. Simulate one group matchday at a time.")
        st.rerun()

def setup_real_continental() -> None:
    st.markdown("## 🏆 Real Continental Tournament")
    competition = st.selectbox("Choose competition", list(CONTINENTAL.keys()))
    st.caption("Seeded with 2025/26 league-phase club teams. The game format uses league phase → play-offs → round of 16 → final.")
    preview = get_teams_by_names(CONTINENTAL[competition]["teams"])
    with st.expander("Preview teams and ratings"):
        st.dataframe(teams_dataframe(preview), hide_index=True, use_container_width=True)
    if st.button("Create continental tournament", type="primary"):
        st.session_state.game = create_uefa_tournament(competition)
        st.session_state.last_results = []
        st.success(f"Created {competition}. Simulate one matchday at a time.")
        st.rerun()


def setup_custom() -> None:
    st.markdown("## 🛠️ Create a Custom League/Tournament")
    all_names = sorted(st.session_state.team_db.keys())
    name = st.text_input("Competition name", value="My Custom Football Universe")
    fmt = st.selectbox("Format", ["Standard League", "Straight Knockout", "Cup: Groups + Knockout"])
    selected = st.multiselect("Select real or custom teams", all_names, default=all_names[:8])

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
            st.success(f"Added {team_name}. Select it from the team list above.")

    teams = get_teams_by_names(selected)
    if selected:
        with st.expander(f"Selected teams ({len(teams)})", expanded=False):
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
            st.rerun()


def quick_match() -> None:
    st.markdown("## ⚡ Quick Match")
    names = sorted(st.session_state.team_db.keys())
    c1, c2 = st.columns(2)
    with c1:
        home = st.selectbox("Home team", names, index=names.index("Arsenal") if "Arsenal" in names else 0)
    with c2:
        away_default = names.index("Real Madrid") if "Real Madrid" in names else min(1, len(names) - 1)
        away = st.selectbox("Away team", names, index=away_default)
    knockout = st.checkbox("Use knockout rules: extra time and penalties if level", value=False)
    if st.button("Simulate quick match", type="primary"):
        if home == away:
            st.error("Pick two different teams.")
        else:
            st.session_state.quick_match_result = simulate_match(
                st.session_state.team_db[home], st.session_state.team_db[away], knockout=knockout
            )
    if st.session_state.quick_match_result:
        show_results([st.session_state.quick_match_result])
        if st.session_state.quick_match_result.get("winner"):
            winner_graphic(st.session_state.quick_match_result.get("winner"), "Quick Match")


def setup_screen() -> None:
    hero()
    instructions_panel()
    st.markdown("## Choose your starting mode")
    st.markdown(
        """
        <div class="mode-grid">
            <div class="mode-card"><h3>🌍 World Cup / EURO</h3><p>International tournaments with national team ratings and real-player squad cores.</p></div>
            <div class="mode-card"><h3>🏆 Real Continental</h3><p>Champions League, Europa League or Conference League.</p></div>
            <div class="mode-card"><h3>🛠️ Custom Competition</h3><p>Create leagues, cups and knockout brackets with real, national or fictional teams.</p></div>
            <div class="mode-card"><h3>⚡ Quick Match</h3><p>Pick any two teams for an instant simulation.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    mode = st.radio(
        "Start mode",
        ["🌍 World Cup / EURO", "🏆 Real Continental Tournament", "🛠️ Custom League/Tournament", "⚡ Quick Match"],
        key="start_mode",
        label_visibility="collapsed",
    )
    if mode.startswith("🌍"):
        setup_international()
    elif mode.startswith("🏆"):
        setup_real_continental()
    elif mode.startswith("🛠️"):
        setup_custom()
    else:
        quick_match()


def play_screen(game: dict) -> None:
    hero()
    st.markdown(f"## {game['name']}")
    if game.get("config", {}).get("format_note"):
        st.caption(game["config"]["format_note"])
    status = game["stage"].replace("_", " ").title()
    m_remaining = len(upcoming_matches(game))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Stage", status)
    c2.metric("Teams", len(game["teams"]))
    c3.metric("Next fixtures", m_remaining)
    c4.metric("Champion", game.get("champion") or "TBD")

    if game["stage"] == "league":
        st.markdown(f"### Upcoming Matchday {game['matchday_index'] + 1}")
        fixtures = upcoming_matches(game)
        fixture_cards(fixtures)
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Quick Simulate Matchday", type="primary"):
                st.session_state.game, st.session_state.last_results = simulate_matchday(game, st.session_state.team_db)
                st.rerun()
        with col2:
            st.caption("This only simulates the next matchday. It will not simulate ahead without you pressing the button again.")

    elif game["stage"] == "knockout":
        current = game["knockout_rounds"][-1]
        st.markdown(f"### Upcoming {current['name']}")
        fixtures = upcoming_matches(game)
        fixture_cards(fixtures)
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Simulate Knockout Round", type="primary"):
                st.session_state.game, st.session_state.last_results = simulate_knockout_round(game, st.session_state.team_db)
                st.rerun()
        with col2:
            st.caption("This simulates one knockout round only, then pauses for your next command.")

    elif game["stage"] == "complete":
        winner_graphic(game.get("champion"), game["name"])
        if st.button("Start a new game"):
            st.session_state.game = None
            st.session_state.last_results = []
            st.rerun()

    st.markdown("---")
    tab_results, tab_table, tab_bracket, tab_stats, tab_teams, tab_save, tab_help = st.tabs(
        ["Results", "Tables", "Bracket", "Stats", "Teams", "Save", "Help"]
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
        show_squad_browser(game["teams"])
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
    with tab_help:
        instructions_panel(compact=True)
        st.markdown(
            """
            **Game rules**

            - League/group stage: 3 points for a win, 1 for a draw.
            - Knockout games: draws go to extra time and then penalties.
            - Match results are weighted by Attack, Midfield, Defence, Overall, player ratings, squad profile and home advantage.
            - National-team scorers and assisters are chosen from real-player squad cores using position/rating weights.
            - You control the pace. The app pauses after every matchday or knockout round.
            """
        )


def sidebar() -> None:
    st.sidebar.title("⚽ Simulator Control")
    st.sidebar.caption("Designed for mobile: keep this closed unless you need admin controls.")
    if st.sidebar.button("Reset active game"):
        st.session_state.game = None
        st.session_state.last_results = []
        st.session_state.quick_match_result = None
        st.rerun()
    st.sidebar.markdown("---")
    with st.sidebar.expander("How to play", expanded=False):
        st.write("1. Pick a mode.")
        st.write("2. Simulate one matchday or round.")
        st.write("3. Check results, tables, bracket and stats.")
        st.write("4. Download a save file anytime.")
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
