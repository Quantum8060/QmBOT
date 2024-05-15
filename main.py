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
import json

intents = discord.Intents.default()
intents.message_content = (True)

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = discord.Bot(intents=intents)
bot.webhooks = {} # !create で作成したWebhookをおいておく場所
Debug_guild = [1235247721934360577]

blacklist_file = 'blacklist.json'

def load_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

# データをJSONファイルに書き込む関数
def save_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)

#起動通知
@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")
    print("------")
    channel = await bot.fetch_channel("1235247794114134037")

    await channel.send(f"{bot.user}BOT起動完了")



#ping
@bot.slash_command(name="ping", description="BotのPingを確認します。")
async def ping(interaction: discord.Interaction):

    user_id = str(interaction.author.id)

    data = load_data()

    if user_id not in data:
        embed = discord.Embed(title="Ping", description="`{0}ms`".format(round(bot.latency * 1000, 2)))
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)



#clear
@bot.slash_command(name="clear", description="指定された数のメッセージを削除します。")
@commands.has_permissions(administrator = True)
async def clear(interaction: discord.ApplicationContext, num: discord.Option(str, required=True, description="削除するメッセージ数を入力")):
    user_id = str(interaction.author.id)

    data = load_data()

    if user_id not in data:

        async for message in interaction.channel.history(limit=int(num)):
            await message.delete(delay=1.2)
    
        embed=discord.Embed(title="メッセージ削除", description=f"{num}メッセージを削除しました。", color=0x4169e1)
        embed.add_field(name="", value="")
        await interaction.respond(embeds=[embed], ephemeral=True)
    else:
        await interaction.response("あなたはブラックリストに登録されています。", ephemeral=True)

@clear.error
async def clearerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
    else:
        await ctx.respond("Something went wrong...", ephemeral=True) 
        raise error



#userinfo
@bot.slash_command(name="userinfo", description="ユーザー情報を取得します")
async def userinfo(interaction: discord.Interaction, user:discord.Member):

    user_id = str(interaction.author.id)

    data = load_data()

    if user_id not in data:

        user = await bot.fetch_user(f"{user.id}")

        embed = discord.Embed(title="User Info", description=f" <@!{user}>", color=0x4169e1)
        embed.add_field(name="表示名", value=user.display_name,inline=True)
        embed.add_field(name="ユーザーID", value=user.id,inline=True)
        embed.add_field(name="メンション", value=user.mention, inline=True)
        embed.add_field(name="アカウント作成日", value=user.created_at)
        embed.add_field(name="アイコンURL", value=f"[アイコンのURLはこちら！]({user.avatar.url})")
        embed.set_footer(text="Userinfoサービス")
        embed.set_thumbnail(url=user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)

@bot.user_command(name="userinfo")
async def userinfo(interaction, user: discord.Member):
    user_id = str(interaction.author.id)

    data = load_data()
    
    user = await bot.fetch_user(f"{user.id}")

    if user_id not in data:

        embed = discord.Embed(title="User Info", description=f" <@!{user}>", color=0x4169e1)
        embed.add_field(name="表示名", value=user.display_name,inline=True)
        embed.add_field(name="ユーザーID", value=user.id,inline=True)
        embed.add_field(name="メンション", value=user.mention, inline=True)
        embed.add_field(name="アカウント作成日", value=user.created_at)
        embed.add_field(name="アイコンURL", value=f"[アイコンのURLはこちら！]({user.avatar.url})")
        embed.set_footer(text="Userinfoサービス")
        embed.set_thumbnail(url=user.avatar.url)
        await interaction.respond(embed=embed, ephemeral=True)
    else:
        await interaction.respond("あなたはブラックリストに登録されています。", ephemeral=True)



#get server icon
@bot.slash_command(name="servericon", description="サーバーのアイコンを取得します。")
async def servericon(interaction: discord.Interaction):
    user_id = str(interaction.author.id)

    data = load_data()

    if user_id not in data:
  

        try:
            guildicon = interaction.guild.icon.replace(static_format='png')
        except:
            embed = discord.Embed(title="アイコン取得失敗", description="アイコンを取得できません")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="アイコン取得完了", description="サーバーアイコンを取得しました。", color=0x4169e1)
            embed.set_thumbnail(url=guildicon)
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)



