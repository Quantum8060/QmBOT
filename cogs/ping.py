import discord
from discord.ext import commands
import json

Debug_guild = [1235247721934360577]

blacklist_file = 'blacklist.json'

def load_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)

lock_file = 'lock.json'

def load_lock_data():
    with open(lock_file, 'r') as file:
        return json.load(file)

def save_lock_data(data):
    with open(lock_file, 'w') as file:
        json.dump(data, file, indent=4)


class ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="BOTのPingを表示します。")
    async def ping(self, ctx: discord.ApplicationContext):
        user_id = str(ctx.author.id)
        server_id = str(ctx.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:

            if user_id not in data:
                embed = discord.Embed(title="Ping", description="`{0}ms`".format(round(self.bot.latency * 1000, 2)))
                await ctx.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await ctx.response.send_message("このサーバーはロックされています。", ephemeral=True)

def setup(bot):
    bot.add_cog(ping(bot))