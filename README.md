# Bonifacic Meal Plan App

Weekly meal plan viewer for the Bonifacic household, powered by Google Sheets.

## Features

- Login with username/password
- View the full weekly meal plan from Google Sheets
- Today and tomorrow are highlighted
- Angela can add notes/suggestions to any meal (saved to the Notes column)
- Mobile-friendly (Bootstrap 5)

## Deploy to Render.com

1. Push this repo to GitHub (make sure `google_creds.json` is in `.gitignore`).

2. On [Render](https://render.com), create a **New Web Service** and connect your repo.

3. Configure the service:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`

4. Add environment variables:
   - `SECRET_KEY` — a random secret string for Flask sessions
   - `PORT` — Render sets this automatically

5. Upload `google_creds.json` as a **Secret File** at path `/etc/secrets/google_creds.json`, then set the start command to copy it before boot:
   ```
   cp /etc/secrets/google_creds.json google_creds.json && gunicorn app:app --bind 0.0.0.0:$PORT
   ```

6. Deploy. The app will be live at your Render URL.

## Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 and log in.
