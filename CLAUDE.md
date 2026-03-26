# meal-plan-app

## Project Overview
Flask app for managing weekly meal plans via Google Sheets integration. Authenticates users (DJ + Angela) and provides web UI to view and edit shared meal planning spreadsheet in real time.

## Tech Stack
- **Backend**: Python 3, Flask
- **Auth**: Username/password (credentials via environment)
- **Google Sheets**: gspread library, service account JSON credentials
- **Frontend**: Jinja2 templates, HTML/CSS forms
- **Deployment**: Gunicorn, render.yaml for Render.com

## Architecture
- app.py — Flask application, login/logout routes, meal plan display/edit
- get_sheet function — Fetches Google Sheets credentials from env or google_creds.json file
- templates/ — Jinja2 templates for login, meal plan views
- static/ — CSS, images, client-side JS
- Procfile — Defines web dyno for Render
- Data flow: User login → fetch Google Sheet via gspread → render in template → POST edits back to Sheet

## Build & Test Commands
Install deps: pip install -r requirements.txt
Run dev server: flask run
Run with gunicorn: gunicorn app:app
Test credentials: python app.py

## Coding Rules
- ALWAYS use full file replacements, never incremental edits
- Security-first: credentials via GOOGLE_CREDS_JSON env var or .gitignored google_creds.json file
- User credentials (DJ_USERNAME, DJ_PASSWORD, ANGELA_USERNAME, ANGELA_PASSWORD) in environment
- All meal plan routes require @login_required decorator
- Google Sheets service account must have editor access to sheet
- Session secret key from SECRET_KEY env var
- Never commit google_creds.json or live credentials

## Known Pitfalls
- Google Sheets API rate limits—cache sheet data for a few minutes
- Service account credentials expire—monitor expiration dates
- gspread can hang if Sheet is slow to respond—add timeout
- Multiple concurrent edits to same cell may cause conflicts—warn users
- render.yaml must have correct PORT (Render injects PORT env var)

## Deployment
- Dev: Mac Studio (flask run on localhost:5000)
- Prod: Render.com (git push triggers auto-deploy via render.yaml)
- Deploy via render.yaml: specifies gunicorn start command
- Set environment variables in Render dashboard or .env
- Service account JSON credentials via GOOGLE_CREDS_JSON environment variable
- Never push directly to main

## References
@/Users/qbot/.openclaw/workspace/LESSONS-LEARNED.md
