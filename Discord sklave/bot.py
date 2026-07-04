import os
import asyncio
import logging

import discord
from discord.ext import commands

from dashboard.web import start_dashboard
from database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s"
)

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

COGS = [
    "cogs.moderation",
    "cogs.level",
    "cogs.tickets",
    "cogs.music",
    "cogs.antiraid",

    # Neue Module
    "cogs.giveaway",
    "cogs.ai",
    "cogs.economy",
    "cogs.games",
]

async def load_extensions():
    for extension in COGS:
        try:
            await bot.load_extension(extension)
            logging.info("Geladen: %s", extension)
        except Exception as e:
            logging.exception("Fehler beim Laden von %s", extension)


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        logging.info("%s Slash-Commands synchronisiert.", len(synced))
    except Exception:
        logging.exception("Slash-Sync fehlgeschlagen")

    logging.info("Bot online als %s", bot.user)


async def main():
    await init_db()
    await load_extensions()

    asyncio.create_task(start_dashboard())

    await bot.start(os.getenv("TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())