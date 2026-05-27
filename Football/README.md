# Football Simulator Pro — Streamlit Game

A polished text-based football simulator and tournament generator built for Streamlit.

## Features

- **3 starting modes**
  1. Real Continental Tournament: Champions League, Europa League, Conference League
  2. Custom League/Tournament: league, straight knockout, or groups + knockout
  3. Quick Match: pick any two teams
- **Custom team creation** with Attack, Midfield, Defence and Star Player
- **Seeded real team database** from England, Spain, Italy, Germany, France, Portugal, USA, Saudi Arabia, Brazil and 2025/26 UEFA competitions
- **Match simulation** weighted by team ratings
- **Realistic events**: goals, assists, minutes, yellow/red cards, injuries, xG and penalties
- **Persistent active tournament state** using Streamlit session state
- **Save/load** active games as JSON
- **League tables, group tables, brackets, top scorers and top assisters**

## File structure

```text
football-simulator-pro/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
└── football_sim/
    ├── __init__.py
    ├── data.py
    ├── simulator.py
    └── tournaments.py
```

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

## Editing team ratings

Open `football_sim/data.py` and edit the `RATINGS` dictionary. Every team has:

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

The app calculates overall automatically.

## Notes

- Ratings are game-balanced estimates, not official rankings.
- The UEFA competitions are seeded from 2025/26 league-phase team lists.
- The UEFA format is implemented as league phase → knockout play-offs → round of 16 → quarter-finals → semi-finals → final.
- No paid API is required.
