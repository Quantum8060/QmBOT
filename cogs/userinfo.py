import discord
from discord.ext import commands

Debug_guild = [1235247721934360577]

class userinfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="userinfo", description="ユーザー情報を取得します。")
    async def userinfo(self, ctx, user:discord.Member):
        try:
            embed = discord.Embed(title="User Info", description=f" <@!{user}>", color=0x4169e1)
            embed.set_thumbnail(url=user.avatar.url)
        except:
            pass
        embed.add_field(name="表示名", value=user.display_name,inline=True)
        embed.add_field(name="ユーザーID", value=user.id,inline=True)
        embed.add_field(name="メンション", value=user.mention, inline=True)
        embed.add_field(name="アカウント作成日", value=user.created_at)
        embed.set_footer(text="Userinfoサービス")
        await ctx.respond(embed=embed, ephemeral=True)

class userinfo_c(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.user_command(name="userinfo")
    async def userinfo_c(self, ctx, user: discord.Member):
    
        try:
            embed = discord.Embed(title="User Info", description=f" <@!{user}>", color=0x4169e1)
            embed.set_thumbnail(url=user.avatar.url)
        except:
            pass
        embed.add_field(name="表示名", value=user.display_name,inline=True)
        embed.add_field(name="ユーザーID", value=user.id,inline=True)
        embed.add_field(name="メンション", value=user.mention, inline=True)
        embed.add_field(name="アカウント作成日", value=user.created_at)
        embed.set_footer(text="Userinfoサービス")
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(userinfo(bot))
    bot.add_cog(userinfo_c(bot))






