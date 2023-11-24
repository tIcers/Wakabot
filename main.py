import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import aiohttp
import certifi

from db import init_db
from tasks import schedule_daily_task, update_status
from commands import setup_commands


load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')


aiohttp.TCPConnector.ssl = False

os.environ['SSL_CERT_FILE'] = certifi.where()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

async def make_request():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://discord.com') as response:
            print("...make_request method...")
            await response.text()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    update_status.start(bot)
    await schedule_daily_task(bot)

setup_commands(bot)

if __name__ == '__main__':
    init_db()
    bot.run(BOT_TOKEN)
