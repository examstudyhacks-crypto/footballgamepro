# No requirements deploy fix

This version intentionally has **no `requirements.txt`**.

Why: Streamlit Community Cloud already includes Streamlit and its direct dependencies in the default environment. The app now imports only:

- Python built-ins
- `streamlit`
- local `football_sim` modules

This avoids Python/pandas/numpy build failures during the `Installing requirements` step.

## Deploy steps

1. Upload these files to the root of your GitHub repo.
2. Delete any old `requirements.txt`, `uv.lock`, `Pipfile`, `environment.yml`, or `pyproject.toml` from the repo.
3. In Streamlit Cloud set the main file to `app.py`.
4. In App settings, clear cache/reboot or redeploy.
5. If Streamlit asks for Python version, choose Python 3.12 or 3.11.

If you still see "Error installing requirements", your GitHub repo probably still has an old dependency file somewhere. Search the repo for `requirements.txt`, `uv.lock`, `Pipfile`, `environment.yml`, and `pyproject.toml` and remove them.
