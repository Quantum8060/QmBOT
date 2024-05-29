import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import json

Debug_guild = [1235247721934360577]

blacklist_file = 'blacklist.json'

def load_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)

class avatar(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="avatar", description="ユーザーのアイコンを取得します。")
    async def avatar(self, interaction: discord.ApplicationContext, user: discord.Member):
        user_id = str(interaction.author.id)

        data = load_data()

        if user_id not in data:
            embed = discord.Embed(title="取得完了！", color=0x4169e1)
            embed.set_image(url=user.avatar.url)

            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)

def setup(bot):
    bot.add_cog(avatar(bot))