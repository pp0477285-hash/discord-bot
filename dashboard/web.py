import os
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from config import Config

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")


@app.route("/")
def index():
    return render_template("index.html", version=Config.VERSION)


@app.route("/dashboard")
def dashboard():
    user = session.get("user")
    return render_template("dashboard.html", user=user, version=Config.VERSION)


@app.route("/login")
def login():
    if Config.DISCORD_CLIENT_ID and Config.DISCORD_CLIENT_SECRET:
        auth_url = (
            "https://discord.com/api/oauth2/authorize?client_id="
            + Config.DISCORD_CLIENT_ID
            + "&redirect_uri="
            + Config.DISCORD_REDIRECT_URI
            + "&response_type=code&scope=identify%20guilds"
        )
        return redirect(auth_url)
    session["user"] = {"username": "demo-user", "id": "local"}
    return redirect(url_for("dashboard"))


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if code:
        session["user"] = {"username": "oauth-user", "id": code}
    else:
        session["user"] = {"username": "demo-user", "id": "local"}
    return redirect(url_for("dashboard"))


@app.route("/settings")
def settings():
    return render_template("settings.html", version=Config.VERSION)


@app.route("/api/giveaways")
def giveaways_api():
    return jsonify([{"id": 1, "prize": "Test-Gewinn", "winners": 1}])


@app.route("/api/tickets")
def tickets_api():
    return jsonify([{"id": 1, "creator": "demo-user", "status": "open"}])


if __name__ == "__main__":
    app.run(host=Config.DASHBOARD_HOST, port=Config.DASHBOARD_PORT, debug=True)
