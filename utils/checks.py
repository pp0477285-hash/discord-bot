import discord
from discord import app_commands


def is_admin_or_mod():
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            return False
        if interaction.user.guild_permissions.administrator:
            return True
        return (
            interaction.user.guild_permissions.manage_messages
            or interaction.user.guild_permissions.ban_members
            or interaction.user.guild_permissions.kick_members
        )

    return app_commands.check(predicate)
