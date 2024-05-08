import discord
import discord.ui
from discord import Option
import os
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.commands import MissingPermissions
from yt_dlp import YoutubeDL
from discord import webhook
from time import sleep
import aiohttp

intents = discord.Intents.default()
intents.message_content = (True)

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = discord.Bot(intents=intents)
bot.webhooks = {} # !create で作成したWebhookをおいておく場所
Debug_guild = [1235247721934360577]



#起動通知
@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")
    print("------")
    channel = await bot.fetch_channel("1235247794114134037")

    await channel.send(f"{bot.user}BOT起動完了")



#ping
@bot.slash_command(name="ping", description="BotのPingを確認します。")
async def ping(ctx: discord.Interaction):
  embed = discord.Embed(title="Ping",
                        description="`{0}ms`".format(round(bot.latency * 1000, 2)))
  await ctx.response.send_message(embed=embed)



#clear
@bot.slash_command(name="clear", description="指定された数のメッセージを削除します。")
@commands.has_permissions(administrator = True)
async def clear(ctx: discord.ApplicationContext, num: discord.Option(str, required=True, description="削除するメッセージ数を入力")):
    async for message in ctx.channel.history(limit=int(num)):
        await message.delete(delay=1.2)
    
    embed=discord.Embed(title="メッセージ削除", description=f"{num}メッセージを削除しました。", color=0x4169e1)
    embed.add_field(name="", value="")
    await ctx.respond(embeds=[embed], ephemeral=True)

@clear.error
async def clearerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
    else:
        await ctx.respond("Something went wrong...", ephemeral=True) 
        raise error



#userinfo
@bot.slash_command(name="userinfo", description="ユーザー情報を取得します")
async def userinfo(ctx: discord.Interaction, user:discord.Member):

    user = await bot.fetch_user(f"{user.id}")

    embed = discord.Embed(title="User Info", description=f" <@!{user}>", color=0x4169e1)
    embed.add_field(name="表示名", value=user.display_name,inline=True)
    embed.add_field(name="ユーザーID", value=user.id,inline=True)
    embed.add_field(name="メンション", value=user.mention, inline=True)
    embed.add_field(name="アカウント作成日", value=user.created_at)
    embed.add_field(name="アイコンURL", value=f"[アイコンのURLはこちら！]({user.avatar.url})")
    embed.set_footer(text="Userinfoサービス")
    embed.set_thumbnail(url=user.avatar.url)
    await ctx.response.send_message(embed=embed, ephemeral=True)

@bot.user_command(name="userinfo")
async def userinfo(ctx, user: discord.Member):
   
    user = await bot.fetch_user(f"{user.id}")

    embed = discord.Embed(title="User Info", description=f" <@!{user}>", color=0x4169e1)
    embed.add_field(name="表示名", value=user.display_name,inline=True)
    embed.add_field(name="ユーザーID", value=user.id,inline=True)
    embed.add_field(name="メンション", value=user.mention, inline=True)
    embed.add_field(name="アカウント作成日", value=user.created_at)
    embed.add_field(name="アイコンURL", value=f"[アイコンのURLはこちら！]({user.avatar.url})")
    embed.set_footer(text="Userinfoサービス")
    embed.set_thumbnail(url=user.avatar.url)
    await ctx.respond(embed=embed, ephemeral=True)



#get server icon
@bot.slash_command(name="servericon", description="サーバーのアイコンを取得します。")
async def servericon(ctx: discord.Interaction):
  try:
    guildicon = ctx.guild.icon.replace(static_format='png')
  except:
    embed = discord.Embed(title="アイコン取得失敗",
                          description="アイコンを取得できません")
    await ctx.response.send_message(embed=embed, ephemeral=True)
  else:
    embed = discord.Embed(title="アイコン取得完了",
                          description="サーバーアイコンを取得しました。",
                          color=0x4169e1)
    embed.set_thumbnail(url=guildicon)
    await ctx.response.send_message(embed=embed, ephemeral=True)



#DL youtube
@bot.slash_command(name="youtube", description="YouTube動画のダウンロードリンクを取得します", )
async def ytdl(ctx: discord.Interaction, url:discord.Option(str, required=True, description="ダウンロードしたい動画のURLを入力") ):
  await ctx.response.defer()
  
  youtube_dl_opts = {'format' : 'best'}

  try:
    with YoutubeDL(youtube_dl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_url = info_dict.get("url", None)
        video_title = info_dict.get('title', None)

  except:
    embed = discord.Embed(title=":x: エラー",
                          description="エラーが発生しました。",
                          color=0x4169e1)
    await ctx.followup.send(embed=embed)

  else:
    embed = discord.Embed(title="動画DLリンク取得完了",description="`{0}`のダウンロードリンクを取得しました。\n\n[クリックしてダウンロード]({1})\n:warning: 著作権に違反してアップロードされた動画をダウンロードする行為は違法です".format(video_title, video_url),color=0x4169e1)
    await ctx.followup.send(embed=embed)



#DM
class dmModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="タイトルを入力してください。", style=discord.InputTextStyle.short))
        self.add_item(discord.ui.InputText(label="送信内容を入力してください。", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="送信先のユーザーのIDを入力してください。", style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):


        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=0x9b59b6)
        embed.add_field(name="", value="")
        embed.set_footer(icon_url=interaction.user.avatar.url, text=f"{interaction.user.name}")
        user = await bot.fetch_user(f"{self.children[2].value}")
        await user.send(embeds=[embed])
        await interaction.response.send_message("送信しました。", ephemeral=True)

