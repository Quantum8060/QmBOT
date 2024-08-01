import discord
import discord.ui
from discord import option
import os
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from time import sleep
import aiohttp
import json
import configparser
from discord.ext import tasks
import asyncio
import random
import string
from dotenv import load_dotenv
import random


intents = discord.Intents.default()
intents.message_content = (True)

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
TOKEN = config_ini["MAIN"]["TOKEN"]

bot = discord.Bot(intents=intents)
bot.webhooks = {}
Debug_guild = [1235247721934360577]

global result
result = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

#起動通知
@bot.event
async def on_ready():
    s_loop.start()
    os.environ['PASS'] = result
    print(f"Bot名:{bot.user} On ready!!")
    print(os.environ['PASS'])
    print("------")
    channel = await bot.fetch_channel("1235247794114134037")
    pass_channel = await bot.fetch_channel("1251824100515512432")
    await channel.send(f"{bot.user}BOT起動完了")
    await pass_channel.send(f"{result}")

#サーバー数表示
@tasks.loop(hours=6)
async def s_loop():
    count = len(bot.guilds)
    await bot.change_presence(activity=discord.Game(name="現在の参加サーバー数" + str(count), type=1))



blacklist_file = 'blacklist.json'

def load_blacklist_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

def save_blacklist_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)



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

    data = load_blacklist_data()

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

    data = load_blacklist_data()

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



#group test
math = discord.SlashCommandGroup("math", "Math related commands")

@math.command(name="add", description="足します。")
async def add(ctx, num1: int, num2: int):
  sum = num1 + num2
  await ctx.respond(f"{sum}")

@math.command(name="subtract", description="引きます。")
async def subtract(ctx, num1: int, num2: int):
  sum = num1 - num2
  await ctx.respond(f"{sum}")

@math.command(name="multiplication",description="掛けます。")
async def multiplication(ctx, num1: int, num2: int):
  sum = num1 * num2
  await ctx.respond(f"{sum}")

@math.command(name="division", description="割ります")
async def division(ctx, num1: int, num2: int):
  sum = num1 / num2
  await ctx.respond(f"{sum}")

bot.add_application_command(math)


#cogs登録
cogs_list = [
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
    'avatar',
    'status',
    'lock',
    'random',
    'blacklist',
    'stop'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


bot.run(TOKEN)