import discord
from discord.ext import commands
from discord import Option
from discord.ext.commands import MissingPermissions
from asyncio import sleep

Debug_guild = [1235247721934360577]

class t_channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="create_text", description="テキストチャンネルを作成します。")
    async def t_channel(self, interaction: discord.ApplicationContext, name: discord.Option(str, required=True, description="作成するチャンネル名を入力"), category: discord.Option(discord.CategoryChannel, description="作成するカテゴリーを選択")):
        await interaction.guild.create_text_channel(name=name, category=category)
        await interaction.response.send_message(f"{name}を作成しました", ephemeral=True)

class v_channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="create_voice", description="ボイスチャンネルを作成します。")
    async def v_channel(self, interaction: discord.ApplicationContext, name: discord.Option(str, required=True, description="作成するチャンネル名を入力"), category: discord.Option(discord.CategoryChannel, description="作成するカテゴリーを選択")):
        await interaction.guild.create_voice_channel(name=name, category=category)
        await interaction.response.send_message(f"{name}を作成しました。", ephemeral=True)

class d_channel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="delete", description="チャンネルを削除します。")
    async def d_channel(self, interaction: discord.ApplicationContext):
        await interaction.response.send_message("チャンネルを削除します。しばらくお待ちください。", ephemeral=True)
        await sleep(10)
        await interaction.channel.delete()

def setup(bot):
    bot.add_cog(t_channel(bot))
    bot.add_cog(v_channel(bot))
    bot.add_cog(d_channel(bot))