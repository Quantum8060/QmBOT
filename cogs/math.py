import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
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


class math(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    math = SlashCommandGroup("math", "Math related commands")

    @math.command(name="add", description="足します。")
    async def add(self, ctx: discord.ApplicationContext, num1: int, num2: int):
        sum = num1 + num2
        await ctx.respond(f"{sum}", ephemeral=True)

    @math.command(name="subtract", description="引きます。")
    async def subtract(self, ctx: discord.ApplicationContext, num1: int, num2: int):
        sum = num1 - num2
        await ctx.respond(f"{sum}", ephemeral=True)

    @math.command(name="multiplication",description="掛けます。")
    async def multiplication(self, ctx: discord.ApplicationContext, num1: int, num2: int):
        sum = num1 * num2
        await ctx.respond(f"{sum}", ephemeral=True)

    @math.command(name="division", description="割ります")
    async def division(self, ctx: discord.ApplicationContext, num1: int, num2: int):
        sum = num1 / num2
        await ctx.respond(f"{sum}", ephemeral=True)


def setup(bot):
    bot.add_cog(math(bot))