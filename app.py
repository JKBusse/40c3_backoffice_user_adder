import os
import re

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

load_dotenv()

HUB = "https://events.ccc.de/congress/2026/hub"
ASSEMBLY_ID = os.environ["ASSEMBLY_ID"]
HUB_USER = os.environ["HUB_USER"]
HUB_PASSWORD = os.environ["HUB_PASSWORD"]

MEMBERS = f"{HUB}/backoffice/assembly/{ASSEMBLY_ID}/members"
CSRF_RE = re.compile(r'name="csrfmiddlewaretoken" value="([^"]+)"')

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

session = requests.Session()


def login():
    login_url = f"{HUB}/accounts/login/"
    page = session.get(login_url, timeout=10)
    page.raise_for_status()
    r = session.post(
        login_url,
        data={
            "csrfmiddlewaretoken": CSRF_RE.search(page.text).group(1),
            "login": HUB_USER,
            "password": HUB_PASSWORD,
        },
        headers={"Referer": login_url},
        timeout=10,
    )
    r.raise_for_status()
    if "/accounts/login" in r.url or "/2fa" in r.url:
        raise RuntimeError("Login fehlgeschlagen (Zugangsdaten falsch oder 2FA aktiv).")


def members_page():
    page = session.get(MEMBERS, timeout=10)
    if "/accounts/login" in page.url:
        login()
        page = session.get(MEMBERS, timeout=10)
    page.raise_for_status()
    return page


def add_member(username):
    page = members_page()
    r = session.post(
        f"{MEMBERS}/add",
        data={"csrfmiddlewaretoken": CSRF_RE.search(page.text).group(1), "name": username},
        headers={"Referer": MEMBERS},
        timeout=10,
    )
    r.raise_for_status()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        names = [
            n.strip()
            for n in request.form["usernames"].replace(",", "\n").splitlines()
            if n.strip()
        ]
        for name in names:
            try:
                add_member(name)
                flash(f"{name}: Anfrage gesendet.", "ok")
            except (requests.RequestException, RuntimeError) as e:
                flash(f"{name}: {e}", "error")
        return redirect(url_for("index"))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
