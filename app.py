from __future__ import annotations

import json
import time
from copy import deepcopy
from html import escape
from textwrap import dedent
from typing import List

import streamlit as st

from football_sim.data import CONTINENTAL, DOMESTIC, INTERNATIONAL, TEAMS
from football_sim.simulator import dumps_state, loads_state, sorted_table, top_list, simulate_match
from football_sim.tournaments import (
    create_cup,
    create_knockout,
    create_league,
    create_uefa_tournament,
    create_international_tournament,
    create_premier_league,
    create_fa_cup,
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


.team-chip {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    min-width: 0;
}
.crest {
    width: 30px;
    height: 30px;
    border-radius: 10px 10px 13px 13px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: .72rem;
    font-weight: 950;
    border: 1px solid rgba(255,255,255,.28);
    box-shadow: inset 0 -8px 12px rgba(0,0,0,.15), 0 6px 18px rgba(0,0,0,.22);
    flex: 0 0 auto;
}
.team-name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.live-card {
    background: linear-gradient(135deg, rgba(250,204,21,.14), rgba(34,197,94,.12)), rgba(15,23,42,.94);
    border: 1px solid rgba(250,204,21,.30);
    border-radius: 22px;
    padding: 1rem;
    margin: .85rem 0;
    box-shadow: 0 16px 52px rgba(0,0,0,.30);
}
.live-minute { color: #fef08a !important; font-weight: 950; font-size: .92rem; }
.live-event { color: #ffffff !important; font-weight: 850; font-size: 1.05rem; margin: .22rem 0 .45rem; }
.score-strip {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: .45rem;
    margin-top: .7rem;
}
.score-tile {
    border: 1px solid rgba(148,163,184,.22);
    background: rgba(2,6,23,.48);
    border-radius: 14px;
    padding: .48rem .55rem;
    color: #f8fafc !important;
    font-weight: 850;
    font-size: .88rem;
}
.mobile-action-bar {
    position: sticky;
    bottom: .35rem;
    z-index: 10;
    background: rgba(2,6,23,.92);
    border: 1px solid rgba(56,189,248,.28);
    border-radius: 20px;
    padding: .72rem;
    margin: .85rem 0;
    box-shadow: 0 18px 58px rgba(0,0,0,.42);
    backdrop-filter: blur(10px);
}
.mobile-action-bar b { color: #ffffff !important; }
.mobile-action-bar span { color: #e2e8f0 !important; }
.stButton>button,
.stDownloadButton>button,
button[kind="secondary"],
button[kind="primary"] {
    background: linear-gradient(135deg, rgba(15,23,42,.96), rgba(30,41,59,.94)) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(148,163,184,.32) !important;
}
.stButton>button:hover,
.stButton>button:focus,
.stButton>button:active,
.stDownloadButton>button:hover,
.stDownloadButton>button:focus,
.stDownloadButton>button:active {
    background: linear-gradient(135deg, #16a34a, #0ea5e9) !important;
    color: #ffffff !important;
    border-color: rgba(255,255,255,.26) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,.22) !important;
}
.stButton>button[kind="primary"], button[kind="primary"] {
    background: linear-gradient(135deg, #16a34a, #0ea5e9) !important;
    color: #ffffff !important;
    border: 0 !important;
}
div[data-baseweb="select"] > div,
div[data-baseweb="select"] input,
div[data-baseweb="select"] span,
div[data-baseweb="popover"],
div[role="listbox"],
div[role="option"],
ul[role="listbox"] li {
    background-color: #0f172a !important;
    color: #f8fafc !important;
}
div[role="option"]:hover,
ul[role="listbox"] li:hover {
    background-color: #1e293b !important;
    color: #ffffff !important;
}
.stRadio div[role="radiogroup"] label,
.stRadio div[role="radiogroup"] span {
    color: #f8fafc !important;
}


.watch-panel {
    background: linear-gradient(135deg, rgba(56,189,248,.14), rgba(34,197,94,.12)), rgba(15,23,42,.92);
    border: 1px solid rgba(56,189,248,.30);
    border-radius: 22px;
    padding: 1rem;
    margin: .8rem 0;
    box-shadow: 0 12px 42px rgba(0,0,0,.24);
}
.watch-panel h3 { margin: .1rem 0 .25rem; color: #ffffff !important; line-height: 1.12; }
.watch-panel p { color: #e2e8f0 !important; margin: 0; }
.fixture-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
}
.fixture-readable {
    min-height: 138px;
    padding: 1rem;
}
.fixture-row {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: .75rem;
    align-items: center;
    padding: .35rem 0;
}
.fixture-row.away-row {
    border-top: 1px solid rgba(148,163,184,.13);
    margin-top: .25rem;
    padding-top: .55rem;
}
.fixture-side {
    font-size: .74rem;
    font-weight: 900;
    letter-spacing: .04em;
    text-transform: uppercase;
    color: #bae6fd !important;
    background: rgba(56,189,248,.12);
    border: 1px solid rgba(56,189,248,.22);
    padding: .18rem .45rem;
    border-radius: 999px;
    white-space: nowrap;
}
.fixture-separator {
    width: 34px;
    height: 25px;
    margin: .12rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    color: #ffffff !important;
    background: rgba(56,189,248,.16);
    border: 1px solid rgba(56,189,248,.24);
    font-size: .76rem;
    font-weight: 950;
}
.fixture-meta { margin-top: .3rem; }
.team-chip {
    max-width: 100%;
    font-size: .98rem;
    line-height: 1.18;
}
.team-name {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    word-break: normal;
}
.result-readable {
    padding: 1.05rem;
}
.result-score-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
    gap: .75rem;
    align-items: center;
    margin-bottom: .65rem;
}
.result-team {
    min-width: 0;
}
.result-team .team-chip {
    width: 100%;
    font-size: 1.05rem;
    font-weight: 950;
}
.away-result .team-chip {
    justify-content: flex-end;
    text-align: right;
}
.big-score {
    color: #ffffff !important;
    font-size: clamp(2rem, 10vw, 3.1rem);
    line-height: .95;
    font-weight: 1000;
    letter-spacing: -.05em;
    white-space: nowrap;
    text-shadow: 0 10px 32px rgba(56,189,248,.18);
}
.result-pills { margin: .45rem 0 .2rem; }
.live-stage {
    position: relative;
    padding: 1rem;
}
.match-clock {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    gap: .75rem;
    align-items: center;
    margin-bottom: .8rem;
}
.match-clock strong {
    color: #fef08a !important;
    font-size: 1.45rem;
    line-height: 1;
    display: block;
}
.match-clock span {
    display: block;
    color: #e2e8f0 !important;
    font-size: .78rem;
    font-weight: 800;
}
.clock-track {
    height: 12px;
    width: 100%;
    background: rgba(15,23,42,.82);
    border: 1px solid rgba(148,163,184,.25);
    border-radius: 999px;
    overflow: hidden;
}
.clock-fill {
    height: 100%;
    background: linear-gradient(90deg, #22c55e, #38bdf8, #facc15);
    border-radius: 999px;
    transition: width .45s ease;
}
.live-event-big {
    display: flex;
    gap: .55rem;
    align-items: flex-start;
    color: #ffffff !important;
    font-size: clamp(1.05rem, 4.8vw, 1.35rem);
    font-weight: 950;
    line-height: 1.2;
    background: rgba(2,6,23,.40);
    border: 1px solid rgba(148,163,184,.18);
    border-radius: 16px;
    padding: .75rem;
}
.live-event-big span {
    flex: 0 0 auto;
}
.recent-events {
    margin-top: .75rem;
    border-top: 1px solid rgba(148,163,184,.16);
    padding-top: .65rem;
}
.recent-events b {
    display: block;
    color: #ffffff !important;
    margin-bottom: .35rem;
}
.recent-line {
    color: #e2e8f0 !important;
    font-size: .9rem;
    line-height: 1.25;
    padding: .18rem 0;
}
.recent-line span {
    color: #fef08a !important;
    font-weight: 950;
    margin-right: .35rem;
}
.score-strip {
    grid-template-columns: repeat(3, minmax(0, 1fr));
}
.score-tile {
    font-size: .82rem;
    line-height: 1.2;
}
.score-tile strong {
    display: inline-block;
    color: #ffffff !important;
    font-size: 1.22rem;
    margin: .2rem 0;
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
    .fixture-grid { grid-template-columns: 1fr !important; }
    .fixture-readable { min-height: auto; padding: .95rem; }
    .team-chip { font-size: 1rem; }
    .crest { width: 34px; height: 34px; font-size: .74rem; }
    .result-score-grid { grid-template-columns: 1fr; text-align: left; gap: .45rem; }
    .away-result .team-chip { justify-content: flex-start !important; text-align: left !important; }
    .big-score { font-size: 3rem; text-align: left; padding: .25rem 0; }
    .score-strip { grid-template-columns: 1fr; }
    .score-tile { font-size: .92rem; }
    .match-clock { grid-template-columns: 1fr; gap: .45rem; }
    .mobile-action-bar { bottom: .2rem; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def h(value: object) -> str:
    """Escape dynamic values before inserting them into unsafe HTML blocks."""
    return escape(str(value), quote=True)


def compact_markup(markup: str) -> str:
    """Flatten custom HTML so Streamlit/Markdown never treats indented tags as code."""
    return " ".join(line.strip() for line in dedent(markup).strip().splitlines())


def render_html(markup: str) -> None:
    """Render custom HTML safely without Markdown turning indented tags into code blocks."""
    st.markdown(compact_markup(markup), unsafe_allow_html=True)


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
        st.session_state.start_mode = "🏴 Domestic Cups/Leagues"
    if "show_inline_results" not in st.session_state:
        st.session_state.show_inline_results = False
    if "last_watch_teams" not in st.session_state:
        st.session_state.last_watch_teams = []


def hero() -> None:
    render_html(
        """
        <div class="hero">
            <h1>⚽ Football Simulator Pro</h1>
            <p>
            A mobile-first text football universe. Create teams, run the Premier League, FA Cup, World Cups, EUROs, leagues, cups and European club tournaments,
            then simulate one matchday or knockout round at a time with stat-weighted winners, real-player scorers,
            late-drama upsets, live 60-second play mode, assists, detailed match stats, injuries, tables and trophy celebrations.
            </p>
            <span class="pill">📱 Mobile-first</span>
            <span class="pill info-pill">One command at a time</span>
            <span class="pill">Real-player squads</span>
            <span class="pill gold-pill">Trophy winner graphic</span>
            <span class="pill info-pill">🎬 Watch Live mode</span>
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
            "Flag": t.get("flag", ""),
            "Team": t.get("name"),
            "Badge": t.get("abbr", ""),
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


def team_chip_html(team_name: str, align: str = "left") -> str:
    team = st.session_state.team_db.get(team_name, {})
    flag = team.get("flag", "🏳️")
    abbr = team.get("abbr", team_name[:3].upper())
    primary = team.get("crest_primary", "#334155")
    secondary = team.get("crest_secondary", "#f8fafc")
    name = h(team_name)
    if align == "right":
        return (
            f"<span class='team-chip' style='justify-content:flex-end'>"
            f"<span class='team-name'>{name}</span><span>{h(flag)}</span>"
            f"<span class='crest' style='background:{h(primary)};color:{h(secondary)}'>{h(abbr)}</span></span>"
        )
    return (
        f"<span class='team-chip'><span class='crest' style='background:{h(primary)};color:{h(secondary)}'>{h(abbr)}</span>"
        f"<span>{h(flag)}</span><span class='team-name'>{name}</span></span>"
    )


def fixture_cards(fixtures: List[dict], title: str | None = None, limit: int = 12) -> None:
    if not fixtures:
        st.info("No fixtures waiting.")
        return
    if title:
        st.markdown(title)

    cards: List[str] = []
    for match in fixtures[:limit]:
        group = match.get("group")
        group_html = f"<span class='pill info-pill'>Group {h(group)}</span>" if group else ""
        cards.append(
            "<div class='fixture-card fixture-readable'>"
            f"<div class='fixture-row'><div>{team_chip_html(match['home'])}</div><span class='fixture-side'>Home</span></div>"
            "<div class='fixture-separator'>v</div>"
            f"<div class='fixture-row away-row'><div>{team_chip_html(match['away'])}</div><span class='fixture-side'>Away</span></div>"
            f"<div class='fixture-meta'>{group_html}</div>"
            "</div>"
        )

    render_html("<div class='fixture-grid'>" + "".join(cards) + "</div>")
    if len(fixtures) > limit:
        st.caption(f"Showing {limit} of {len(fixtures)} fixtures. Full fixture table is below.")
        st.dataframe(
            [{"Home": m["home"], "Away": m["away"], "Group": m.get("group", "—")} for m in fixtures],
            hide_index=True,
            use_container_width=True,
        )


def watch_selector_panel(fixtures: List[dict], key_prefix: str) -> List[str]:
    """Mobile-friendly selector for 1-3 teams to focus the live broadcast."""
    if not fixtures:
        return []
    options: List[str] = []
    for match in fixtures:
        for name in (match["home"], match["away"]):
            if name not in options:
                options.append(name)
    default = st.session_state.get(f"{key_prefix}_watch_defaults")
    if not default:
        default = [fixtures[0]["home"]]
        st.session_state[f"{key_prefix}_watch_defaults"] = default
    selected = st.multiselect(
        "Pick 1, 2 or 3 teams to watch live",
        options,
        default=[name for name in default if name in options][:3],
        key=f"{key_prefix}_watch_teams",
        help="Watch Live focuses on these teams so the phone screen is easier to follow. The other fixtures are still simulated and shown after.",
    )
    if len(selected) > 3:
        st.warning("Watch mode is limited to 3 teams so the live feed stays readable. I’ll use the first 3 you selected.")
        selected = selected[:3]
    watched = [m for m in fixtures if m["home"] in selected or m["away"] in selected]
    if selected:
        render_html(
            "<div class='watch-panel'>"
            "<span class='next-label'>WATCH FOCUS</span>"
            f"<h3>{h(', '.join(selected))}</h3>"
            "<p>🎬 Watch Live will follow these teams first. Full matchday results appear after the live feed.</p>"
            "</div>"
        )
        fixture_cards(watched[:3], title="#### Watched fixtures", limit=3)
    else:
        st.info("Pick at least one team for Watch Live, or use Quick Sim for the whole matchday.")
    return selected


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


def _score_tiles(scores: dict, results: List[dict], limit: int = 6) -> str:
    tiles = []
    for r in results[:limit]:
        sc = scores.get(r["id"], {"home": 0, "away": 0})
        tiles.append(
            f"<div class='score-tile'>{team_chip_html(r['home'])}<br><strong>{sc['home']}–{sc['away']}</strong><br>{team_chip_html(r['away'])}</div>"
        )
    return "<div class='score-strip'>" + "".join(tiles) + "</div>"


def _live_feed(results: List[dict]) -> List[dict]:
    feed: List[dict] = []
    for r in results:
        feed.append({"minute": 0, "result_id": r["id"], "text": f"Kick-off: {r['home']} v {r['away']}", "type": "kickoff"})
        for ev in r.get("timeline", []):
            feed.append({"minute": int(ev.get("minute", 0)), "result_id": r["id"], "text": ev.get("text", ""), "type": ev.get("type", "event"), "team": ev.get("team")})
        feed.append({"minute": 45, "result_id": r["id"], "text": f"Half-time: {r['home']} v {r['away']}", "type": "half_time"})
        feed.append({"minute": 96, "result_id": r["id"], "text": f"Full-time: {r['home']} {r['home_goals']}–{r['away_goals']} {r['away']}", "type": "full_time"})
    return sorted(feed, key=lambda e: (e["minute"], e["result_id"], e["text"]))


def _focus_results(results: List[dict], watch_teams: List[str] | None = None) -> List[dict]:
    if not watch_teams:
        return results[:3]
    focused = [r for r in results if r["home"] in watch_teams or r["away"] in watch_teams]
    return focused[:3] if focused else results[:3]


def _ordered_results(results: List[dict], watch_teams: List[str] | None = None) -> List[dict]:
    if not watch_teams:
        return results
    focused = [r for r in results if r["home"] in watch_teams or r["away"] in watch_teams]
    rest = [r for r in results if r not in focused]
    return focused + rest


def _event_icon(event_type: str) -> str:
    return {
        "goal": "⚽",
        "save": "🧤",
        "chance": "🔥",
        "pressure": "🚩",
        "control": "🎛️",
        "late": "⏳",
        "card": "🟨",
        "injury": "🚑",
        "full_time": "✅",
        "half_time": "☕",
        "kickoff": "▶️",
        "penalties": "🥅",
        "extra_time": "⏱️",
    }.get(event_type, "•")


def live_broadcast(results: List[dict], seconds: int = 60, watch_teams: List[str] | None = None) -> None:
    if not results:
        st.info("No live events to show.")
        return
    focused_results = _focus_results(results, watch_teams)
    watch_label = ", ".join(watch_teams or []) if watch_teams else "featured matches"
    st.markdown("### 🎬 Live match centre")
    st.caption(f"Watching {watch_label}. The rest of the matchday is simulated quietly and shown after the live feed.")

    stage = st.empty()
    progress = st.progress(0)
    feed = _live_feed(focused_results)
    scores = {r["id"]: {"home": 0, "away": 0} for r in focused_results}
    result_lookup = {r["id"]: r for r in focused_results}
    recent: List[str] = []
    delay = max(0.55, min(2.8, seconds / max(1, len(feed))))

    for idx, ev in enumerate(feed, start=1):
        r = result_lookup[ev["result_id"]]
        if ev.get("type") == "goal":
            if ev.get("team") == r["home"]:
                scores[r["id"]]["home"] += 1
            elif ev.get("team") == r["away"]:
                scores[r["id"]]["away"] += 1
        minute = ev.get("minute", 0)
        label = "90+" + str(minute - 90) if 91 <= minute <= 99 else ("FT" if minute >= 96 else str(minute) + "'")
        clock_pct = min(100, max(0, int(minute / 96 * 100)))
        icon = _event_icon(ev.get("type", "event"))
        event_line = f"<div class='recent-line'><span>{h(label)}</span> {h(ev['text'])}</div>"
        recent.append(event_line)
        recent_html = "".join(recent[-5:])
        stage.markdown(
            compact_markup(
                f"""
                <div class='live-card live-stage'>
                    <div class='match-clock'>
                        <div><strong>{h(label)}</strong><span>Match clock</span></div>
                        <div class='clock-track'><div class='clock-fill' style='width:{clock_pct}%'></div></div>
                    </div>
                    <div class='live-event-big'><span>{h(icon)}</span>{h(ev['text'])}</div>
                    {_score_tiles(scores, focused_results, limit=3)}
                    <div class='recent-events'><b>Latest movements</b>{recent_html}</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )
        progress.progress(min(100, int(idx / len(feed) * 100)))
        if idx < len(feed):
            time.sleep(delay)
    st.success("Live simulation complete. Watched results are below, followed by the rest of the matchday.")


def play_next(game: dict, live: bool, key_note: str = "", watch_teams: List[str] | None = None) -> None:
    if game.get("stage") == "league":
        new_game, results = simulate_matchday(game, st.session_state.team_db)
    elif game.get("stage") == "knockout":
        new_game, results = simulate_knockout_round(game, st.session_state.team_db)
    else:
        return
    st.session_state.last_watch_teams = watch_teams or []
    if live:
        live_broadcast(results, seconds=60, watch_teams=watch_teams)
        st.session_state.game = new_game
        st.session_state.last_results = results
        st.session_state.show_inline_results = True
        show_results(results, focus_teams=watch_teams)
        st.info("Tables/brackets are updated in the saved state. Tap any tab or Refresh after live mode to redraw the full page.")
        if st.button("🔄 Refresh updated tables", key=f"refresh_after_live_{key_note}"):
            st.rerun()
    else:
        st.session_state.game = new_game
        st.session_state.last_results = results
        st.session_state.show_inline_results = True
        st.rerun()


def action_buttons(game: dict, key_prefix: str, sticky: bool = False, watch_teams: List[str] | None = None) -> None:
    if game.get("stage") not in ("league", "knockout"):
        return
    if sticky:
        render_html("<div class='mobile-action-bar'><b>Bottom menu</b><br><span>Watch selected teams, quick sim the next stage, or show result cards.</span></div>")
    c1, c2, c3 = st.columns(3)
    with c1:
        live_label = "🎬 Watch selected" if watch_teams else "🎬 Watch Live"
        if st.button(live_label, type="primary", key=f"{key_prefix}_watch_live"):
            play_next(game, live=True, key_note=key_prefix, watch_teams=watch_teams)
    with c2:
        label = "⚡ Quick Sim"
        if game.get("stage") == "league":
            label = f"⚡ Matchday {game.get('matchday_index', 0) + 1}"
        elif game.get("stage") == "knockout":
            label = "⚡ Round"
        if st.button(label, key=f"{key_prefix}_quick_sim"):
            play_next(game, live=False, key_note=key_prefix, watch_teams=watch_teams)
    with c3:
        if st.button("📋 Show Results", key=f"{key_prefix}_show_results"):
            st.session_state.show_inline_results = True



def next_action_panel(game: dict, context: str = "top") -> None:
    stage = game.get("stage")
    if stage == "league":
        title = f"Next: simulate matchday {game.get('matchday_index', 0) + 1}"
        body = "Use 🎬 Watch Live for a 60-second event feed, or ⚡ Quick Sim for instant results. The game pauses again after this matchday."
    elif stage == "knockout":
        current = game.get("knockout_rounds", [{}])[-1].get("name", "knockout round")
        title = f"Next: simulate {current}"
        body = "Use 🎬 Watch Live for a dramatic round reveal, or ⚡ Quick Sim for instant results. The game pauses before the next round."
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
    # Backwards-compatible wrapper used by older UI locations/tests.
    action_buttons(game, key_prefix=key, watch_teams=st.session_state.get("last_watch_teams", []))


def show_results(results: List[dict], focus_teams: List[str] | None = None) -> None:
    if not results:
        st.info("No results yet. Simulate the next matchday or round when you are ready.")
        return
    ordered = _ordered_results(results, focus_teams)
    for idx, r in enumerate(ordered):
        focused = bool(focus_teams and (r["home"] in focus_teams or r["away"] in focus_teams))
        focus_badge = "<span class='pill gold-pill'>Watched game</span>" if focused else ""
        winner = f"<span class='pill gold-pill'>Winner: {h(r['winner'])}</span>" if r.get("winner") else ""
        penalties = ""
        if r.get("penalties"):
            penalties = f"<span class='pill info-pill'>Pens {r['penalties']['home']}–{r['penalties']['away']}</span>"
        summary = match_summary_html(r)
        render_html(
            f"""
            <div class="result-card result-readable">
                <div class="result-score-grid">
                    <div class="result-team">{team_chip_html(r['home'])}</div>
                    <div class="big-score">{h(r['home_goals'])}–{h(r['away_goals'])}</div>
                    <div class="result-team away-result">{team_chip_html(r['away'], align='right')}</div>
                </div>
                <div class="result-pills">
                    {focus_badge}
                    <span class="pill info-pill">xG {r['home_xg']}–{r['away_xg']}</span>
                    <span class="pill info-pill">Power {r.get('home_power', '—')}–{r.get('away_power', '—')}</span>
                    <span class="pill">{h(r['played_at'])}</span>
                    {winner}{penalties}
                </div>
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


def setup_domestic() -> None:
    st.markdown("## 🏴 Domestic Cups/Leagues")
    competition = st.selectbox("Choose domestic competition", list(DOMESTIC.keys()))
    cfg = DOMESTIC[competition]
    st.caption(cfg.get("format_note", "Domestic competition."))
    preview = get_teams_by_names(cfg["teams"])
    with st.expander("Preview teams, flags, ratings and badge initials", expanded=True):
        st.dataframe(teams_table_rows(preview), hide_index=True, use_container_width=True)
    with st.expander("Preview player cores"):
        show_squad_browser(preview)
    if st.button(f"Create {competition}", type="primary"):
        if competition == "Premier League":
            st.session_state.game = create_premier_league()
        else:
            st.session_state.game = create_fa_cup()
        st.session_state.last_results = []
        st.session_state.show_inline_results = False
        st.success(f"Created {competition}. Use Watch Live or Quick Sim one stage at a time.")
        st.rerun()


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
    c1, c2 = st.columns(2)
    with c1:
        quick_clicked = st.button("⚡ Simulate quick match", type="primary")
    with c2:
        live_clicked = st.button("🎬 Watch quick match live")
    if quick_clicked or live_clicked:
        if home == away:
            st.error("Pick two different teams.")
        else:
            result = simulate_match(st.session_state.team_db[home], st.session_state.team_db[away], knockout=knockout)
            st.session_state.quick_match_result = result
            if live_clicked:
                live_broadcast([result], seconds=60)
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
            <div class="mode-card"><h3>🏴 Domestic Cups/Leagues</h3><p>Premier League season or FA Cup knockout with flags, generated crest badges and player cores.</p></div>
            <div class="mode-card"><h3>🌍 World Cup / EURO</h3><p>International tournaments with national team ratings and real-player squad cores.</p></div>
            <div class="mode-card"><h3>🏆 Real Continental</h3><p>Champions League, Europa League or Conference League.</p></div>
            <div class="mode-card"><h3>🛠️ Custom Competition</h3><p>Create leagues, cups and knockout brackets with real, national or fictional teams.</p></div>
            <div class="mode-card"><h3>⚡ Quick Match</h3><p>Pick any two teams for an instant or live 60-second simulation.</p></div>
        </div>
        """
    )
    mode = st.radio(
        "Start mode",
        ["🏴 Domestic Cups/Leagues", "🌍 World Cup / EURO", "🏆 Real Continental Tournament", "🛠️ Custom League/Tournament", "⚡ Quick Match"],
        key="start_mode",
        label_visibility="collapsed",
    )
    if mode.startswith("🏴"):
        setup_domestic()
    elif mode.startswith("🌍"):
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
    active_watch_teams: List[str] = []

    if game["stage"] == "league":
        st.markdown(f"### Upcoming Matchday {game['matchday_index'] + 1}")
        fixtures = upcoming_matches(game)
        watch_teams = watch_selector_panel(fixtures, key_prefix="league")
        active_watch_teams = watch_teams
        fixture_cards(fixtures, title="#### Full matchday fixtures")
        action_buttons(game, key_prefix="top_next_matchday", watch_teams=watch_teams)
        st.caption("Watch Live focuses on your selected teams for about 60 seconds. Quick Sim instantly simulates the full matchday. Neither option runs ahead without another tap.")
        if st.session_state.get("show_inline_results") and st.session_state.last_results:
            st.markdown("### Latest results")
            show_results(st.session_state.last_results, focus_teams=st.session_state.get("last_watch_teams", []))

    elif game["stage"] == "knockout":
        current = game["knockout_rounds"][-1]
        st.markdown(f"### Upcoming {current['name']}")
        fixtures = upcoming_matches(game)
        watch_teams = watch_selector_panel(fixtures, key_prefix="knockout")
        active_watch_teams = watch_teams
        fixture_cards(fixtures, title="#### Full round fixtures")
        action_buttons(game, key_prefix="top_next_knockout", watch_teams=watch_teams)
        st.caption("Watch Live focuses on your selected teams dramatically. Quick Sim is instant. The app pauses again before the next round.")
        if st.session_state.get("show_inline_results") and st.session_state.last_results:
            st.markdown("### Latest results")
            show_results(st.session_state.last_results, focus_teams=st.session_state.get("last_watch_teams", []))

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
        show_results(st.session_state.last_results or game.get("history", [])[-12:], focus_teams=st.session_state.get("last_watch_teams", []))
        if game.get("stage") in ("league", "knockout"):
            st.markdown("### Continue")
            st.caption("You can continue from here on mobile, so you do not need to scroll back to the top.")
            action_buttons(game, key_prefix="results_continue", watch_teams=active_watch_teams)
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
            - The domestic modes add Premier League and FA Cup, with generated shield badges instead of official crests.
            - Watch Live mode takes about 60 seconds and reveals events one at a time.
            """
        )

    if game.get("stage") in ("league", "knockout"):
        st.markdown("---")
        action_buttons(game, key_prefix="bottom_menu", sticky=True, watch_teams=active_watch_teams)
        if st.session_state.get("show_inline_results") and st.session_state.last_results:
            st.markdown("### Latest results")
            show_results(st.session_state.last_results, focus_teams=st.session_state.get("last_watch_teams", []))


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
