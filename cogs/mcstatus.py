import discord
from discord.ext import commands
import requests
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

class mcstatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="mcstatus", description="マイクラのサーバーステータスを確認します。")
    async def mcstatus(self, ctx, server_address):
        user_id = str(ctx.author.id)
        server_id = str(ctx.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:
            if user_id not in data:
                url = f"https://api.mcstatus.io/v2/status/java/{server_address}"
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()

                    if data['online']:
                        embed = discord.Embed(title="Minecraft Server Status", description=f"サーバーアドレス: {server_address}", color=discord.Color.green())
                        embed.add_field(name="オンライン", value="Yes", inline=True)
                        embed.add_field(name="ホスト", value=data['host'], inline=True)
                        embed.add_field(name="ポート", value=data['port'], inline=True)
                        embed.add_field(name="バージョン", value=data['version']['name_clean'], inline=True)
                        embed.add_field(name="プレイヤー数", value=f"{data['players']['online']} / {data['players']['max']}", inline=True)
                        embed.add_field(name="MOTD", value=data['motd']['clean'], inline=False)
                    else:
                        embed = discord.Embed(title="Minecraft Server Status", description=f"サーバーアドレス: {server_address}", color=discord.Color.red())
                        embed.add_field(name="オンライン", value="No", inline=True)

                    await ctx.respond(embed=embed, ephemeral=True)
                else:
                    await ctx.respond(f"サーバー情報の取得に失敗しました: HTTP {response.status_code}", ephemeral=True)
            else:
                await ctx.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await ctx.response.send_message("このサーバーはロックされています。", ephemeral=True)


def setup(bot):
    bot.add_cog(mcstatus(bot))