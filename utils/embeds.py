import discord
from config import Config


def success_embed(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description, color=Config.SUCCESS_COLOR)


def error_embed(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description, color=Config.ERROR_COLOR)


def warning_embed(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description, color=Config.WARNING_COLOR)


def info_embed(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description, color=Config.EMBED_COLOR)
