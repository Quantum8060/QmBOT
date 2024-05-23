import discord
from discord import option
from discord.ext import commands

Debug_guild = [1235247721934360577]

class ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="指定された数のメッセージを削除します。", guild_ids=Debug_guild)
    async def ping(self, ctx: discord.ApplicationContext):

        embed = discord.Embed(title="Ping", description="`{0}ms`".format(round(self.bot.latency * 1000, 2)))
        await ctx.response.send_message(embed=embed)
    
        
def setup(bot):
    bot.add_cog(ping(bot))