@bot.slash_command(name="dm", description="指定したユーザーにDMを送ります。")
@commands.has_permissions(administrator = True)
async def dm(ctx: discord.ApplicationContext):
    modal = dmModal(title="DM送信用フォーム")
    await ctx.send_modal(modal)
    await ctx.respond("フォームでの入力を待機しています…", ephemeral=True)

@dm.error
async def adminerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
    else:
        await ctx.respond("Something went wrong...", ephemeral=True) 
        raise error



#minecraft server online checker
@bot.slash_command(name="online_check", description="Minecraftのサーバーステータスを確認します。")
@commands.cooldown(1, 30, commands.BucketType.user)
async def mcsinfo(ctx: discord.ApplicationContext, server_address: discord.Option(str, required=True, description="返信内容を記入")):
   embed = discord.Embed(title=f"{server_address}のオンライン状況")
   embed.add_field(name="", value="")
   embed.set_image(url=f"https://api.mcstatus.io/v2/widget/java/{server_address}")
   embed.set_author(name="Minecraftサーバーオンライン確認")

   await ctx.respond(embed=embed, ephemeral=True)


  
#suggestion
class suggestionModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="提案や質問等を入力してください。", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):


        embed = discord.Embed(title="BOTに関する提案", description=self.children[0].value, color=0x4169e1)
        embed.add_field(name="", value="")
        embed.set_footer(icon_url=interaction.user.avatar.url, text=interaction.user.id)
        Quantum = await bot.fetch_user("822458692473323560")
        await Quantum.send(embeds=[embed])
        await interaction.response.send_message(f"以下の内容で送信しました。\n管理者からBOTで返信が来る可能性がありますのでご了承ください。\n```{self.children[0].value}```", ephemeral=True)
        await interaction.user.dm_channel.send(f"以下の内容で送信しました。\n管理者からBOTで返信が来る可能性がありますのでご了承ください。\n```{self.children[0].value}```")

@bot.slash_command(name="suggestion", description="BOT管理者に機能の提案やエラーなどの報告を行うことができます。", )
async def suggestion(ctx: discord.ApplicationContext):
    modal = suggestionModal(title="BOT管理者に送信。")
    await ctx.send_modal(modal)
    await ctx.respond("フォームでの入力を待機しています…", ephemeral=True)



#invite
@bot.slash_command(name="invite", description="BOTを招待します。")
@commands.cooldown(1, 30, commands.BucketType.user)
async def invite(ctx: discord.ApplicationContext):
  button = discord.ui.Button(label="Invite BOT!", style=discord.ButtonStyle.primary, url="https://discord.com/oauth2/authorize?client_id=1057679845087252521&permissions=8&scope=bot+applications.commands")

  embed=discord.Embed(title="QmBOT招待", description="BOTを招待する場合は下のボタンを押してください。", color=0x4169e1)
  embed.add_field(name="", value="")
  embed.set_footer(text="This BOT developer -> @7984_at")
  view = discord.ui.View()
  view.add_item(button)
  await ctx.response.send_message(embed=embed, view=view, ephemeral=True)



#anonymous chat
@bot.slash_command(name="anonymous", description="匿名で送信します。")
@commands.cooldown(1, 10, commands.BucketType.user)
async def anonymous(ctx: discord.ApplicationContext, text: discord.Option(str, description="匿名メッセージを送信します。")):
   
   embed=discord.Embed()
   embed.add_field(name="", value=f"{text}", inline=False)

   await ctx.respond("匿名メッセージを送信しました。", ephemeral=True)
   await ctx.channel.send(embed=embed)

   

#anonymous image
@bot.slash_command(name="anonymous_im", description="匿名で送信します。")
@commands.cooldown(1, 10, commands.BucketType.user)
async def anonymousIM(ctx: discord.ApplicationContext, picture: discord.Attachment):
   
   embed=discord.Embed()
   embed.set_image(url=picture.url)
   embed.add_field(name="", value="")
   embed.set_footer(text="匿名画像")
   

   await ctx.respond("匿名画像メッセージを送信しました。", ephemeral=True)
   await ctx.channel.send(embed=embed)



#Embed webhook
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
        await interaction.response.send_message("送信しました。\n※エラー防止用のメッセージです。", ephemeral=True)

@bot.slash_command(name="embed", description="メッセージを埋め込みにして送信します。")
async def webhookembed(ctx: discord.ApplicationContext):
    modal = EmbedModal(title="Embedコマンド")
    await ctx.send_modal(modal)
    await ctx.respond("フォームでの入力を待機しています…", ephemeral=True)



bot.run(TOKEN)