import discord
from discord import app_commands
from discord.ext import commands

from config import Config
from utils.embeds import info_embed


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping_command(self, ctx: commands.Context):
        await ctx.send(embed=info_embed("🏓 Pong", f"Latency: {round(self.bot.latency * 1000)}ms"))

    @app_commands.command(name="ping")
    async def ping_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=info_embed("🏓 Pong", f"Latency: {round(self.bot.latency * 1000)}ms"), ephemeral=True)

    @commands.command(name="about")
    async def about_command(self, ctx: commands.Context):
        await ctx.send(embed=info_embed("ℹ️ Über den Bot", f"CommunityBot Version {Config.VERSION}"))

    @app_commands.command(name="about")
    async def about_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=info_embed("ℹ️ Über den Bot", f"CommunityBot Version {Config.VERSION}"), ephemeral=True)

    @commands.command(name="serverinfo")
    async def serverinfo_command(self, ctx: commands.Context):
        embed = info_embed("🧾 Serverinfo", f"Server: {ctx.guild.name}")
        embed.add_field(name="Mitglieder", value=str(ctx.guild.member_count), inline=True)
        embed.add_field(name="Owner", value=str(ctx.guild.owner), inline=True)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))
