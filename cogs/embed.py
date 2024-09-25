import discord
from discord.ext import commands
import aiohttp
from discord import webhook
import discord.ui
import json

Debug_guild = [1235247721934360577]

blacklist_file = 'blacklist.json'

def load_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)

lock_file = 'lock.json'

def load_lock_data():
    with open(lock_file, 'r') as file:
        return json.load(file)

def save_lock_data(data):
    with open(lock_file, 'w') as file:
        json.dump(data, file, indent=4)

user_dict = {}


class embed(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @discord.slash_command(name="embed", description="メッセージを埋め込みにして送信します。")
    @commands.has_permissions(administrator=True)
    async def webhookembed(self, interaction):
        user_id = interaction.author.id

        if user_id in user_dict:
            # 辞書にユーザーが存在する場合、削除
            user_dict.pop(user_id)
            await interaction.respond("埋め込み送信モードを終了しました。", ephemeral=True)
        else:
            # 辞書にユーザーが存在しない場合、追加
            user_dict[user_id] = interaction.author.name
            await interaction.respond("埋め込み送信モードが起動しました", ephemeral=True)

class embed_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        user_id = message.author.id

        if user_id in user_dict and not message.author.bot:

            embed = discord.Embed(description=message.content, color=0x4169e1)
            embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)

            if message.attachments:
                for attachment in message.attachments:
                    if attachment.content_type.startswith("image/"):
                        embed.set_image(url=attachment.url)
                        break  # 最初の画像のみを埋め込みに表示

            # メンションのリストを作成
            mentions = [mention.mention for mention in message.mentions]
            role_mentions = [role.mention for role in message.role_mentions]
            if message.mention_everyone:
                mentions.append("@everyone")
            mention_text = " ".join(mentions + role_mentions)

            # 返信元メッセージが存在するかチェック
            if message.reference:
                replied_message = await message.channel.fetch_message(message.reference.message_id)
                # メンション付きでメッセージを送信
                if mention_text:
                    await replied_message.reply(content=mention_text, embed=embed)
                    await message.delete()
                else:
                    await replied_message.reply(embed=embed)
                    await message.delete()

            else:
                # メンション付きでメッセージを送信
                if mention_text:
                    await message.channel.send(content=mention_text, embed=embed)
                    await message.delete()
                else:
                    await message.channel.send(embed=embed)
                    await message.delete()

def setup(bot):
    bot.add_cog(embed(bot))
    bot.add_cog(embed_message(bot))