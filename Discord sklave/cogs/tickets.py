import discord
from discord.ext import commands

class TicketView(discord.ui.View):
    @discord.ui.button(label="Ticket öffnen", style=discord.ButtonStyle.green)
    async def open(self, interaction, button):
        guild = interaction.guild
        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}")
        await channel.send(f"{interaction.user.mention} Ticket erstellt")
        await interaction.response.send_message("OK", ephemeral=True)

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Tickets(bot))
