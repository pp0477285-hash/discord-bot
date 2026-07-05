from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

BASE_DIR = Path(__file__).parent


class Config:
    TOKEN = os.getenv("TOKEN", "")
    PREFIX = os.getenv("PREFIX", "!")
    DATABASE = BASE_DIR / "data" / "bot.db"

    EMBED_COLOR = 0x5865F2
    SUCCESS_COLOR = 0x57F287
    ERROR_COLOR = 0xED4245
    WARNING_COLOR = 0xFEE75C

    DEFAULT_VOLUME = 50
    MUSIC_TIMEOUT = 300
    MAX_QUEUE_SIZE = 100

    LAVALINK_HOST = os.getenv("LAVALINK_HOST", "localhost")
    LAVALINK_PORT = int(os.getenv("LAVALINK_PORT", "2333"))
    LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD", "youshallnotpass")

    DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
    DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "5000"))

    DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID", "")
    DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET", "")
    DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "http://localhost:5000/callback")
    DISCORD_REDIRECT_URI_ENCODED = DISCORD_REDIRECT_URI.replace(":", "%3A").replace("/", "%2F")

    VERSION = "2.1.0"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
