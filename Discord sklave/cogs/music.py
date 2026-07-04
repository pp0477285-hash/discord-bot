from discord.ext import commands

queue = []

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url: str):
        queue.append(url)
        await ctx.send(f"🎵 Hinzugefügt: {url}")

async def setup(bot):
    await bot.add_cog(Music(bot))
