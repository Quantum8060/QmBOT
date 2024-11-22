import discord
from discord.ext import commands
import os
from time import sleep
from discord.ext import tasks
import asyncio
import subprocess

Debug_guild = [1235247721934360577]

class stop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="stop", description="BOTを停止します。")
    @commands.is_owner()
    async def stop(self, ctx):
        await ctx.respond("BOTを停止します。", ephemeral=True)
        print("BOTを停止しました。\n------")
        await self.bot.close()
        await asyncio.sleep(1)
        loop = asyncio.get_event_loop()
        loop.stop

    @discord.slash_command(name="reboot", description="BOTを再起動します。")
    @commands.is_owner()
    async def reboot(self, ctx):

        embed = discord.Embed(title="再起動確認", description="BOTを再起動します。")
        await ctx.respond(embed=embed)
        await self.bot.close()
        loop = asyncio.get_event_loop()
        loop.stop
        await asyncio.sleep(30)
        await subprocess.call(['pm2', 'restart' 'main'])




def setup(bot):
    bot.add_cog(stop(bot))