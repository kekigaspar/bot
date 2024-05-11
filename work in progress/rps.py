import discord
from discord.ext import commands
from discord.ui import Button, View


def challenge(ctx, chl: discord.Member, chl_icon, opp: discord.Member, opp_icon):
    embed = discord.Embed(title=f"ROCK PAPER SCISSORS BATTLE",
                          colour=ctx.guild.me.color)

    embed.add_field(name=f"{chl.display_name}",
                    value=f"{chl_icon}",
                    inline=True)
    embed.add_field(name="",
                    value="VS",
                    inline=True)
    embed.add_field(name=f"{opp.display_name}",
                    value=f"{opp_icon}",
                    inline=True)

    return embed


class rps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="rpc", with_app_command=True,
                             description="Challenge someone to ROCK PAPER SCISSORS!")
    async def test(self, ctx: commands.Context, opponent: discord.Member):
        await ctx.defer(ephemeral=False)

        embed = discord.Embed(title=f"ROCK PAPER SCISSORS BATTLE",
                              colour=ctx.guild.me.color)

        embed.add_field(name=f"{ctx.author.display_name} has challenged you!\n{opponent.display_name} do you accept?",
                        value="",
                        inline=False)

        accept_button = Button(label="Accept", style=discord.ButtonStyle.green, emoji="✔")
        decline_button = Button(label="Decline", style=discord.ButtonStyle.red, emoji="✖")

        invite_view = View()
        invite_view.add_item(accept_button)
        invite_view.add_item(decline_button)

        invitation = await ctx.reply(opponent.mention, embed=embed, mention_author=False, view=invite_view)

        def button_check(i):
            try:
                return i.user == opponent and i.data["custom_id"] in [accept_button.custom_id, decline_button.custom_id]
            except KeyError:
                return False

        button = await self.bot.wait_for("interaction", check=button_check)

        if button.data["custom_id"] == decline_button.custom_id:
            declined = discord.Embed(title=f"ROCK PAPER SCISSORS BATTLE",
                                     colour=ctx.guild.me.color)

            embed.add_field(name=f"{opponent.display_name} has declined the challenge,\nfrom {ctx.author.display_name}",
                            value="",
                            inline=False)
            return await invitation.edit(content=None, embed=declined, view=None)


        embed = challenge(ctx, ctx.author, ":thought_balloon:", opponent, ":thought_balloon:")


async def setup(bot) -> None:
    await bot.add_cog(rps(bot))