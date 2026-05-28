# Mobile Results + Next Click Fix Report

## Issue found
On mobile, the match result mini-stat HTML could be displayed as raw text because Markdown treated indented generated HTML as a code block. This made the results hard to read and created horizontal scrolling.

## Fixes applied

- Changed `render_html()` so generated HTML is flattened onto a single safe line before rendering.
- Kept bright/light text styling across cards, captions, tabs, labels and tables.
- Changed mobile match stat cards to a 2-column grid instead of a long horizontal block.
- Added a clear `WHAT TO CLICK NEXT` card at the top of an active tournament.
- Added an extra `Continue` button inside the Results tab so mobile users do not need to scroll back to the top.
- Renamed simulation controls to clearer labels like `▶ Simulate matchday 2`.
- Added a short result story under every scoreline so each result has more football context.

## Tests run

```bash
python -m py_compile app.py football_sim/*.py tools/fidelity_check.py
python tools/fidelity_check.py
```

Result:

```text
FULL FIDELITY CHECK PASSED
```

The fidelity check now also verifies:

- the HTML single-line mobile render safeguard exists;
- the next-action card exists;
- the Results-tab continue button exists;
- old `DeltaGenerator` and `teams_dataframe` bugs are not present.
