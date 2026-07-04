from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Discord Bot Dashboard läuft ✅"

def run():
    app.run(host="0.0.0.0", port=3000)

async def start_dashboard():
    thread = threading.Thread(target=run)
    thread.start()
