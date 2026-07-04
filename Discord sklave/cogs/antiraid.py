from discord.ext import commands
import time

users = {}

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        now = time.time()
        gid = member.guild.id

        users.setdefault(gid, [])

        users[gid] = [t for t in users[gid] if now - t < 10]
        users[gid].append(now)

        if len(users[gid]) > 5:
            print("⚠️ RAID erkannt!")

async def setup(bot):
    await bot.add_cog(AntiRaid(bot))
