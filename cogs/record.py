import discord
from discord.ext import commands
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


class r_start(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="r_start", description="VCの録音を開始します。")
    async def r_start(self, ctx: discord.ApplicationContext):
        user_id = str(ctx.author.id)
        server_id = str(ctx.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:
            if user_id not in data:
                try:
                    vc = await ctx.author.voice.channel.connect()
                    await ctx.respond("録音開始...")
                except AttributeError:
                    await ctx.respond("ボイスチャンネルに入ってください。")
                    return

                ctx.voice_client.start_recording(discord.sinks.MP3Sink(), finished_callback, ctx)
            else:
                await ctx.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await ctx.response.send_message("このサーバーはロックされています。", ephemeral=True)

    async def finished_callback(self, sink:discord.sinks.MP3Sink, ctx:discord.ApplicationContext):
        # 録音したユーザーの音声を取り出す
        recorded_users = [
            f"<@{user_id}>"
            for user_id, audio in sink.audio_data.items()
        ]
        # discordにファイル形式で送信。拡張子はmp3。
        files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
        await ctx.channel.send(f"録音終了 {', '.join(recorded_users)}.", files=files)



class r_stop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="r_stop", description="VCの録音を終了します。")
    async def r_stop(self, ctx: discord.ApplicationContext):
        user_id = str(ctx.author.id)
        server_id = str(ctx.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:
            if user_id not in data:
                ctx.voice_client.stop_recording()
                await ctx.respond("録音終了")
                await ctx.voice_client.disconnect()
            else:
                await ctx.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await ctx.response.send_message("このサーバーはロックされています。", ephemeral=True)

def setup(bot):
    bot.add_cog(r_start(bot))
    bot.add_cog(r_stop(bot))