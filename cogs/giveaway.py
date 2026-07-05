import random
import asyncio
from datetime import datetime, timedelta

import discord
from discord import app_commands
from discord.ext import commands

from database import Database
from utils.embeds import error_embed, info_embed, success_embed
from utils.views import GiveawayJoinView
from utils.logger import get_logger

logger = get_logger(__name__)


class Giveaway(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="gstart")
    @commands.has_permissions(manage_guild=True)
    async def start_command(self, ctx: commands.Context, duration: str, winners: int, *, prize: str):
        seconds = self._parse_duration(duration)
        if seconds is None or winners <= 0:
            return await ctx.send(embed=error_embed("❌ Fehler", "Bitte gib eine gültige Dauer wie 30s/5m/1h an."))
        embed = discord.Embed(title="🎉 Giveaway", description=prize, color=0xFEE75C)
        embed.add_field(name="Gewinner", value=str(winners), inline=True)
        embed.add_field(name="Dauer", value=duration, inline=True)
        view = GiveawayJoinView(0)
        message = await ctx.send(embed=embed, view=view)
        giveaway_id = await Database.create_giveaway(ctx.guild.id, ctx.channel.id, message.id, prize, winners, ctx.author.id, int((datetime.utcnow() + timedelta(seconds=seconds)).timestamp()))
        view.giveaway_id = giveaway_id
        await ctx.send(embed=success_embed("🎉 Giveaway gestartet", f"Gewinnspiel wurde erstellt. ID: {giveaway_id}"))

    @app_commands.command(name="gstart")
    @app_commands.describe(duration="Dauer (z. B. 30s, 5m, 1h)", winners="Anzahl der Gewinner", prize="Gewinn")
    async def start_slash(self, interaction: discord.Interaction, duration: str, winners: int, prize: str):
        seconds = self._parse_duration(duration)
        if seconds is None or winners <= 0:
            await interaction.response.send_message(embed=error_embed("❌ Fehler", "Bitte gib eine gültige Dauer an."), ephemeral=True)
            return
        embed = discord.Embed(title="🎉 Giveaway", description=prize, color=0xFEE75C)
        embed.add_field(name="Gewinner", value=str(winners), inline=True)
        embed.add_field(name="Dauer", value=duration, inline=True)
        view = GiveawayJoinView(0)
        await interaction.response.send_message(embed=embed, view=view)
        message = await interaction.original_response()
        giveaway_id = await Database.create_giveaway(interaction.guild_id, interaction.channel_id, message.id, prize, winners, interaction.user.id, int((datetime.utcnow() + timedelta(seconds=seconds)).timestamp()))
        view.giveaway_id = giveaway_id

    @commands.command(name="gend")
    @commands.has_permissions(manage_guild=True)
    async def end_command(self, ctx: commands.Context, giveaway_id: int):
        await self.end_giveaway(ctx, giveaway_id)

    @app_commands.command(name="gend")
    @app_commands.describe(giveaway_id="Giveaway-ID")
    async def end_slash(self, interaction: discord.Interaction, giveaway_id: int):
        await self.end_giveaway(interaction, giveaway_id)

    @commands.command(name="greroll")
    @commands.has_permissions(manage_guild=True)
    async def reroll_command(self, ctx: commands.Context, giveaway_id: int):
        await self.reroll_giveaway(ctx, giveaway_id)

    @app_commands.command(name="greroll")
    @app_commands.describe(giveaway_id="Giveaway-ID")
    async def reroll_slash(self, interaction: discord.Interaction, giveaway_id: int):
        await self.reroll_giveaway(interaction, giveaway_id)

    async def end_giveaway(self, interaction, giveaway_id: int):
        giveaway = await Database.get_giveaway(giveaway_id)
        if not giveaway:
            await interaction.send(embed=error_embed("❌ Fehler", "Giveaway nicht gefunden.")) if hasattr(interaction, "send") else None
            return
        entries = await Database.get_giveaway_entries(giveaway_id)
        winners = []
        if entries:
            winners = random.sample(entries, k=min(giveaway[5], len(entries)))
        await Database.end_giveaway(giveaway_id)
        if hasattr(interaction, "send"):
            await interaction.send(embed=success_embed("🎉 Giveaway beendet", f"Gewinner: {', '.join(str(self.bot.get_user(user_id) or user_id) for user_id in winners)}"))
        else:
            await interaction.response.send_message(embed=success_embed("🎉 Giveaway beendet", f"Gewinner: {', '.join(str(self.bot.get_user(user_id) or user_id) for user_id in winners)}"), ephemeral=True)

    async def reroll_giveaway(self, interaction, giveaway_id: int):
        giveaway = await Database.get_giveaway(giveaway_id)
        if not giveaway:
            await interaction.send(embed=error_embed("❌ Fehler", "Giveaway nicht gefunden.")) if hasattr(interaction, "send") else None
            return
        entries = await Database.get_giveaway_entries(giveaway_id)
        winners = []
        if entries:
            winners = random.sample(entries, k=min(giveaway[5], len(entries)))
        if hasattr(interaction, "send"):
            await interaction.send(embed=info_embed("🔁 Neuer Ziehungsprozess", f"Neue Gewinner: {', '.join(str(self.bot.get_user(user_id) or user_id) for user_id in winners)}"))
        else:
            await interaction.response.send_message(embed=info_embed("🔁 Neuer Ziehungsprozess", f"Neue Gewinner: {', '.join(str(self.bot.get_user(user_id) or user_id) for user_id in winners)}"), ephemeral=True)

    def _parse_duration(self, value: str):
        units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        if value[:-1].isdigit() and value[-1] in units:
            return int(value[:-1]) * units[value[-1]]
        return None


async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway(bot))
