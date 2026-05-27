# Streamlit UI Fix Report

This build fixes the live issue shown in the screenshot where Streamlit displayed raw `DeltaGenerator(...)` text inside the Stats tab.

## Root cause

The Stats tab used expression-level ternaries like:

```python
st.dataframe(rows, hide_index=True, use_container_width=True) if rows else st.caption("No goals yet.")
```

Streamlit can treat expression-level ternaries as displayable magic output, which can leak the returned Streamlit `DeltaGenerator` object into the app.

## Fix

The Stats tab now uses explicit `if/else` blocks:

```python
if scorer_rows:
    st.dataframe(scorer_rows, hide_index=True, use_container_width=True)
else:
    st.caption("No goals yet.")
```

## Extra UI improvements

- Brighter text variables for dark mode.
- Stronger CSS for cards, markdown text and Streamlit tables/dataframes.
- Full-fidelity test now scans `app.py` for expression-level ternaries that could leak Streamlit objects.

## Test command

Run from the repo root:

```bash
python tools/fidelity_check.py
```

Expected result:

```text
FULL FIDELITY CHECK PASSED
```
