# Streamlit Cloud deployment fix

If Streamlit says **error installing requirements**, use this fixed repo version.

## What changed

The previous `requirements.txt` used open-ended versions:

```txt
streamlit>=1.35
pandas>=2.2
```

That lets Streamlit Cloud pull the newest package versions available at deploy time. If a newer Python/package combination is not available or has a dependency conflict, the build can fail.

This version pins stable versions:

```txt
streamlit==1.41.1
pandas==2.2.3
numpy==2.2.6
```

## Recommended Streamlit Cloud settings

When deploying:

1. Main file path: `app.py`
2. Python version: `3.12` if Streamlit gives you the option in **Advanced settings**
3. Make sure `requirements.txt` is either:
   - in the repository root, or
   - in the same folder as `app.py`

Streamlit Community Cloud looks for dependency files in the app entrypoint directory first, then the repository root.

## If you already deployed with the wrong Python version

Streamlit may not let you change Python version after deployment. The clean fix is usually:

1. Delete the failed app from Streamlit Community Cloud.
2. Redeploy it from the GitHub repo.
3. In Advanced settings, choose Python 3.12.
4. Use `app.py` as the entrypoint.

## Local test

Run locally with:

```bash
pip install -r requirements.txt
streamlit run app.py
```
