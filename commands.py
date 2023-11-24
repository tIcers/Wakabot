from discord.ext import commands
from db import get_total_savings

def setup_commands(bot):
    @bot.command()
    async def total(ctx):
        total_saved = get_total_savings()
        await ctx.send(f'Total amount saved:￥{total_saved}')
