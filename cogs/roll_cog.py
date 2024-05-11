import random

import discord
import pandas as pd
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands


class Rolls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="roll", with_app_command=True,
                             description="Roll a number between 1 and 9999. Be the one with the highest roll!")
    @app_commands.choices(ranking=[Choice(name="Server", value="top"),
                                   Choice(name="Member", value="member")])
    async def roll(self, ctx: commands.Context, ranking: str = "", member: discord.Member = None):
        await ctx.defer(ephemeral=False)

        try:
            leaderboard = pd.read_csv(f"C:/Users/kekig/PycharmProjects/bot_for_real/roll_top/{ctx.guild.id}.csv")
        except FileNotFoundError:
            file = open(f"C:/Users/kekig/PycharmProjects/bot_for_real/roll_top/{ctx.guild.id}.csv", "w")
            file.write("user,score")
            file.close()
            leaderboard = pd.read_csv(f"C:/Users/kekig/PycharmProjects/bot_for_real/roll_top/{ctx.guild.id}.csv")

        if ranking == "top":
            embed = discord.Embed(title="Roll leaderboard",
                                  color=ctx.guild.me.color)
            embed.set_author(name=ctx.guild,
                             icon_url=ctx.guild.icon)
            rank = 1
            for i in range(min(len(leaderboard), 10)):
                try:
                    embed.add_field(name=f"{rank}. {ctx.guild.get_member(leaderboard['user'][i]).display_name}",
                                    value=leaderboard["score"][i],
                                    inline=False)
                    rank += 1
                except:
                    pass

        elif ranking == "member":
            try:
                embed = discord.Embed(title=f"is {list(leaderboard['user']).index(member.id) + 1}. with:",
                                      description=list(leaderboard['score'])[list(leaderboard['user']).index(member.id)],
                                      color=ctx.guild.me.color)
                embed.set_author(name=member.display_name,
                                 icon_url=member.avatar)
            except ValueError:
                embed = discord.Embed(title=f"{member.display_name} does not have a score",
                                      description="on this server",
                                      color=ctx.guild.me.color)

        else:
            number = random.randint(0, 10000)

            leaderboard = leaderboard.set_index("user")
            try:
                if number > leaderboard.loc[ctx.author.id][0]:
                    leaderboard.loc[ctx.author.id] = [number]
            except KeyError:
                leaderboard.loc[ctx.author.id] = [number]
            leaderboard.sort_values("score", ascending=False).to_csv(f"C:/Users/kekig/PycharmProjects/bot_for_real/roll_top/{ctx.guild.id}.csv")

            embed = discord.Embed(title="You rolled:",
                                  description=str(number),
                                  color=ctx.guild.me.color)
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar)

        return await ctx.reply(embed=embed, mention_author=False)


async def setup(bot) -> None:
    await bot.add_cog(Rolls(bot))
