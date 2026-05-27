from __future__ import annotations

import json
from copy import deepcopy
from html import escape
from textwrap import dedent
from typing import List

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
    --text-soft: #e2e8f0;
    --text-muted: #cbd5e1;
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

.stApp,
.stApp p,
.stApp li,
.stApp label,
.stApp span,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p {
    color: #f8fafc !important;
}
.card, .instruction-card, .mode-card, .fixture-card, .result-card {
    color: #f8fafc !important;
}
.card p, .instruction-card p, .mode-card p, .fixture-card p, .result-card p {
    color: #e2e8f0 !important;
}
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] * {
    color: #f8fafc !important;
}
[data-testid="stTable"] table,
[data-testid="stTable"] th,
[data-testid="stTable"] td {
    color: #f8fafc !important;
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

.next-action-card {
    background: linear-gradient(135deg, rgba(34,197,94,.18), rgba(56,189,248,.10)), rgba(15,23,42,.9);
    border: 1px solid rgba(34,197,94,.32);
    border-radius: 22px;
    padding: 1rem;
    margin: .95rem 0;
    box-shadow: 0 12px 42px rgba(0,0,0,.24);
}
.next-action-card h3 {
    margin: 0 0 .35rem;
    color: #ffffff !important;
    letter-spacing: -.02em;
}
.next-action-card p, .next-action-card li {
    color: #e2e8f0 !important;
    margin: .2rem 0;
}
.next-action-card .next-label {
    display: inline-block;
    margin-bottom: .35rem;
    padding: .22rem .58rem;
    border-radius: 999px;
    background: rgba(250,204,21,.16);
    color: #fef9c3 !important;
    border: 1px solid rgba(250,204,21,.32);
    font-size: .82rem;
    font-weight: 900;
}
.result-story {
    margin-top: .6rem;
    color: #e2e8f0 !important;
    font-size: .96rem;
    line-height: 1.35;
}

.mini-stat-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: .45rem;
    margin-top: .7rem;
}
.mini-stat {
    background: rgba(2, 6, 23, .42);
    border: 1px solid rgba(148, 163, 184, .22);
    border-radius: 14px;
    padding: .55rem .62rem;
    color: #f8fafc !important;
}
.mini-stat b {
    display: block;
    font-size: .74rem;
    color: #e2e8f0 !important;
    opacity: .96;
    margin-bottom: .16rem;
}
.mini-stat span {
    color: #ffffff !important;
    font-weight: 900;
    letter-spacing: -.02em;
}
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] *,
.stTabs [data-baseweb="tab"],
.stTabs [data-baseweb="tab"] * {
    color: #f8fafc !important;
}
.stSelectbox label,
.stMultiSelect label,
.stRadio label,
.stCheckbox label,
.stSlider label,
.stTextInput label,
.stFileUploader label {
    color: #f8fafc !important;
}

@media (max-width: 760px) {
    .block-container { padding: .75rem .65rem 5.5rem; }
    .hero { padding: 1.05rem; border-radius: 22px; }
    .instruction-grid, .mode-grid, .fixture-grid { grid-template-columns: 1fr; gap: .65rem; }
    .mini-stat-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .48rem; }
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


