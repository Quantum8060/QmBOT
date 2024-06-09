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


class lock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="lock", description="サーバーをロックします。")
    @commands.is_owner()
    async def lock(self, interaction: discord.Interaction, reason: discord.Option(str, description="理由を入力します。")):
        b_id = str(interaction.author.id)
        l_id = str(interaction.guild.id)

        b_data = load_blacklist_data()
        data = load_lock_data()

        if b_id not in data:

            data = load_lock_data()

            if l_id not in data:
                await interaction.respond(f"サーバー:{l_id}をロックしました。", ephemeral=True)

                data[str(interaction.guild.id)] = reason
                save_lock_data(data)
            else:
                await interaction.response.send_message("このサーバーはすでにロックされています。", ephemeral=True)
        else:
            await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)

def setup(bot):
    bot.add_cog(lock(bot))
