import asyncio
import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import Config
from database import Database

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
    format="[%(asctime)s] %(levelname)s | %(message)s",
)
logger = logging.getLogger("communitybot")

intents = discord.Intents(
    guilds=True,
    messages=True,
    reactions=True,
    members=True,
    voice_states=True,
    message_content=True,
)

bot = commands.Bot(
    command_prefix=Config.PREFIX,
    intents=intents,
    help_command=None,
    case_insensitive=True,
)

COGS = [
    "cogs.moderation",
    "cogs.music",
    "cogs.giveaway",
    "cogs.tickets",
    "cogs.level",
    "cogs.welcome",
    "cogs.utility",
    "cogs.antiraid",
]


@bot.event
async def on_ready():
    print("=" * 60)
    print(f"✅ Bot gestartet als {bot.user}")
    print(f"📌 ID: {bot.user.id}")
    print(f"🔧 Version: {Config.VERSION}")
    print("=" * 60)
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} Slash Commands synchronisiert")
    except Exception as exc:
        logger.exception("Slash Commands konnten nicht synchronisiert werden: %s", exc)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    logger.exception("Befehlsfehler in %s: %s", ctx.command, error)
    await ctx.send(f"⚠ Fehler: {error}")


@bot.event
async def on_app_command_error(interaction, error):
    logger.exception("Slash-Command-Fehler: %s", error)
    if interaction.response.is_done():
        await interaction.followup.send(f"⚠ Fehler: {error}", ephemeral=True)
    else:
        await interaction.response.send_message(f"⚠ Fehler: {error}", ephemeral=True)


async def load_extensions():
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"✔ Geladen: {cog}")
        except Exception as exc:
            logger.exception("Fehler beim Laden von %s: %s", cog, exc)


async def main():
    if not Config.TOKEN:
        raise RuntimeError("TOKEN ist nicht gesetzt. Bitte ergänze die .env-Datei.")

    await Database.initialize()
    await load_extensions()
    await bot.start(Config.TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
