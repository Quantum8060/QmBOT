import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

Debug_guild = [1235247721934360577]

class clear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="clear", description="指定された数のメッセージを削除します。")
    @commands.has_permissions(administrator = True)
    async def clear(self, interaction: discord.ApplicationContext, num: discord.Option(str, required=True, description="削除するメッセージ数を入力")):

        async for message in interaction.channel.history(limit=int(num)):
            await message.delete(delay=1.2)

        embed=discord.Embed(title="メッセージ削除", description=f"{num}メッセージを削除しました。", color=0x4169e1)
        embed.add_field(name="", value="")
        await interaction.respond(embeds=[embed], ephemeral=True)

    @clear.error
    async def clearerror(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
        else:
            await ctx.respond("Something went wrong...", ephemeral=True)
        raise error


def setup(bot):
    bot.add_cog(clear(bot))