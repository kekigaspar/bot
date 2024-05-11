import datetime
import random
import string

import discord
from discord.ext import commands


class Draw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="draw", with_app_command=True,
                             description="test")
    async def draw(self, ctx: commands.Context, size: int = 7):
        await ctx.defer(ephemeral=False)
        size = min(max(size, 1), 13)
        embed = discord.Embed(title="".join([random.choice(string.ascii_letters) for betu in range(random.randint(4, 12))]),
                              description=f"commissioned by {ctx.author.display_name}",
                              color=ctx.guild.me.color,
                              timestamp=datetime.datetime.now())
        embed.add_field(name="",
                        value="\n".join(["".join([random.choice(['⬛', '⬜', '🟦', '🟩', '🟨', '🟥']) for oszlop in range(size)]) for sor in range(size)]))
        return await ctx.reply(embed=embed, mention_author=False)


async def setup(bot) -> None:
    await bot.add_cog(Draw(bot))
