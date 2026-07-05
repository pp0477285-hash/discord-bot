import discord
from discord.ext import commands

from database import Database
from utils.embeds import error_embed, info_embed, success_embed
from utils.logger import get_logger

logger = get_logger(__name__)


class Level(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _calculate_level(self, xp: int) -> int:
        return 1 + (xp // 100)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
        await Database.add_xp(message.guild.id, message.author.id, 10)
        data = await Database.get_level(message.guild.id, message.author.id)
        new_level = self._calculate_level(data["xp"])
        if new_level != data["level"]:
            await Database.set_level(message.guild.id, message.author.id, new_level, data["xp"], data["messages"])
            await message.channel.send(embed=success_embed("⭐ Levelaufstieg", f"{message.author.mention} ist jetzt Level {new_level}!"))

    @commands.command(name="xp")
    async def xp_command(self, ctx: commands.Context):
        data = await Database.get_level(ctx.guild.id, ctx.author.id)
        await ctx.send(embed=info_embed("⭐ XP", f"XP: {data['xp']} | Level: {data['level']}"))

    @commands.command(name="rank")
    async def rank_command(self, ctx: commands.Context):
        data = await Database.get_level(ctx.guild.id, ctx.author.id)
        await ctx.send(embed=info_embed("🏆 Rang", f"{ctx.author.mention} ist Level {data['level']} mit {data['xp']} XP"))

    @commands.command(name="leaderboard")
    async def leaderboard_command(self, ctx: commands.Context):
        await ctx.send(embed=info_embed("📊 Leaderboard", "Das Leaderboard wird hiermit vorbereitet."))

    @commands.command(name="setlevelrole")
    @commands.has_permissions(administrator=True)
    async def set_level_role(self, ctx: commands.Context, level: int, role: discord.Role):
        await Database.add_level_role(ctx.guild.id, level, role.id)
        await ctx.send(embed=success_embed("🎯 Rollenbelohnung", f"Level {level} gibt nun die Rolle {role.name}."))


async def setup(bot: commands.Bot):
    await bot.add_cog(Level(bot))
