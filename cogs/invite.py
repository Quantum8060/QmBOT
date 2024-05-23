import discord
from discord.ext import commands

Debug_guild = [1235247721934360577]

class invite(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="invite", description="BOTを招待します。")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def invite(self, interaction: discord.ApplicationContext):
        
        button = discord.ui.Button(label="Invite BOT!", style=discord.ButtonStyle.primary, url="https://discord.com/oauth2/authorize?client_id=1057679845087252521&permissions=8&scope=bot+applications.commands")

        embed=discord.Embed(title="QmBOT招待", description="BOTを招待する場合は下のボタンを押してください。", color=0x4169e1)
        embed.add_field(name="", value="")
        view = discord.ui.View()
        view.add_item(button)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

def setup(bot):
    bot.add_cog(invite(bot))
