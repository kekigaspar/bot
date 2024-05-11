import asyncio
import os

import discord
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="$", intents=intents, owner_id=413071345069588500)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}.")

    async def on_command_error(self, ctx, error):
        print(error)
        await ctx.reply(error, ephemeral=True)


bot = Bot()


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        # noinspection SpellCheckingInspection
        await bot.start('ODI0NjQ0MDU5OTIyMDM4Nzg0.YFyXoQ.43BLiO3UhkhoPYD7CF70gZTLiMU')

asyncio.run(main())
