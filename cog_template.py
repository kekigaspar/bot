"""
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="test", with_app_command=True,
                             description="test")
    async def test(self, ctx: commands.Context):
        await ctx.defer(ephemeral=False)
        embed = discord.Embed(title="test",
                              description="test",
                              color=ctx.guild.me.color)
        return await ctx.reply(embed=embed, mention_author=False)


async def setup(bot) -> None:
    await bot.add_cog(Test(bot))

"""
