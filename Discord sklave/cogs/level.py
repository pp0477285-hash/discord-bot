import aiosqlite
from discord.ext import commands
import random

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        async with aiosqlite.connect("bot.db") as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS xp (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER
            )
            """)

            await db.execute("""
            INSERT INTO xp (user_id, xp)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET xp = xp + ?
            """, (message.author.id, random.randint(1,5), random.randint(1,5)))

            await db.commit()

async def setup(bot):
    await bot.add_cog(Level(bot))
