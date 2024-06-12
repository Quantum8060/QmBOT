import discord
from discord.ext import commands
import json
import random

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

# データをJSONファイルに書き込む関数
def save_lock_data(data):
    with open(lock_file, 'w') as file:
        json.dump(data, file, indent=4)

class dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="dice", description="1~決めた数字の範囲内でサイコロをふります。")
    async def avatar(self, interaction: discord.ApplicationContext, num: discord.Option(int, required=True, description="振りたい最大値を入力。")):
        user_id = str(interaction.author.id)
        server_id = str(interaction.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:
            if user_id not in data:
                num_random = random.randrange(1,num)
                dice_result = str(num_random)
                await interaction.response.send_message(f"{dice_result}がでたよ！", ephemeral=True)
            else:
                await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await interaction.response.send_message("このサーバーはロックされています。", ephemeral=True)

def setup(bot):
    bot.add_cog(dice(bot))