#DL youtube
@bot.slash_command(name="youtube", description="YouTube動画のダウンロードリンクを取得します", )
async def ytdl(interaction: discord.Interaction, url:discord.Option(str, required=True, description="ダウンロードしたい動画のURLを入力") ):

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
async def dm(interaction: discord.ApplicationContext):
    user_id = str(interaction.author.id)

    data = load_data()

    if user_id not in data:
        modal = dmModal(title="DM送信用フォーム")
        await interaction.send_modal(modal)
        await interaction.respond("フォームでの入力を待機しています…", ephemeral=True)
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)

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
async def mcsinfo(interaction: discord.ApplicationContext, server_address: discord.Option(str, required=True, description="返信内容を記入")):
    user_id = str(interaction.author.id)

    data = load_data()

    if user_id not in data:
        embed = discord.Embed(title=f"{server_address}のオンライン状況")
        embed.add_field(name="", value="")
        embed.set_image(url=f"https://api.mcstatus.io/v2/widget/java/{server_address}")
        embed.set_author(name="Minecraftサーバーオンライン確認")

        await interaction.respond(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)



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
async def suggestion(interaction: discord.ApplicationContext):
    user_id = str(interaction.author.id)

    data = load_data()

    if user_id not in data:
        modal = suggestionModal(title="BOT管理者に送信。")
        await interaction.send_modal(modal)
        await interaction.respond("フォームでの入力を待機しています…", ephemeral=True)
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)



#invite
@bot.slash_command(name="invite", description="BOTを招待します。")
@commands.cooldown(1, 30, commands.BucketType.user)
async def invite(interaction: discord.ApplicationContext):
        
    user_id = str(interaction.author.id)

    data = load_data()

    if user_id not in data:
        button = discord.ui.Button(label="Invite BOT!", style=discord.ButtonStyle.primary, url="https://discord.com/oauth2/authorize?client_id=1057679845087252521&permissions=8&scope=bot+applications.commands")

        embed=discord.Embed(title="QmBOT招待", description="BOTを招待する場合は下のボタンを押してください。", color=0x4169e1)
        embed.add_field(name="", value="")
        embed.set_footer(text="This BOT developer -> @7984_at")
        view = discord.ui.View()
        view.add_item(button)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)



#anonymous chat
@bot.slash_command(name="anonymous", description="匿名で送信します。")
@commands.cooldown(1, 10, commands.BucketType.user)
async def anonymous(interaction: discord.ApplicationContext, text: discord.Option(str, description="匿名メッセージを送信します。")):

    user_id = str(interaction.author.id)

    data = load_data()

    if user_id not in data:
        embed=discord.Embed()
        embed.add_field(name="", value=f"{text}", inline=False)

        await interaction.respond("匿名メッセージを送信しました。", ephemeral=True)
        await interaction.channel.send(embed=embed)
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)

   

#anonymous image
@bot.slash_command(name="anonymous_im", description="匿名で送信します。")
@commands.cooldown(1, 10, commands.BucketType.user)
async def anonymousIM(interaction: discord.ApplicationContext, picture: discord.Attachment):

    user_id = str(interaction.author.id)

    data = load_data()

    if user_id not in data:
        embed=discord.Embed()
        embed.set_image(url=picture.url)
        embed.add_field(name="", value="")
        embed.set_footer(text="匿名画像")
   

        await interaction.respond("匿名画像メッセージを送信しました。", ephemeral=True)
        await interaction.channel.send(embed=embed)
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)



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
        await webhook.delete()

@bot.slash_command(name="embed", description="メッセージを埋め込みにして送信します。")
async def webhookembed(interaction: discord.ApplicationContext):

    user_id = str(interaction.author.id)

    data = load_data()

    if user_id not in data:
        modal = EmbedModal(title="Embedコマンド")
        await interaction.send_modal(modal)
        await interaction.respond("フォームでの入力を待機しています…", ephemeral=True)
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)


'''
@bot.slash_command(name="r_start", description="VCの録音を開始します。")
async def start_record(ctx:discord.ApplicationContext):
    # コマンドを使用したユーザーのボイスチャンネルに接続
    try:
       vc = await ctx.author.voice.channel.connect()
       await ctx.respond("録音開始...")
    except AttributeError:
       await ctx.respond("ボイスチャンネルに入ってください。")
       return
        
    # 録音開始。mp3で帰ってくる。wavだとなぜか壊れる。
    ctx.voice_client.start_recording(discord.sinks.MP3Sink(), finished_callback, ctx)


async def finished_callback(sink:discord.sinks.MP3Sink, ctx:discord.ApplicationContext):
    # 録音したユーザーの音声を取り出す
    recorded_users = [
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    # discordにファイル形式で送信。拡張子はmp3。
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
    await ctx.channel.send(f"録音終了 {', '.join(recorded_users)}.", files=files) 

@bot.slash_command(name="r_stop", description="VCの録音を終了します。")
async def stop_recording(ctx:discord.ApplicationContext):
    # 録音停止
    ctx.voice_client.stop_recording()
    await ctx.respond("録音終了")
    await ctx.voice_client.disconnect()
'''

blacklist_file = 'blacklist.json'

def load_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

# データをJSONファイルに書き込む関数
def save_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)

