import discord
import wavelink

from discord.ext import commands
from discord import app_commands


class MusicPlayer:

    def __init__(self):
        self.queue = []
        self.loop = False
        self.volume = 50


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def get_player(self, interaction: discord.Interaction):

        guild = interaction.guild

        if guild.id not in self.players:
            self.players[guild.id] = MusicPlayer()

        return self.players[guild.id]

    @app_commands.command(
        name="play",
        description="Spielt einen Song"
    )
    async def play(
        self,
        interaction: discord.Interaction,
        query: str
    ):

        if not interaction.user.voice:

            await interaction.response.send_message(
                "❌ Du musst in einem Sprachkanal sein.",
                ephemeral=True
            )
            return

        channel = interaction.user.voice.channel

        player: wavelink.Player

        if interaction.guild.voice_client is None:

            player = await channel.connect(cls=wavelink.Player)

        else:

            player = interaction.guild.voice_client

        tracks = await wavelink.Playable.search(query)

        if not tracks:

            await interaction.response.send_message(
                "❌ Keine Ergebnisse gefunden."
            )
            return

        track = tracks[0]

        await player.play(track)

        embed = discord.Embed(
            title="🎵 Jetzt läuft",
            description=f"**{track.title}**",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Autor",
            value=track.author,
            inline=True
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="pause",
        description="Pausiert die Musik"
    )
    async def pause(self, interaction: discord.Interaction):

        player = interaction.guild.voice_client

        if player:

            await player.pause(True)

            await interaction.response.send_message(
                "⏸ Musik pausiert."
            )

    @app_commands.command(
        name="resume",
        description="Setzt die Musik fort"
    )
    async def resume(self, interaction: discord.Interaction):

        player = interaction.guild.voice_client

        if player:

            await player.pause(False)

            await interaction.response.send_message(
                "▶ Musik fortgesetzt."
            )

    @app_commands.command(
        name="skip",
        description="Überspringt den Song"
    )
    async def skip(self, interaction: discord.Interaction):

        player = interaction.guild.voice_client

        if player:

            await player.skip()

            await interaction.response.send_message(
                "⏭ Song übersprungen."
            )

    @app_commands.command(
        name="stop",
        description="Stoppt die Musik"
    )
    async def stop(self, interaction: discord.Interaction):

        player = interaction.guild.voice_client

        if player:

            await player.disconnect()

            await interaction.response.send_message(
                "⏹ Musik gestoppt."
            )


async def setup(bot):
    await bot.add_cog(Music(bot))