import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import json
import random
import sqlite3

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



conn = sqlite3.connect('bot.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS role_id
             (id TEXT PRIMARY KEY, roleid INTEGER )''')

conn.commit()

def save_role(message_id, roleid):
    with conn:
        c.execute("INSERT OR IGNORE INTO role_id (id, roleid) VALUES (?, ?)", (message_id, roleid))
        c.execute("UPDATE role_id SET roleid = ? WHERE id = ?", (roleid, message_id))

def get_role_info(user_id):
    c.execute("SELECT id, roleid FROM role_id WHERE id = ?", (user_id,))
    return c.fetchone()



class roleReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(roleView())



class roleView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="ロールを取得", custom_id="auth-button", style=discord.ButtonStyle.primary)
    async def auth(self, button: discord.ui.Button, interaction: discord.Interaction):
        m_id = interaction.message.id
        role_id = get_role_info(m_id)

        role = interaction.guild.get_role(role_id[1])

        embed = discord.Embed(title="ロール付与", description=f"<@!{role_id[1]}>を付与しました。", color=0x00ff00)

        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.user.add_roles(role)



class role(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="role", description="認証パネルを設置します。", guild_ids=Debug_guild)
    @commands.has_permissions(administrator=True)
    async def role(self, interaction: discord.ApplicationContext, role: discord.Role):
        user_id = str(interaction.author.id)
        server_id = str(interaction.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:

            if user_id not in data:
                embed = discord.Embed(title="ロールパネル", description="下のボタンを押してロールを取得できます。")
                embed.add_field(name="ロール名", value=role.mention)
                await interaction.response.send_message("ロールパネルを作成しました。", ephemeral=True)

                message = await interaction.followup.send(embed=embed, view=roleView())
                message_id = str(message.id)
                roleid = int(role.id)
                save_role(message_id, roleid)
            else:
                await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await interaction.response.send_message("このサーバーはロックされています。", ephemeral=True)

    @role.error
    async def roleerror(self, interaction, error):
        if isinstance(error, MissingPermissions):
            await interaction.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
        else:
            await interaction.respond("Something went wrong...", ephemeral=True)
            raise error


def setup(bot):
    bot.add_cog(role(bot))
    bot.add_cog(roleReady(bot))