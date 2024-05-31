import discord
import discord.ui
from discord import option
import os
import sys
import datetime
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from time import sleep
import aiohttp
import json
import configparser
from discord.ext import tasks


intents = discord.Intents.default()
intents.message_content = (True)

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
TOKEN = config_ini["MAIN"]["TOKEN"]

bot = discord.Bot(intents=intents)
bot.webhooks = {}
Debug_guild = [1235247721934360577]

blacklist_file = 'blacklist.json'

def load_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)

#起動通知
@bot.event
async def on_ready():
    s_loop.start()
    print(f"Bot名:{bot.user} On ready!!")
    print("------")
    channel = await bot.fetch_channel("1235247794114134037")
    await channel.send(f"{bot.user}BOT起動完了")

#サーバー数表示
@tasks.loop(hours=6)
async def s_loop():
    count = len(bot.guilds)
    await bot.change_presence(activity=discord.Game(name="現在の参加サーバー数" + str(count), type=1))



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
@commands.is_owner()
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

@a_blacklist.error
async def a_blacklisterror(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
        else:
            await ctx.respond("Something went wrong...", ephemeral=True)
        raise error



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

            if (target_message.content != "") and (not author.bot):
                await message.channel.send(embed=embed)

            for original_embed in target_message.embeds:
                await message.channel.send(embed=original_embed)

        except Exception as e:
            print(f"エラーらしい: {e}")



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



#suggestion image
@bot.slash_command(name="suggestion_im", description="BOT管理者への報告等の際に画像や動画を送信できます。")
@commands.cooldown(1, 10, commands.BucketType.user)
async def suggestionIM(interaction: discord.ApplicationContext, picture: discord.Attachment):

    user_id = str(interaction.author.id)

    data = load_data()

    if user_id not in data:
        embed = discord.Embed(title="BOTに関する提案", color=0x4169e1)
        embed.add_field(name="", value="")
        embed.set_image(url=picture.url)
        embed.set_footer(icon_url=interaction.user.avatar.url, text=interaction.user.id)
        Quantum = await bot.fetch_user("822458692473323560")
        await Quantum.send(embeds=[embed])
        await interaction.response.send_message(f"以下のファイルを送信しました。\n管理者からBOTで返信が来る可能性がありますのでご了承ください。\n{picture.url}", ephemeral=True)
        await interaction.user.dm_channel.send(f"以下のファイルを送信しました。\n管理者からBOTで返信が来る可能性がありますのでご了承ください。\n{picture.url}")
    else:
        await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)



#stop
def stop_py():
    if (bot.is_closed()):
        print("osを切ります。")
        os.system("kill 1")

@bot.slash_command(name="stop", description="BOTを停止します。")
@commands.is_owner()
async def stop(ctx):
    await ctx.respond("BOTを停止します。", ephemeral=True)
    print("BOTを停止しました。\n------")
    await bot.close()



#cogs登録
cogs_list = [
    'help',
    'clear',
    'ping',
    'userinfo',
    'invite',
    'support',
    'serverinfo',
    'mcstatus',
    'servericon',
    'anonymous',
    'youtube',
    'embed',
    'dm',
    'ban',
    'kick',
    'channel',
    'tasks',
    'avatar'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


bot.run(TOKEN)