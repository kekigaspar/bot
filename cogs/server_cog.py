import subprocess
import time

import discord
import psutil
from discord.ext import commands

server = subprocess.Popen
playit = subprocess.Popen


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="start", with_app_command=True,
                             description="Starts server")
    async def start(self, ctx: commands.Context):
        global server
        global playit
        await ctx.defer(ephemeral=False)
        try:
            if server.poll() is None:
                embed = discord.Embed(title="Already started server")
                return await ctx.reply(embed=embed, mention_author=False)
            else:
                embed = discord.Embed(title="Starting server")
                await ctx.send(embed=embed)
                server = subprocess.Popen(r"minecraft.jar", shell=True)
                playit = subprocess.Popen(r"minecraft.exe", shell=True)
                time.sleep(20)
                embed = discord.Embed(title="Started server")
                return await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(title="Starting server")
            await ctx.send(embed=embed)
            server = subprocess.Popen(r"C:\Users\kekig\Desktop\minecraftcrossserver\paper-1.20.5-22.jar", shell=True)
            playit = subprocess.Popen(r"C:\Program Files\playit_gg\bin\playit.exe", shell=True)
            time.sleep(20)
            embed = discord.Embed(title="Started server")
            return await ctx.reply(embed=embed, mention_author=False)


class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="stop", with_app_command=True,
                             description="Stops server")
    async def stop(self, ctx: commands.Context):
        global server
        global playit
        await ctx.defer(ephemeral=False)
        try:
            kill(server.pid)
            kill(playit.pid)
            embed = discord.Embed(title="Stopped server")
            return await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(title="Already stopped server")
            return await ctx.reply(embed=embed, mention_author=False)


async def setup(bot) -> None:
    global server
    global playit
    server = subprocess.Popen
    playit = subprocess.Popen
    await bot.add_cog(Start(bot))
    await bot.add_cog(Stop(bot))
