import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

Debug_guild = [1235247721934360577]

class avatar(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="avatar", description="ユーザーのアイコンを取得します。")
    @commands.has_permissions(administrator = True)
    async def avatar(self, interaction: discord.ApplicationContext, user: discord.Member):
        embed = discord.Embed(title="取得完了！", color=0x4169e1)
        embed.set_image(url=user.avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(avatar(bot))