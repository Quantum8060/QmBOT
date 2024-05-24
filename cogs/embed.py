import discord
from discord.ext import commands
import aiohttp
from discord import webhook
import discord.ui


Debug_guild = [1235247721934360577]
class EmbedModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="埋め込むメッセージを入力してください。", style=discord.InputTextStyle.long))


    async def callback(self, interaction: discord.Interaction):

        embed = discord.Embed(title=self.children[0].value, color=0x4169e1)
        embed.add_field(name="", value="")
        
        async with aiohttp.ClientSession() as session:
            webhook = await interaction.channel.create_webhook(name=f"{interaction.user.display_name}")

        await webhook.send(embed=embed)
        await interaction.response.send_message("送信しました。", ephemeral=True)
        await webhook.delete()


class embed(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="embed", description="メッセージを埋め込みにして送信します。")
    async def webhookembed(self, interaction: discord.ApplicationContext):
        
        modal = EmbedModal(title="Embedコマンド")
        await interaction.send_modal(modal)
        await interaction.respond("フォームでの入力を待機しています…", ephemeral=True)

def setup(bot):
    bot.add_cog(embed(bot))

