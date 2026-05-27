# Streamlit Cloud install fix

This package removes `requirements.txt` completely and removes the app's direct `pandas` import.

The app only needs Streamlit plus Python built-ins. Streamlit Community Cloud includes Streamlit by default, so there is nothing extra to install.

## Very important

When replacing your GitHub repo, delete the old `requirements.txt` file. Do not leave it in GitHub, because Streamlit Cloud will still try to install it.

Also delete these if they exist:

- `uv.lock`
- `Pipfile`
- `environment.yml`
- `pyproject.toml`

Then redeploy with main file:

```text
app.py
```

If Streamlit Cloud still shows "Error installing requirements", open **Manage app → Logs** and check which dependency file it found. The file named there must be removed or simplified.
