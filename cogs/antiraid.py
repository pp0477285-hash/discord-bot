import discord
from discord.ext import commands

from utils.embeds import error_embed, success_embed
from utils.logger import get_logger

logger = get_logger(__name__)


class AntiRaid(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.raid_mode = False
        self.join_log = {}

    @commands.command(name="antiraid")
    @commands.has_permissions(administrator=True)
    async def antiraid_command(self, ctx: commands.Context, enabled: bool = True):
        self.raid_mode = enabled
        await ctx.send(embed=success_embed("🛡 Anti-Raid", f"Anti-Raid ist jetzt {'aktiv' if enabled else 'deaktiviert'}"))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not self.raid_mode:
            return
        self.join_log[member.guild.id] = self.join_log.get(member.guild.id, 0) + 1
        if self.join_log[member.guild.id] >= 5:
            try:
                await member.guild.ban(member, reason="Anti-Raid Schutz")
            except discord.Forbidden:
                logger.warning("Anti-Raid konnte nicht aktiv werden")


async def setup(bot: commands.Bot):
    await bot.add_cog(AntiRaid(bot))
