import os
from datetime import datetime, timedelta
from functools import wraps

import gspread
from flask import Flask, flash, redirect, render_template, request, session, url_for
from google.oauth2.service_account import Credentials

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "bonifacic-meal-plan-secret-key-change-me")

USERS = {
    "dj": "wolfpack2026",
    "angela": "wolfpack2026",
}

SHEET_ID = "1pgFsQUT6_pK5I5dZU1S_eyqwDBBdndDd9LkB69MW6R0"
TAB_NAME = "Weekly Meal Plan"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_sheet():
    import json
    creds_json = os.environ.get("GOOGLE_CREDS_JSON")
    if creds_json:
        creds_info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    else:
        creds_file = os.path.join(os.path.dirname(__file__), "google_creds.json")
        creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(TAB_NAME)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect(url_for("meal_plan"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/")
@login_required
def meal_plan():
    sheet = get_sheet()
    rows = sheet.get_all_records()

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    meals = []
    for i, row in enumerate(rows):
        date_str = row.get("Date", "")
        parsed_date = None
        for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m/%d/%y", "%m-%d-%Y"):
            try:
                parsed_date = datetime.strptime(date_str, fmt).date()
                break
            except (ValueError, TypeError):
                continue

        is_today = parsed_date == today if parsed_date else False
        is_tomorrow = parsed_date == tomorrow if parsed_date else False

        meals.append({
            "row_index": i + 2,  # +2 for header row and 0-index
            "date": date_str,
            "parsed_date": parsed_date,
            "breakfast": row.get("Breakfast", ""),
            "lunch": row.get("Lunch", ""),
            "dinner": row.get("Dinner", ""),
            "snack": row.get("Snack", ""),
            "notes": row.get("Notes", ""),
            "is_today": is_today,
            "is_tomorrow": is_tomorrow,
        })

    return render_template("meal_plan.html", meals=meals, user=session["user"])


@app.route("/save_note", methods=["POST"])
@login_required
def save_note():
    row_index = request.form.get("row_index", type=int)
    note = request.form.get("note", "").strip()
    if row_index:
        sheet = get_sheet()
        headers = sheet.row_values(1)
        notes_col = headers.index("Notes") + 1  # 1-indexed
        sheet.update_cell(row_index, notes_col, note)
        flash("Note saved!", "success")
    return redirect(url_for("meal_plan"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
