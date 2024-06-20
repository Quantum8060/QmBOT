import discord
from discord.ext import commands
from discord import Option
from asyncio import sleep
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

class t_channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="create_text", description="テキストチャンネルを作成します。")
    @commands.has_permissions(administrator = True)
    async def t_channel(self, interaction: discord.ApplicationContext, name: discord.Option(str, required=True, description="作成するチャンネル名を入力"), category: discord.Option(discord.CategoryChannel, description="作成するカテゴリーを選択")):
        user_id = str(interaction.author.id)
        server_id = str(interaction.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:
            if user_id not in data:
                await interaction.guild.create_text_channel(name=name, category=category)
                await interaction.response.send_message(f"{name}を作成しました", ephemeral=True)
            else:
                await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await interaction.response.send_message("このサーバーはロックされています。", ephemeral=True)

class v_channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="create_voice", description="ボイスチャンネルを作成します。")
    @commands.has_permissions(administrator = True)
    async def v_channel(self, interaction: discord.ApplicationContext, name: discord.Option(str, required=True, description="作成するチャンネル名を入力"), category: discord.Option(discord.CategoryChannel, description="作成するカテゴリーを選択")):
        user_id = str(interaction.author.id)
        server_id = str(interaction.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:
            if user_id not in data:
                await interaction.guild.create_voice_channel(name=name, category=category)
                await interaction.response.send_message(f"{name}を作成しました。", ephemeral=True)
            else:
                await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await interaction.response.send_message("このサーバーはロックされています。", ephemeral=True)

class f_channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="create_forum", description="フォーラムチャンネルを作成します。")
    @commands.has_permissions(administrator = True)
    async def f_channel(self, interaction: discord.ApplicationContext, name: discord.Option(str, required=True, description="作成するチャンネル名を入力"), category: discord.Option(discord.CategoryChannel, description="作成するカテゴリーを選択")):
        user_id = str(interaction.author.id)
        server_id = str(interaction.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:
            if user_id not in data:
                await interaction.guild.create_forum_channel(name=name, category=category)
                await interaction.response.send_message(f"{name}を作成しました。", ephemeral=True)
            else:
                await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await interaction.response.send_message("このサーバーはロックされています。", ephemeral=True)

class d_channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="delete", description="チャンネルを削除します。")
    @commands.has_permissions(administrator = True)
    async def d_channel(self, interaction: discord.ApplicationContext):
        user_id = str(interaction.author.id)
        server_id = str(interaction.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:
            if user_id not in data:
                await interaction.response.send_message("チャンネルを削除します。しばらくお待ちください。", ephemeral=True)
                await sleep(10)
                await interaction.channel.delete()
            else:
                await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await interaction.response.send_message("このサーバーはロックされています。", ephemeral=True)

def setup(bot):
    bot.add_cog(t_channel(bot))
    bot.add_cog(v_channel(bot))
    bot.add_cog(d_channel(bot))
    bot.add_cog(f_channel(bot))