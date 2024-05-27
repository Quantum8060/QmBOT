import discord
from discord.ext import commands
import discord.ui


Debug_guild = [1235247721934360577]



class helpView(discord.ui.View):

        @discord.ui.button(label="管理者用コマンド一覧", style=discord.ButtonStyle.green)
        async def help1(self, button: discord.ui.Button, interaction):
            embed = discord.Embed(title="```管理者用コマンド一覧を表示しています。```", description="ここに載っていないコマンドが一部存在していますが、BOT開発者専用のため使用することはできません。")

            embed.set_author(name="管理者用コマンド一覧")

            embed.add_field(name="/add_blacklist",
                    value="```ブラックリストにユーザーを登録します。```",
                    inline=False)
            embed.add_field(name="/show_blacklist",
                    value="```ブラックリストを表示します。```",
                    inline=False)
            embed.add_field(name="/dm",
                    value="```指定したユーザーにDMを送信します。```",
                    inline=False)
            embed.add_field(name="/clear",
                    value="```指定した数のメッセージを削除します。```",
                    inline=False)
            embed.add_field(name="/create_text",
                    value="```テキストチャンネルを作成します。```",
                    inline=False)
            embed.add_field(name="/create_voice",
                    value="```ボイスチャンネルを作成します。```",
                    inline=False)
            embed.add_field(name="/delete",
                    value="```コマンドを実行したチャンネルを削除します。```",
                    inline=False)
            embed.add_field(name="",
                    value="",
                    inline=False)
            embed.add_field(name="☆ほしい機能等があれば`/suggestion`でお願いします。",
                    value="",
                    inline=False)
            await interaction.response.send_message(embed=embed,ephemeral=True)

        @discord.ui.button(label="機能系コマンド一覧", style=discord.ButtonStyle.primary)
        async def help2(self, button: discord.ui.Button, interaction):

            embed = discord.Embed(title="```機能系コマンド一覧を表示しています。```", description="ここに載っていないコマンドが一部存在していますが、管理者専用のため使用することはできません。")

            embed.set_author(name="機能系コマンド一覧")
            embed.add_field(name="/suggestion",
                    value="```BOTに関する機能の提案や報告等を行えます。```",
                    inline=False)
            embed.add_field(name="/suggestion_im",
                    value="```BOTに関する機能提案等の際に画像や動画の送信を行えます。```",
                    inline=False)
            embed.add_field(name="/help",
                    value="```コマンド一覧を表示します。```",
                    inline=False)
            embed.add_field(name="/userinfo",
                    value="```IDで指定したユーザーのMCIDを表示します。```",
                    inline=False)
            embed.add_field(name="/anonymous",
                    value="```匿名メッセージを送信します。```",
                    inline=False)
            embed.add_field(name="/embed",
                    value="```メッセージを埋め込みにします。```",
                    inline=False)
            embed.add_field(name="/invite",
                    value="```このBOTの招待ができます。```",
                    inline=False)
            embed.add_field(name="/servericon",
                    value="```サーバーのアイコンを取得します。```",
                    inline=False)
            embed.add_field(name="/youtube",
                    value="```YouTubeから動画をダウンロードできます。```",
                    inline=False)
            embed.add_field(name="/ping",
                    value="```このBOTのpingを確認できます。```",
                    inline=False)
            embed.add_field(name="/mcstatus",
                    value="```マイクラサーバーのステータスをチェックします。```",
                    inline=False)
            embed.add_field(name="/serverinfo",
                    value="```Discordサーバーの情報を表示します。```",
                    inline=False)
            embed.add_field(name="/support",
                    value="```サポートサーバーへのリンクを表示します。```",
                    inline=False)
            embed.add_field(name="",
                    value="",
                    inline=False)
            embed.add_field(name="☆ほしい機能等があれば`/suggestion`でお願いします。",
                    value="",
                    inline=False)
            await interaction.response.send_message(embed=embed,ephemeral=True)

class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="help", description="コマンド一覧を表示します。")
    async def help(self, ctx):
        await ctx.respond("以下のボタンを押すことで指定したコマンド一覧を表示できます。", view=helpView(), ephemeral=True)


def setup(bot):
    bot.add_cog(help(bot))