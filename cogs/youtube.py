import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import json

Debug_guild = [1235247721934360577]

blacklist_file = 'blacklist.json'

def load_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)

class youtube(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="youtube", description="YouTube動画のダウンロードリンクを取得します。")
    async def youtube(self, interaction: discord.ApplicationContext, url:discord.Option(str, required=True, description="ダウンロードしたい動画のURLを入力")):
        user_id = str(interaction.author.id)

        data = load_data()

        if user_id not in data:
            await interaction.response.defer()

            youtube_dl_opts = {'format' : 'best'}

            try:
                with YoutubeDL(youtube_dl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    video_url = info_dict.get("url", None)
                    video_title = info_dict.get('title', None)

            except:
                embed = discord.Embed(title=":x: エラー", description="エラーが発生しました。", color=0x4169e1)
                await interaction.followup.send(embed=embed)

            else:
                embed = discord.Embed(title="動画DLリンク取得完了",description="`{0}`のダウンロードリンクを取得しました。\n\n[クリックしてダウンロード]({1})\n:warning: 著作権に違反してアップロードされた動画をダウンロードする行為は違法です".format(video_title, video_url),color=0x4169e1)
                await interaction.followup.send(embed=embed)
        else:
            await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)


def setup(bot):
    bot.add_cog(youtube(bot))