# Football Simulator Pro — Streamlit Game

A polished, mobile-first text-based football simulator and tournament generator built for Streamlit.

## Features

- **4 starting modes**
  1. World Cup / EURO: international tournaments with national team ratings and real-player squad cores
  2. Real Continental Tournament: Champions League, Europa League, Conference League
  3. Custom League/Tournament: league, straight knockout, or groups + knockout
  4. Quick Match: pick any two club or national teams
- **World Cup 2026-style mode**: 48 teams, 12 groups of four, top two plus eight best third-placed teams qualify for the Round of 32
- **EURO / European Championship mode**: 24 teams, six groups of four, top two plus four best third-placed teams qualify for the Round of 16
- **Real-player squad cores** for national teams, with editable player positions and rating estimates
- **Custom team creation** with Attack, Midfield, Defence and Star Player
- **Seeded real club database** from England, Spain, Italy, Germany, France, Portugal, USA, Saudi Arabia, Brazil and 2025/26 UEFA competitions
- **Stat-weighted match simulation** using Attack, Midfield, Defence, Overall, player positions, player ratings and home/neutral advantage
- **Realistic events**: goals, assists, minutes, yellow/red cards, injuries, xG, extra time and penalties
- **Mobile-first interface** with stacked fixture cards, large buttons, collapsed sidebar and responsive spacing
- **Built-in player instructions** on the setup screen, Help tab and sidebar
- **Winner trophy graphic** with animated CSS confetti when a champion is crowned
- **Persistent active tournament state** using Streamlit session state
- **Save/load** active games as JSON
- **League tables, group tables, best third-place qualifiers, brackets, top scorers and top assisters**

## File structure

```text
football-simulator-pro/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
├── assets/
│   └── winner-trophy.svg
├── docs/
│   ├── INSTRUCTIONS.md
│   └── MOBILE_UX_NOTES.md
└── football_sim/
    ├── __init__.py
    ├── data.py
    ├── simulator.py
    └── tournaments.py
```

## How to play

1. Open the app.
2. Choose a starting mode: World Cup / EURO, Real Continental Tournament, Custom League/Tournament, or Quick Match.
3. Press one simulation button at a time. The game never auto-simulates ahead.
4. Review Results, Tables, Bracket, Stats and Teams after each matchday or knockout round.
5. In international modes, open the Teams tab to view the real-player squad cores and player rating estimates.
6. When the tournament finishes, the champion screen shows a trophy graphic and animated confetti.
7. Use the Save tab to download or reload an active universe.

See `docs/INSTRUCTIONS.md` for the full player guide.

## Mobile-first UX

The app is designed to work well on phones:

- Sidebar starts collapsed.
- Important actions are full-width buttons.
- Fixtures are shown as cards before dense tables.
- Tabs stay short and scroll cleanly on narrow screens.
- The winner screen uses CSS/HTML, so no paid image API is required.

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Create a new GitHub repository.
2. Upload all files from this folder.
3. Go to Streamlit Community Cloud.
4. Select the repo.
5. Set the main file path to:

```text
app.py
```

6. Deploy.

## Editing team and player ratings

Open `football_sim/data.py`.

Club/custom-style teams use the `RATINGS` dictionary:

```python
"Team Name": {
    "country": "England",
    "league": "Premier League",
    "attack": 90,
    "midfield": 88,
    "defence": 86,
    "star_player": "Star Name",
}
```

National teams use:

- `NATIONAL_RATINGS` for team Attack, Midfield and Defence
- `NATIONAL_SQUADS` for real-player squad cores and player ratings
- `WORLD_CUP_2026_TEAMS` and `EURO_2024_TEAMS` for tournament pools
- `INTERNATIONAL` for group/qualification rules

The app calculates overall automatically.

## Notes

- Ratings are game-balanced estimates, not official rankings or official player-rating data.
- National team squads are representative real-player cores and are easy to edit as final squads change.
- The World Cup mode uses the 48-team modern format but randomises the group draw each time for replayability.
- The UEFA club competitions are seeded from 2025/26 league-phase team lists.
- The UEFA club format is implemented as league phase → knockout play-offs → round of 16 → quarter-finals → semi-finals → final.
- No paid API is required.
