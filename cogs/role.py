import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import json
import sqlite3

Debug_guild = [1235247721934360577]  # デバッグ用のギルドID

blacklist_file = 'blacklist.json'
lock_file = 'lock.json'
db_file = 'bot.db'

# SQLite接続設定
conn = sqlite3.connect(db_file)
c = conn.cursor()

# ロールIDを保存するテーブル作成
c.execute('''CREATE TABLE IF NOT EXISTS role_id
             (id TEXT PRIMARY KEY, roleid INTEGER )''')
conn.commit()

# ブラックリストとロックデータの読み込み/保存関数
def load_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)

def load_lock_data():
    with open(lock_file, 'r') as file:
        return json.load(file)

def save_lock_data(data):
    with open(lock_file, 'w') as file:
        json.dump(data, file, indent=4)

# ロールデータをSQLiteに保存
def save_role(message_id, roleid):
    with conn:
        c.execute("INSERT OR IGNORE INTO role_id (id, roleid) VALUES (?, ?)", (message_id, roleid))
        c.execute("UPDATE role_id SET roleid = ? WHERE id = ?", (roleid, message_id))

# ロールデータをSQLiteから取得
def get_role_info(message_id):
    c.execute("SELECT roleid FROM role_id WHERE id = ?", (message_id,))
    return c.fetchone()

# 各ロールごとにボタンを作成するViewクラス
class roleView(discord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=None)  # timeoutをNoneにすることでボタンが再起動後も維持される

        # 各ロールに対応するボタンを動的に作成
        for role in roles:
            self.add_item(RoleButton(role))

# ロールボタンを作成するクラス
class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role):
        super().__init__(label=role.name, custom_id=str(role.id), style=discord.ButtonStyle.primary)
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        # ボタンが押されたときにロールを付与/削除
        user = interaction.user
        role = self.role

        if role in user.roles:
            await user.remove_roles(role)
            await interaction.response.send_message(f"{role.name} ロールを削除しました。", ephemeral=True)
        else:
            await user.add_roles(role)
            await interaction.response.send_message(f"{role.name} ロールを付与しました。", ephemeral=True)

# ロールパネルコマンドのクラス
class role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ロールパネルコマンド
    @discord.slash_command(name="role", description="ロールパネルを設置します。", guild_ids=Debug_guild)
    @commands.has_permissions(administrator=True)
    async def role(self, interaction: discord.ApplicationContext, role_1: discord.Role, role_2: discord.Role = None, role_3: discord.Role = None, role_4: discord.Role = None, role_5: discord.Role = None):
        # 指定されたロールをリストにする
        roles = [role_1, role_2, role_3, role_4, role_5]
        roles = [role for role in roles if role is not None]  # Noneではないロールだけを保持

        if len(roles) < 1 or len(roles) > 5:
            await interaction.response.send_message("ロールの数は1から5の範囲で指定してください。", ephemeral=True)
            return

        user_id = str(interaction.user.id)
        server_id = str(interaction.guild.id)

        data = load_data()
        l_data = load_lock_data()

        if server_id not in l_data:  # サーバーがロックされていないか確認
            if user_id not in data:  # ユーザーがブラックリストにないか確認
                embed = discord.Embed(title="ロールパネル", description="下のボタンを押してロールを取得できます。")
                for role in roles:
                    embed.add_field(name="ロール名", value=role.mention, inline=True)

                await interaction.response.send_message("ロールパネルを作成しました。", ephemeral=True)
                message = await interaction.followup.send(embed=embed, view=roleView(roles))

                message_id = str(message.id)
                for role in roles:
                    save_role(message_id, role.id)  # 各ロールIDを保存
            else:
                await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)
        else:
            await interaction.response.send_message("このサーバーはロックされています。", ephemeral=True)

    # エラーハンドリング
    @role.error
    async def roleerror(self, interaction, error):
        if isinstance(error, MissingPermissions):
            await interaction.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
        else:
            await interaction.respond("Something went wrong...", ephemeral=True)
            raise error

# Botセットアップ
def setup(bot):
    bot.add_cog(role(bot))
