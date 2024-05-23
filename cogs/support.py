import discord
from discord.ext import commands

Debug_guild = [1235247721934360577]

class support(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="support", description="サポートサーバーへのリンクを表示します。※ブラックリストの異議申し立てはサポートサーバーで行えます。")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def support(self, interaction: discord.ApplicationContext):
        button = discord.ui.Button(label="Join!", style=discord.ButtonStyle.primary, url="https://discord.gg/Ch4XZdSqPK")

        embed=discord.Embed(title="Join support server!", description="サポートサーバーに参加する場合は下のボタンを押してください。", color=0x4169e1)
        embed.add_field(name="※ブラックリストの異議申し立てに関して", value="異議申し立てはサポートサーバーで行ってください。\nその際、ブラックリストに追加したユーザーにも聴取を行うためユーザーIDを取得してきてください。")
        view = discord.ui.View()
        view.add_item(button)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

def setup(bot):
    bot.add_cog(support(bot))