import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

Debug_guild = [1235247721934360577]

class status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    statuses = SlashCommandGroup("status", "ステータスグループ")

    @statuses.command(name='dnd', description="取り込み中にします。")
    @commands.is_owner()
    async def dnd(self, interaction: discord.ApplicationContext):
        await self.bot.change_presence(status = discord.Status.dnd)
        await interaction.response.send_message("取り込み中に変更しました。", ephemeral=True)

    @statuses.command(name='idle', description="退出中にします。")
    @commands.is_owner()
    async def idle(self, interaction: discord.ApplicationContext):
        await self.bot.change_presence(status = discord.Status.idle)
        await interaction.response.send_message("退席中に変更しました。", ephemeral=True)

    @statuses.command(name='online', description="オンラインにします。")
    @commands.is_owner()
    async def online(self, interaction: discord.ApplicationContext):
        await self.bot.change_presence(status = discord.Status.online)
        await interaction.response.send_message("オンラインに変更しました。", ephemeral=True)



def setup(bot):
    bot.add_cog(status(bot))