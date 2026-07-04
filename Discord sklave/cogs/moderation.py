from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member: str):
        await ctx.send(f"{member} gekickt")

    @commands.command()
    async def ban(self, ctx, member: str):
        await ctx.send(f"{member} gebannt")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