def render_html(markup: str) -> None:
    """Render custom HTML safely without Markdown turning indented tags into code blocks."""
    cleaned = " ".join(line.strip() for line in dedent(markup).strip().splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


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
    render_html(
        """
        <div class="hero">
            <h1>⚽ Football Simulator Pro</h1>
            <p>
            A mobile-first text football universe. Create teams, run World Cups, EUROs, leagues, cups and European club tournaments,
            then simulate one matchday or knockout round at a time with stat-weighted winners, real-player scorers,
            assists, detailed match stats, fewer card-heavy events, injuries, tables and trophy celebrations.
            </p>
            <span class="pill">📱 Mobile-first</span>
            <span class="pill info-pill">One command at a time</span>
            <span class="pill">Real-player squads</span>
            <span class="pill gold-pill">Trophy winner graphic</span>
        </div>
        """
    )


def instructions_panel(compact: bool = False) -> None:
    title = "How to play" if not compact else "Quick instructions"
    st.markdown(f"### {title}")
    render_html(
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
        """
    )
    if not compact:
        render_html(
            """
            <div class="mobile-note">
                <strong>Phone tip:</strong> the sidebar starts closed. Use the top-left arrow only when you want reset,
                database filtering, or save guidance. Main controls stay in the page so it feels app-like on mobile.
            </div>
            """
        )


def winner_graphic(champion: str | None, competition: str) -> None:
    if not champion:
        return
    render_html(
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
        """
    )


def get_teams_by_names(names: List[str]) -> List[dict]:
    return [deepcopy(st.session_state.team_db[n]) for n in names if n in st.session_state.team_db]


def teams_table_rows(teams: List[dict]) -> List[dict]:
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
    return rows


def fixture_cards(fixtures: List[dict]) -> None:
    if not fixtures:
        st.info("No fixtures waiting.")
        return

    cards: List[str] = []
    for match in fixtures[:12]:
        group = match.get("group")
        group_html = f"<span class='pill info-pill'>Group {h(group)}</span>" if group else ""
        cards.append(
            "<div class='fixture-card'>"
            f"<div class='fixture-vs'><span>{h(match['home'])}</span><b class='vs-pill'>v</b><span class='away'>{h(match['away'])}</span></div>"
            f"{group_html}"
            "</div>"
        )

    render_html("<div class='fixture-grid'>" + "".join(cards) + "</div>")
    if len(fixtures) > 12:
        st.caption(f"Showing 12 of {len(fixtures)} fixtures. Full fixture table is below.")
        st.dataframe(
            [{"Home": m["home"], "Away": m["away"], "Group": m.get("group", "—")} for m in fixtures],
            hide_index=True,
            use_container_width=True,
        )


def match_stats_rows(result: dict) -> List[dict]:
    stats = result.get("match_stats") or {}
    home_stats = stats.get(result.get("home"), {})
    away_stats = stats.get(result.get("away"), {})
    labels = [
        ("Possession", "possession", "%"),
        ("Shots", "shots", ""),
        ("Shots on target", "shots_on_target", ""),
        ("Big chances", "big_chances", ""),
        ("Corners", "corners", ""),
        ("Fouls", "fouls", ""),
        ("Pass accuracy", "pass_accuracy", "%"),
        ("Keeper saves", "keeper_saves", ""),
    ]
    rows = []
    for label, key, suffix in labels:
        h_value = home_stats.get(key, "—")
        a_value = away_stats.get(key, "—")
        if h_value != "—" and suffix:
            h_value = f"{h_value}{suffix}"
        if a_value != "—" and suffix:
            a_value = f"{a_value}{suffix}"
        rows.append({"Stat": label, result.get("home", "Home"): h_value, result.get("away", "Away"): a_value})
    return rows


def match_summary_html(result: dict) -> str:
    stats = result.get("match_stats") or {}
    home = result.get("home")
    away = result.get("away")
    home_stats = stats.get(home, {})
    away_stats = stats.get(away, {})
    if not home_stats or not away_stats:
        return ""
    return (
        "<div class='mini-stat-grid'>"
        f"<div class='mini-stat'><b>Possession</b><span>{h(home_stats.get('possession', '—'))}%–{h(away_stats.get('possession', '—'))}%</span></div>"
        f"<div class='mini-stat'><b>Shots</b><span>{h(home_stats.get('shots', '—'))}–{h(away_stats.get('shots', '—'))}</span></div>"
        f"<div class='mini-stat'><b>On target</b><span>{h(home_stats.get('shots_on_target', '—'))}–{h(away_stats.get('shots_on_target', '—'))}</span></div>"
        f"<div class='mini-stat'><b>Corners</b><span>{h(home_stats.get('corners', '—'))}–{h(away_stats.get('corners', '—'))}</span></div>"
        "</div>"
    )


def match_story(result: dict) -> str:
    stats = result.get("match_stats") or {}
    home = result.get("home")
    away = result.get("away")
    home_stats = stats.get(home, {})
    away_stats = stats.get(away, {})
    if not home_stats or not away_stats:
        return ""
    home_shots = home_stats.get("shots", 0)
    away_shots = away_stats.get("shots", 0)
    home_poss = home_stats.get("possession", 0)
    away_poss = away_stats.get("possession", 0)
    if result.get("home_goals", 0) > result.get("away_goals", 0):
        winner = home
    elif result.get("away_goals", 0) > result.get("home_goals", 0):
        winner = away
    else:
        winner = None
    if winner:
        if abs(home_shots - away_shots) >= 5:
            dominant = home if home_shots > away_shots else away
            return f"{dominant} created the greater volume of chances, while {winner} made the scoreboard count."
        if abs(home_poss - away_poss) >= 10:
            controller = home if home_poss > away_poss else away
            return f"{controller} controlled long spells of possession, but {winner} found the decisive moments."
        return "A tight game decided by finishing quality and key moments in both boxes."
    return "A balanced contest with both teams having spells of pressure but neither side doing enough to win it."


def next_action_panel(game: dict, context: str = "top") -> None:
    stage = game.get("stage")
    if stage == "league":
        title = f"Next: simulate matchday {game.get('matchday_index', 0) + 1}"
        body = "Tap the green button to play only the next matchday. Then check Results and Tables. The game will pause again."
    elif stage == "knockout":
        current = game.get("knockout_rounds", [{}])[-1].get("name", "knockout round")
        title = f"Next: simulate {current}"
        body = "Tap the green button to play this knockout round only. Then check Results and Bracket before continuing."
    elif stage == "complete":
        title = "Tournament complete"
        body = "The champion has been crowned. Save your universe or start a new game."
    else:
        title = "Next step"
        body = "Choose a mode, then create a competition."
    render_html(
        f'''
        <div class="next-action-card">
            <span class="next-label">WHAT TO CLICK NEXT</span>
            <h3>{h(title)}</h3>
            <p>{h(body)}</p>
            <p><strong>Mobile tip:</strong> results are shown below as cards. Open View match details for timeline and full stats.</p>
        </div>
        '''
    )


def continue_button(game: dict, key: str) -> None:
    if game.get("stage") == "league":
        label = f"▶ Simulate matchday {game.get('matchday_index', 0) + 1}"
        if st.button(label, type="primary", key=key):
            st.session_state.game, st.session_state.last_results = simulate_matchday(game, st.session_state.team_db)
            st.rerun()
    elif game.get("stage") == "knockout":
        current = game.get("knockout_rounds", [{}])[-1].get("name", "knockout round")
        if st.button(f"▶ Simulate {current}", type="primary", key=key):
            st.session_state.game, st.session_state.last_results = simulate_knockout_round(game, st.session_state.team_db)
            st.rerun()


def show_results(results: List[dict]) -> None:
    if not results:
        st.info("No results yet. Simulate the next matchday or round when you are ready.")
        return
    for idx, r in enumerate(results):
        winner = f"<span class='pill gold-pill'>Winner: {h(r['winner'])}</span>" if r.get("winner") else ""
        penalties = ""
        if r.get("penalties"):
            penalties = f"<span class='pill info-pill'>Pens {r['penalties']['home']}–{r['penalties']['away']}</span>"
        summary = match_summary_html(r)
        render_html(
            f"""
            <div class="result-card">
                <div class="scoreline">{h(r['home'])} {r['home_goals']}–{r['away_goals']} {h(r['away'])}</div>
                <span class="pill info-pill">xG {r['home_xg']}–{r['away_xg']}</span>
                <span class="pill">{h(r['played_at'])}</span>
                {winner}{penalties}
                {summary}
                <p class="result-story">{h(match_story(r))}</p>
            </div>
            """
        )
        with st.expander(f"View match details: {r['home']} v {r['away']}", expanded=(idx == 0 and len(results) == 1)):
            stat_rows = match_stats_rows(r)
            if r.get("match_stats"):
                st.markdown("#### Match stats")
                st.dataframe(stat_rows, hide_index=True, use_container_width=True)
            st.markdown("#### Timeline")
            for event in r["events"]:
                st.write(event)


def show_tables(game: dict) -> None:
    if game["mode"] in ("cup", "international") and game.get("group_tables"):
        tabs = st.tabs([f"Group {g}" for g in sorted(game["group_tables"].keys())])
        for tab, group_name in zip(tabs, sorted(game["group_tables"].keys())):
            with tab:
                st.dataframe(sorted_table(game["group_tables"][group_name]), hide_index=True, use_container_width=True)
        best_thirds = game.get("config", {}).get("best_thirds_qualified")
        if best_thirds:
            st.markdown("### Best third-placed qualifiers")
            st.dataframe(best_thirds, hide_index=True, use_container_width=True)
    else:
        table = sorted_table(game["standings"])
        if table:
            st.dataframe(table, hide_index=True, use_container_width=True)
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
        st.dataframe(rows, hide_index=True, use_container_width=True)


def show_stats(game: dict) -> None:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Top scorers")
        scorer_rows = top_list(game.get("top_scorers", {}), 12)
        if scorer_rows:
            st.dataframe(scorer_rows, hide_index=True, use_container_width=True)
        else:
            st.caption("No goals yet.")
    with c2:
        st.markdown("### Top assisters")
        assister_rows = top_list(game.get("top_assisters", {}), 12)
        if assister_rows:
            st.dataframe(assister_rows, hide_index=True, use_container_width=True)
        else:
            st.caption("No assists yet.")



def show_squad_browser(teams: List[dict]) -> None:
    national = [t for t in teams if t.get("players")]
    if not national:
        st.caption("No detailed squads for these teams yet. Custom and club teams use generated depth players around their star player.")
        return
    selected = st.selectbox("View player squad", [t["name"] for t in national])
    team = next(t for t in national if t["name"] == selected)
    st.markdown(f"### {selected} squad core")
    st.caption("Player ratings are editable game estimates used for weighted scorers, assists, match details, lower-noise cards and injury events.")
    st.dataframe(team.get("players", []), hide_index=True, use_container_width=True)


def setup_international() -> None:
    st.markdown("## 🌍 World Cup / EURO")
    competition = st.selectbox("Choose international tournament", list(INTERNATIONAL.keys()))
    cfg = INTERNATIONAL[competition]
    st.caption(cfg.get("format_note", "Group stage followed by knockout football."))
    preview = get_teams_by_names(cfg["teams"])
    with st.expander("Preview national teams, ratings and squad sizes", expanded=True):
        st.dataframe(teams_table_rows(preview), hide_index=True, use_container_width=True)
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
        st.dataframe(teams_table_rows(preview), hide_index=True, use_container_width=True)
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
            st.dataframe(teams_table_rows(teams), hide_index=True, use_container_width=True)

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
    render_html(
        """
        <div class="mode-grid">
            <div class="mode-card"><h3>🌍 World Cup / EURO</h3><p>International tournaments with national team ratings and real-player squad cores.</p></div>
            <div class="mode-card"><h3>🏆 Real Continental</h3><p>Champions League, Europa League or Conference League.</p></div>
            <div class="mode-card"><h3>🛠️ Custom Competition</h3><p>Create leagues, cups and knockout brackets with real, national or fictional teams.</p></div>
            <div class="mode-card"><h3>⚡ Quick Match</h3><p>Pick any two teams for an instant simulation.</p></div>
        </div>
        """
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

    next_action_panel(game)

    if game["stage"] == "league":
        st.markdown(f"### Upcoming Matchday {game['matchday_index'] + 1}")
        fixtures = upcoming_matches(game)
        fixture_cards(fixtures)
        col1, col2 = st.columns([1, 2])
        with col1:
            continue_button(game, key="top_next_matchday")
        with col2:
            st.caption("This only simulates the next matchday. It will not simulate ahead without you pressing the button again.")

    elif game["stage"] == "knockout":
        current = game["knockout_rounds"][-1]
        st.markdown(f"### Upcoming {current['name']}")
        fixtures = upcoming_matches(game)
        fixture_cards(fixtures)
        col1, col2 = st.columns([1, 2])
        with col1:
            continue_button(game, key="top_next_knockout")
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
        st.markdown("### Latest results")
        show_results(st.session_state.last_results or game.get("history", [])[-12:])
        if game.get("stage") in ("league", "knockout"):
            st.markdown("### Continue")
            st.caption("You can continue from here on mobile, so you do not need to scroll back to the top.")
            continue_button(game, key="results_continue")
    with tab_table:
        show_tables(game)
    with tab_bracket:
        show_bracket(game)
    with tab_stats:
        show_stats(game)
    with tab_teams:
        st.dataframe(teams_table_rows(game["teams"]), hide_index=True, use_container_width=True)
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
            - Match details include possession, shots, shots on target, big chances, corners, fouls, pass accuracy and saves.
            - Yellow cards are lower-noise now, so the timeline is driven more by football actions than discipline.
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
    st.sidebar.dataframe(teams_table_rows(teams[:10]), hide_index=True, use_container_width=True)


def main() -> None:
    init()
    sidebar()
    if st.session_state.game is None:
        setup_screen()
    else:
        play_screen(st.session_state.game)


if __name__ == "__main__":
    main()
