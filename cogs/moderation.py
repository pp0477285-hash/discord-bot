import discord
from discord import app_commands
from discord.ext import commands

from database import Database
from utils.embeds import error_embed, info_embed, success_embed
from utils.checks import is_admin_or_mod
from utils.logger import get_logger

logger = get_logger(__name__)


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_command(self, ctx: commands.Context, member: discord.Member, *, reason: str = "Keine Angabe"):
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send(embed=error_embed("❌ Fehler", "Du kannst dieses Mitglied nicht kicken."))
        await member.kick(reason=reason)
        await Database.log_mod_action(ctx.guild.id, ctx.author.id, member.id, "kick", reason)
        await ctx.send(embed=success_embed("✅ Mitglied gekickt", f"{member.mention} wurde gekickt. Grund: {reason}"))

    @app_commands.command(name="kick")
    @app_commands.describe(member="Mitglied", reason="Grund")
    @is_admin_or_mod()
    async def kick_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Keine Angabe"):
        if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message(embed=error_embed("❌ Fehler", "Du kannst dieses Mitglied nicht kicken."), ephemeral=True)
            return
        await member.kick(reason=reason)
        await Database.log_mod_action(interaction.guild_id, interaction.user.id, member.id, "kick", reason)
        await interaction.response.send_message(embed=success_embed("✅ Mitglied gekickt", f"{member.mention} wurde gekickt."), ephemeral=True)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_command(self, ctx: commands.Context, member: discord.Member, *, reason: str = "Keine Angabe"):
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send(embed=error_embed("❌ Fehler", "Du kannst dieses Mitglied nicht bannen."))
        await member.ban(reason=reason)
        await Database.log_mod_action(ctx.guild.id, ctx.author.id, member.id, "ban", reason)
        await ctx.send(embed=success_embed("✅ Mitglied gebannt", f"{member.mention} wurde gebannt. Grund: {reason}"))

    @app_commands.command(name="ban")
    @app_commands.describe(member="Mitglied", reason="Grund")
    @is_admin_or_mod()
    async def ban_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Keine Angabe"):
        if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message(embed=error_embed("❌ Fehler", "Du kannst dieses Mitglied nicht bannen."), ephemeral=True)
            return
        await member.ban(reason=reason)
        await Database.log_mod_action(interaction.guild_id, interaction.user.id, member.id, "ban", reason)
        await interaction.response.send_message(embed=success_embed("✅ Mitglied gebannt", f"{member.mention} wurde gebannt."), ephemeral=True)

    @commands.command(name="timeout")
    @commands.has_permissions(moderate_members=True)
    async def timeout_command(self, ctx: commands.Context, member: discord.Member, duration: int = 60, *, reason: str = "Keine Angabe"):
        until = discord.utils.utcnow() + discord.timedelta(minutes=duration)
        await member.timeout(until, reason=reason)
        await Database.log_mod_action(ctx.guild.id, ctx.author.id, member.id, "timeout", reason)
        await ctx.send(embed=success_embed("✅ Timeout gesetzt", f"{member.mention} wurde für {duration} Minuten getimeoutet."))

    @app_commands.command(name="timeout")
    @app_commands.describe(member="Mitglied", duration="Dauer in Minuten", reason="Grund")
    @is_admin_or_mod()
    async def timeout_slash(self, interaction: discord.Interaction, member: discord.Member, duration: int = 60, reason: str = "Keine Angabe"):
        until = discord.utils.utcnow() + discord.timedelta(minutes=duration)
        await member.timeout(until, reason=reason)
        await Database.log_mod_action(interaction.guild_id, interaction.user.id, member.id, "timeout", reason)
        await interaction.response.send_message(embed=success_embed("✅ Timeout gesetzt", f"{member.mention} wurde getimeoutet."), ephemeral=True)

    @commands.command(name="warn")
    @commands.has_permissions(moderate_members=True)
    async def warn_command(self, ctx: commands.Context, member: discord.Member, *, reason: str = "Keine Angabe"):
        await Database.add_warn(ctx.guild.id, member.id, ctx.author.id, reason)
        await Database.log_mod_action(ctx.guild.id, ctx.author.id, member.id, "warn", reason)
        await ctx.send(embed=success_embed("⚠ Warnung", f"{member.mention} wurde verwarnt. Grund: {reason}"))

    @app_commands.command(name="warn")
    @app_commands.describe(member="Mitglied", reason="Grund")
    @is_admin_or_mod()
    async def warn_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Keine Angabe"):
        await Database.add_warn(interaction.guild_id, member.id, interaction.user.id, reason)
        await Database.log_mod_action(interaction.guild_id, interaction.user.id, member.id, "warn", reason)
        await interaction.response.send_message(embed=success_embed("⚠ Warnung", f"{member.mention} wurde verwarnt."), ephemeral=True)

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear_command(self, ctx: commands.Context, amount: int = 10):
        if amount <= 0:
            return await ctx.send(embed=error_embed("❌ Fehler", "Die Anzahl muss größer als 0 sein."))
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(embed=success_embed("🧹 Nachrichten gelöscht", f"{len(deleted)} Nachrichten wurden entfernt."), delete_after=5)

    @app_commands.command(name="clear")
    @app_commands.describe(amount="Anzahl der Nachrichten")
    @is_admin_or_mod()
    async def clear_slash(self, interaction: discord.Interaction, amount: int = 10):
        if amount <= 0:
            await interaction.response.send_message(embed=error_embed("❌ Fehler", "Die Anzahl muss größer als 0 sein."), ephemeral=True)
            return
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(embed=success_embed("🧹 Nachrichten gelöscht", f"{amount} Nachrichten wurden entfernt."), ephemeral=True)

    @commands.command(name="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock_command(self, ctx: commands.Context):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=success_embed("🔒 Kanal gesperrt", "Der Kanal ist jetzt gesperrt."))

    @app_commands.command(name="lock")
    @is_admin_or_mod()
    async def lock_slash(self, interaction: discord.Interaction):
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message(embed=success_embed("🔒 Kanal gesperrt", "Der Kanal ist jetzt gesperrt."), ephemeral=True)

    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock_command(self, ctx: commands.Context):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=success_embed("🔓 Kanal entsperrt", "Der Kanal ist jetzt entsperrt."))

    @app_commands.command(name="unlock")
    @is_admin_or_mod()
    async def unlock_slash(self, interaction: discord.Interaction):
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message(embed=success_embed("🔓 Kanal entsperrt", "Der Kanal ist jetzt entsperrt."), ephemeral=True)

    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode_command(self, ctx: commands.Context, seconds: int = 10):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(embed=success_embed("⏱ Slowmode", f"Slowmode auf {seconds} Sekunden gesetzt."))

    @app_commands.command(name="slowmode")
    @app_commands.describe(seconds="Slowmode in Sekunden")
    @is_admin_or_mod()
    async def slowmode_slash(self, interaction: discord.Interaction, seconds: int = 10):
        await interaction.channel.edit(slowmode_delay=seconds)
        await interaction.response.send_message(embed=success_embed("⏱ Slowmode", f"Slowmode auf {seconds} Sekunden gesetzt."), ephemeral=True)

    @commands.command(name="modlogs")
    async def modlogs_command(self, ctx: commands.Context, limit: int = 10):
        rows = await Database.get_modlogs(ctx.guild.id, limit)
        if not rows:
            return await ctx.send(embed=error_embed("ℹ️ Keine Logs", "Es liegen keine Moderationslogs vor."))
        lines = [f"{i + 1}. {row[4]} | {row[2]} -> {row[3]}" for i, row in enumerate(rows)]
        await ctx.send(embed=info_embed("📝 Modlogs", "\n".join(lines)))

    @app_commands.command(name="modlogs")
    @app_commands.describe(limit="Anzahl der Einträge")
    async def modlogs_slash(self, interaction: discord.Interaction, limit: int = 10):
        rows = await Database.get_modlogs(interaction.guild_id, limit)
        if not rows:
            await interaction.response.send_message(embed=error_embed("ℹ️ Keine Logs", "Es liegen keine Moderationslogs vor."), ephemeral=True)
            return
        lines = [f"{i + 1}. {row[4]} | {row[2]} -> {row[3]}" for i, row in enumerate(rows)]
        await interaction.response.send_message(embed=info_embed("📝 Modlogs", "\n".join(lines)), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
