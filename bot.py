import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Eingeloggt als {client.user}")

# /ping Command
@tree.command(name="ping", description="Antwortet mit Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# /hello Command
@tree.command(name="hello", description="Sagt Hallo")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hallo! 👋")

client.run("MTUyMjk4NDA4NjQxMzYzOTc0MQ.GUEA5N.1Sw1wbkYVW1uFiiP_t0wlUIjjpGpqLKg5QEF3c")