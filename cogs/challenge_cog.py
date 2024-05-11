import asyncio

import discord
from discord.ext import commands
from discord.ui import Button, Select, View


class Challenge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="challenge", with_app_command=True,
                             description="Challenge someone to ROCK PAPER SCISSORS!")
    async def challenge(self, ctx: commands.Context, opponent: discord.Member):
        await ctx.defer(ephemeral=False)
        embed = discord.Embed(title=f"{opponent.display_name} do you accept?",
                              color=ctx.guild.me.color)

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
            declined = discord.Embed(title=f"{opponent.display_name} has declined the challenge",
                                     color=ctx.guild.me.color)
            await invitation.edit(content=None, embed=declined, view=None)

        if button.data["custom_id"] == accept_button.custom_id:
            accepted = discord.Embed(title="Let the game begin!",
                                     color=ctx.guild.me.color)
            accepted.add_field(name=ctx.author.display_name,
                               value="💭",
                               inline=True)
            accepted.add_field(name="⁣",
                               value="🆚",
                               inline=True)
            accepted.add_field(name=opponent.display_name,
                               value="💭",
                               inline=True)
            await invitation.edit(content=None, embed=accepted, view=None)

            choices = {}

            async def choice_callback(interaction):
                if interaction.user == ctx.author:
                    choices.update({ctx.author.display_name: ['🪨', '🗞', '✂'][['Rock', 'Paper', 'Scissors'].index(choice_select.values[0])]})
                    chose = discord.Embed(title="You chose:",
                                          description=['🪨', '🗞', '✂'][['Rock', 'Paper', 'Scissors'].index(choice_select.values[0])],
                                          color=ctx.guild.me.color)
                    await player1.edit(embed=chose, view=None)

                    accepted.set_field_at(index=0,
                                          name=ctx.author.display_name,
                                          value="✅",
                                          inline=True)
                    await invitation.edit(embed=accepted)

                elif interaction.user == opponent:
                    choices.update({opponent.display_name: ['🪨', '🗞', '✂'][['Rock', 'Paper', 'Scissors'].index(choice_select.values[0])]})
                    chose = discord.Embed(title="You chose:",
                                          description=['🪨', '🗞', '✂'][['Rock', 'Paper', 'Scissors'].index(choice_select.values[0])],
                                          color=ctx.guild.me.color)
                    await player2.edit(embed=chose, view=None)

                    accepted.set_field_at(index=2,
                                          name=opponent.display_name,
                                          value="✅",
                                          inline=True)
                    await invitation.edit(embed=accepted)

            choice = discord.Embed(title="What do you choose?",
                                   color=ctx.guild.me.color)

            choice_select = Select(options=[discord.SelectOption(label="Rock", emoji="🪨", description="Beats scissors"),
                                            discord.SelectOption(label="Paper", emoji="🗞", description="Beats rock"),
                                            discord.SelectOption(label="Scissors", emoji="✂", description="Beats paper")])

            choice_select.callback = choice_callback

            choice_view = View()
            choice_view.add_item(choice_select)

            player1 = await ctx.author.send(embed=choice, view=choice_view)
            player2 = await opponent.send(embed=choice, view=choice_view)

            def author_check(i):
                return i.user == ctx.author and choice_select.custom_id == i.data["custom_id"]

            def opponent_check(i):
                return i.user == opponent and choice_select.custom_id == i.data["custom_id"]

            tasks = [self.bot.wait_for("interaction", check=author_check),
                     self.bot.wait_for("interaction", check=opponent_check)]

            await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

            win = discord.Embed(title="The game has concluded",
                                color=ctx.guild.me.color)

            win.add_field(name=ctx.author.display_name,
                          value=choices[ctx.author.display_name],
                          inline=True)
            win.add_field(name="⁣",
                          value="🆚",
                          inline=True)
            win.add_field(name=opponent.display_name,
                          value=choices[opponent.display_name],
                          inline=True)

            winner = ["No one! It's a tie!", ctx.author.display_name, opponent.display_name][(3 + ["🪨", "🗞", "✂"].index(choices[ctx.author.display_name]) - ["🪨", "🗞", "✂"].index(choices[opponent.display_name])) % 3]
            win.add_field(name="The winner is:", value=winner, inline=False)

            await asyncio.sleep(1)
            await invitation.edit(embed=win)


async def setup(bot) -> None:
    await bot.add_cog(Challenge(bot))
