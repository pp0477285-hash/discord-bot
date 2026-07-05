import discord
from discord import app_commands
from discord.ext import commands

from database import Database
from utils.embeds import error_embed, info_embed, success_embed
from utils.views import TicketPanelView
from utils.logger import get_logger

logger = get_logger(__name__)


class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ticketpanel")
    @commands.has_permissions(administrator=True)
    async def panel_command(self, ctx: commands.Context):
        view = TicketPanelView()
        await ctx.send(embed=info_embed("🎫 Ticket-System", "Klicke auf den Button, um ein Ticket zu erstellen."), view=view)

    @app_commands.command(name="ticketpanel")
    async def panel_slash(self, interaction: discord.Interaction):
        view = TicketPanelView()
        await interaction.response.send_message(embed=info_embed("🎫 Ticket-System", "Klicke auf den Button, um ein Ticket zu erstellen."), view=view, ephemeral=True)

    @commands.command(name="close")
    async def close_command(self, ctx: commands.Context):
        if not isinstance(ctx.channel, discord.TextChannel):
            return
        await Database.close_ticket(ctx.channel.id)
        await ctx.send(embed=success_embed("✅ Ticket geschlossen", "Das Ticket wurde geschlossen."))

    @app_commands.command(name="close")
    async def close_slash(self, interaction: discord.Interaction):
        await Database.close_ticket(interaction.channel_id)
        await interaction.response.send_message(embed=success_embed("✅ Ticket geschlossen", "Das Ticket wurde geschlossen."), ephemeral=True)

    @commands.command(name="transcript")
    async def transcript_command(self, ctx: commands.Context):
        await ctx.send(embed=info_embed("📝 Transcript", f"Transcript für {ctx.channel.name} wird vorbereitet."))

    @app_commands.command(name="transcript")
    async def transcript_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=info_embed("📝 Transcript", f"Transcript für {interaction.channel.name} wird vorbereitet."), ephemeral=True)

    @commands.command(name="adduser")
    async def adduser_command(self, ctx: commands.Context, member: discord.Member):
        await ctx.channel.set_permissions(member, read_messages=True, send_messages=True)
        await ctx.send(embed=success_embed("➕ Nutzer hinzugefügt", f"{member.mention} wurde dem Ticket hinzugefügt."))

    @commands.command(name="removeuser")
    async def removeuser_command(self, ctx: commands.Context, member: discord.Member):
        await ctx.channel.set_permissions(member, read_messages=False, send_messages=False)
        await ctx.send(embed=success_embed("➖ Nutzer entfernt", f"{member.mention} wurde aus dem Ticket entfernt."))


async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))