#add blacklist
@bot.slash_command(name="add_blacklist", description="ユーザーをブラックリストに追加します。")
@commands.has_permissions(administrator = True)
async def a_blacklist(interaction: discord.Interaction, user: discord.Member, reason: discord.Option(str, description="理由を入力します。")):
    b_id = str(interaction.author.id)

    data = load_data()

    if b_id not in data:

        user_id = await bot.fetch_user(f"{user.id}")
    
        data = load_data()

        if user_id not in data:
            await interaction.respond(f"{user.mention}をブラックリストに追加しました。", ephemeral=True)

            data[str(user.id)] = reason
            save_data(data)
        else:
            await interaction.response.send_message("このユーザーはすでにブラックリストに追加されています。", ephemeral=True)
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)



#show blacklist
@bot.slash_command(name="show_blacklist", description="ブラックリストを一覧表示します。")
async def s_blacklist(interaction: discord.ApplicationContext):
    b_id = str(interaction.author.id)

    data = load_data()

    if b_id not in data:
        try:
            with open(blacklist_file, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            await interaction.send("データファイルが見つかりませんでした。")
            return

        user_id = str(interaction.author.id)

        data = load_data()

        embed = discord.Embed(title="ブラックリストユーザー一覧")
    
        user_info = "\n".join([f"<@!{key}> : {value}" for key, value in data.items()])
        embed.add_field(name="ブラックリストユーザーの一覧です。", value=user_info, inline=False)
    
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)



#open message
@bot.event
async def on_message(message):
    if "https://discord.com/channels/" in message.content:
        link = message.content.split("https://discord.com/channels/")[1]
        guild_id, channel_id, message_id = map(int, link.split("/"))

        if message.guild.id != guild_id:

            return

        try:
            target_channel = bot.get_guild(guild_id).get_channel(channel_id)
            target_message = await target_channel.fetch_message(message_id)

            author = target_message.author
            timestamp = target_message.created_at
            target_message_link = f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"

            embed = discord.Embed(description=target_message.content, color=0x00bfff, timestamp=timestamp)
            embed.set_author(name=author.display_name, icon_url=author.avatar.url if author.avatar else author.default_avatar.url)
            embed.set_footer(text=f"From #{target_message.channel}")

            if target_message.attachments:
                attachment = target_message.attachments[0]
                if any(attachment.filename.lower().endswith(image_ext) for image_ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']):
                    embed.set_image(url=attachment.url)

            await message.channel.send(embed=embed)

            for original_embed in target_message.embeds:
                await message.channel.send(embed=original_embed)

        except Exception as e:
            print(f"エラーらしい: {e}")



#help
class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="管理者用コマンド一覧", style=discord.ButtonStyle.green) # Create a button with the label "😎 Click me!" with color Blurple
    async def help1(self, button: discord.ui.Button, interaction):
        embed = discord.Embed(title="```管理者用コマンド一覧を表示しています。```",
                      description="ここに載っていないコマンドが一部存在していますが、BOT開発者専用のため使用することはできません。")

        embed.set_author(name="管理者用コマンド一覧")

        embed.add_field(name="/add_blacklist",
                value="```ブラックリストにユーザーを登録します。```",
                inline=False)
        embed.add_field(name="/show_blacklist",
                value="```ブラックリストを表示します。```",
                inline=False)
        embed.add_field(name="/dm",
                value="指定したユーザーにDMを送信します。",
                inline=False)
        embed.add_field(name="/clear",
                value="```指定した数のメッセージを削除します。```",
                inline=False)
        embed.add_field(name="☆ほしい機能等があれば`/suggestion`でお願いします。",
                value="",
                inline=False)          

        await interaction.response.send_message(embed=embed,ephemeral=True) # Send a message when the button is clicked
    
    @discord.ui.button(label="機能系コマンド一覧", style=discord.ButtonStyle.primary) # Create a button with the label "😎 Click me!" with color Blurple
    async def help2(self, button: discord.ui.Button, interaction):

        embed = discord.Embed(title="```機能系コマンド一覧を表示しています。```",
                      description="ここに載っていないコマンドが一部存在していますが、管理者専用のため使用することはできません。")

        embed.set_author(name="機能系コマンド一覧")
        embed.add_field(name="/suggestion",
                value="```BOTに関する機能やネタコマンドの提案を行えます。※DM専用コマンドです。```",
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
        embed.add_field(name="/anonymous_im",
                value="```匿名で画像を送信します。```",
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
        embed.add_field(name="/online_check",
                value="```マイクラサーバーのオンライン状態をチェックします。```",
                inline=False)
        embed.add_field(name="☆ほしい機能等があれば`/suggestion`でお願いします。",
                value="",
                inline=False)

        await interaction.response.send_message(embed=embed,ephemeral=True)


@bot.slash_command(name="help", description="コマンド一覧を表示します。") # Create a slash command
@commands.cooldown(1, 30, commands.BucketType.user)
async def help(ctx):
    await ctx.respond("以下のボタンを押すことで指定したコマンド一覧を表示できます。", view=MyView(), ephemeral=True)

bot.run(TOKEN)