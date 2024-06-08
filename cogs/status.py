import discord
from discord.ext import commands

Debug_guild = [1235247721934360577]

class dnd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='set_dnd', description="取り込み中にします。")
    @commands.is_owner()
    async def dnd(self, interaction: discord.ApplicationContext):
        await self.bot.change_presence(status = discord.Status.dnd)
        await interaction.response.send_message("取り込み中に変更しました。", ephemeral=True)

class idle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='set_idle', description="退出中にします。")
    @commands.is_owner()
    async def idle(self, interaction: discord.ApplicationContext):
        await self.bot.change_presence(status = discord.Status.idle)
        await interaction.response.send_message("退席中に変更しました。", ephemeral=True)

class online(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='set_online', description="オンラインにします。")
    @commands.is_owner()
    async def online(self, interaction: discord.ApplicationContext):
        await self.bot.change_presence(status = discord.Status.online)
        await interaction.response.send_message("オンラインに変更しました。", ephemeral=True)



def setup(bot):
    bot.add_cog(dnd(bot))
    bot.add_cog(idle(bot))
    bot.add_cog(online(bot))