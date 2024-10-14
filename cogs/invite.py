import discord
from discord.ext import commands
import json
from dotenv import load_dotenv
import os
import configparser

Debug_guild = [1235247721934360577]

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
LINK = config_ini["MAIN"]["LINK"]

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



class inviteModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="招待リンクを入力してください。", style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.ApplicationContext):

        load_dotenv()
        correct = os.getenv('PASS')

        self.children[0].value
        if self.children[0].value == correct:
            button = discord.ui.Button(label="Invite BOT!", style=discord.ButtonStyle.primary, url=LINK)
            embed=discord.Embed(title="BOT招待", description="Password認証に成功しました。\nBOTを招待する場合は下のボタンを押してください。", color=0x4169e1)
            embed.add_field(name="", value="")
            view = discord.ui.View()
            view.add_item(button)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await interaction.response.send_message("パスワードが間違っています。", ephemeral=True)

class invite(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="invite", description="BOTを招待します。")
    async def invite(self, interaction: discord.ApplicationContext):
        user_id = str(interaction.author.id)

        data = load_data()

        if user_id not in data:
            modal = inviteModal(title="招待リンクパスワード入力フォーム")
            await interaction.send_modal(modal)
            await interaction.respond("パスワードの入力を待機しています…", ephemeral=True)
        else:
            await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)

def setup(bot):
    bot.add_cog(invite(bot))
