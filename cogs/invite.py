import discord
from discord.ext import commands
import json
from dotenv import load_dotenv
import os

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

class invite(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="invite", description="BOTを招待します。")
    async def invite(self, interaction: discord.ApplicationContext, password):
        user_id = str(interaction.author.id)
        server_id = str(interaction.guild.id)

        data = load_data()
        l_data = load_lock_data()

        load_dotenv()
        correct = os.getenv('PASS')

        if server_id not in l_data:
            if user_id not in data:
                if password == correct:

                    button = discord.ui.Button(label="Invite BOT!", style=discord.ButtonStyle.primary, url="https://discord.com/oauth2/authorize?client_id=1057679845087252521&permissions=8&scope=bot+applications.commands")

                    embed=discord.Embed(title="QmBOT招待", description="Password認証に成功しました。\nBOTを招待する場合は下のボタンを押してください。", color=0x4169e1)
                    embed.add_field(name="", value="")
                    view = discord.ui.View()
                    view.add_item(button)
                    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
                else:
                    await interaction.response.send_message("パスワードが間違っています。", ephemeral=True)
            else:
                await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await interaction.response.send_message("このサーバーはロックされています。", ephemeral=True)

def setup(bot):
    bot.add_cog(invite(bot))
