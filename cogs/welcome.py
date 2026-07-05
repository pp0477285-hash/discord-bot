import discord
from discord.ext import commands

from database import Database
from utils.embeds import success_embed
from utils.logger import get_logger

logger = get_logger(__name__)


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not member.guild:
            return
        welcome_channel_id = await Database.get_setting(member.guild.id, "welcome_channel")
        auto_role_id = await Database.get_setting(member.guild.id, "auto_role")
        if welcome_channel_id:
            channel = member.guild.get_channel(welcome_channel_id)
            if channel:
                await channel.send(embed=success_embed("👋 Willkommen", f"Willkommen {member.mention} auf dem Server!"))
        if auto_role_id:
            role = member.guild.get_role(auto_role_id)
            if role:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    logger.warning("Rolle konnte nicht vergeben werden")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if not member.guild:
            return
        goodbye_channel_id = await Database.get_setting(member.guild.id, "goodbye_channel")
        if goodbye_channel_id:
            channel = member.guild.get_channel(goodbye_channel_id)
            if channel:
                await channel.send(embed=success_embed("👋 Auf Wiedersehen", f"{member.display_name} hat den Server verlassen."))


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))
