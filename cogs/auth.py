import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import json
import random

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



class authReady(commands.cogs):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener
    async def on_ready(self):
        self.bot.add_view(authView())


class authModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="タイトルにある式の計算をしてください。", style=discord.InputTextStyle.short))


    async def callback(self, interaction: discord.Interaction):

        embed = discord.Embed(title=self.children[0].value, color=0x4169e1)
        embed.add_field(name="", value="")

        if self.children[0].value == str(auth_math):

            role = interaction.guild.get_role(role_id)

            embed = discord.Embed(title="認証成功", description="認証に成功しました。", color=0x00ff00)

            await interaction.response.send_message(embed=embed, ephemeral=True)
            await interaction.user.add_roles(role)
        else:
            embed = discord.Embed(title="認証失敗", description="認証に失敗しました。\n再度認証を行うかサーバー管理者に連絡してください。", color=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)

class authView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="認証", custom_id="auth-button", style=discord.ButtonStyle.primary)
    async def auth(self, button: discord.ui.Button, interaction):

        global auth_math, random1, random2
        random1 = random.randint(0, 10)
        random2 = random.randint(0, 10)
        auth_math = random1 * random2

        modal = authModal(title=f"{str(random1)} × {str(random2)}")
        await interaction.response.send_modal(modal)



class auth(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="auth", description="認証パネルを設置します。")
    @commands.has_permissions(administrator=True)
    async def auth(self, ctx: discord.ApplicationContext, role: discord.Role):
        user_id = str(ctx.author.id)
        server_id = str(ctx.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:

            if user_id not in data:
                embed = discord.Embed(title="認証パネル", description="下のボタンを押して認証を開始してください。")
                await ctx.respond("認証用パネルを設置しました。", ephemeral=True)
                await ctx.send(embed=embed, view=authView())

                global role_id
                role_id = role.id
            else:
                await ctx.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await ctx.response.send_message("このサーバーはロックされています。", ephemeral=True)

    @auth.error
    async def autherror(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
        else:
            await ctx.respond("Something went wrong...", ephemeral=True)
            raise error


def setup(bot):
    bot.add_cog(auth(bot))