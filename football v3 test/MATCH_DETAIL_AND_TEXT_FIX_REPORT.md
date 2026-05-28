# Match Detail + Text Contrast Fix Report

## What changed

### Brighter text
- Confirmed the app uses bright white/near-white text on the dark mobile UI.
- Added extra CSS coverage for captions, tab labels, form labels and match-stat cards.
- Result-card text and mini-stat text now use high-contrast values with `!important` safeguards.

### Fewer yellow cards
- Replaced the old `random.randint(0, 4)` card model per team.
- New lower-noise model averages roughly 1.5–2.0 total cards per match instead of constant card-heavy timelines.
- Red cards are now deliberately rare.

### More football detail
Each simulated match now includes a box-score style match detail model:

- Possession
- Shots
- Shots on target
- Big chances
- Corners
- Fouls
- Pass accuracy
- Keeper saves

The results screen now shows a quick mobile-friendly stat card under each scoreline, and the match expander includes a full match-stats table plus timeline.

### Better timelines
The timeline now includes more football action, such as:

- Goalkeeper saves
- Big chances
- Corner pressure
- Midfield control
- Late pressure
- Goals, assists, rare cards and injuries

## Test result

```text
FULL FIDELITY CHECK PASSED
Quick match, league, cup, knockout, save/load, lower-card model, detailed match stats and HTML source checks passed.
```
