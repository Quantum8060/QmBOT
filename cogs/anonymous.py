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

# データをJSONファイルに書き込む関数
def save_lock_data(data):
    with open(lock_file, 'w') as file:
        json.dump(data, file, indent=4)

class anonymous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='anonymous', description="匿名で送信します。")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def anonymous(self, interaction: discord.ApplicationContext, text: discord.Option(str, description="匿名メッセージを送信します。"), picture: discord.Attachment = None):
        user_id = str(interaction.author.id)
        server_id = str(interaction.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:

            if user_id not in data:
                if text and picture:
                    embed=discord.Embed()
                    embed.add_field(name="", value=f"{text}", inline=False)
                    embed.set_image(url=picture.url)

                    await interaction.respond("匿名メッセージを送信しました。", ephemeral=True)
                    await interaction.channel.send(embed=embed)
                elif text:
                    embed=discord.Embed()
                    embed.add_field(name="", value=f"{text}", inline=False)

                    await interaction.respond("匿名メッセージを送信しました。", ephemeral=True)
                    await interaction.channel.send(embed=embed)
            else:
                await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await interaction.response.send_message("このサーバーはロックされています。", ephemeral=True)



class say(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='say', description="BOTが送信します。")
    @commands.is_owner()
    async def anonymous(self, interaction: discord.ApplicationContext, text: discord.Option(str, description="メッセージを入力してください。")):
        user_id = str(interaction.author.id)
        server_id = str(interaction.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:

            if user_id not in data:
                await interaction.response.send_message("送信しました。", ephemeral=True)
                await interaction.send(text)
            else:
                await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await interaction.response.send_message("このサーバーはロックされています。", ephemeral=True)





def setup(bot):
    bot.add_cog(anonymous(bot))
    bot.add_cog(say(bot))