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

class servericon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="servericon", description="サーバーのアイコンを取得します。")
    async def servericon(self, interaction: discord.ApplicationContext):
        user_id = str(interaction.author.id)
        server_id = str(interaction.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:
            if user_id not in data:
                try:
                    guildicon = interaction.guild.icon.replace(static_format='png')
                except:
                    embed = discord.Embed(title="アイコン取得失敗", description="アイコンを取得できません")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title="アイコン取得完了", description="サーバーアイコンを取得しました。", color=0x4169e1)
                    embed.set_image(url=guildicon)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await interaction.response.send_message("このサーバーはロックされています。", ephemeral=True)

def setup(bot):
    bot.add_cog(servericon(bot))