import discord
from discord.ext import commands
import json

Debug_guild = [1235247721934360577]

lock_file = 'lock.json'

def load_data():
    with open(lock_file, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(lock_file, 'w') as file:
        json.dump(data, file, indent=4)


class lock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="lock", description="サーバーをロックします。")
    @commands.is_owner()
    async def lock(self, interaction: discord.ApplicationContext, reason: discord.Option(str, description="理由を入力します。")):
        l_id = str(interaction.guild.id)

        data = load_data()

        if l_id not in data:
            await interaction.response.send_message(f"サーバー:{l_id}をロックしました。", ephemeral=True)

            data[str(interaction.guild.id)] = reason
            save_data(data)
        else:
            await interaction.response.send_message("このサーバーはすでにロックされています。", ephemeral=True)


def setup(bot):
    bot.add_cog(lock(bot))
