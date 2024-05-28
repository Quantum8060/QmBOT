import discord
from discord.ext import commands
import psutil

Debug_guild = [1235247721934360577]

class tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='tasks', description="サーバーの使用状況を確認します。")
    @commands.is_owner()
    async def tasks(self, interaction: discord.ApplicationContext):

        embed = discord.Embed(title="サーバー状況", description="サーバーの状態を表示しています。", color=0x4169e1)
        embed.add_field(name="CPU", value=f"{psutil.cpu_percent(interval=1)}％", inline=False)
        embed.add_field(name="Memory", value=f"{psutil.virtual_memory().percent}％", inline=False)
        embed.add_field(name="STORAGE", value=f"{psutil.disk_usage('/').percent}％", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(tasks(bot))