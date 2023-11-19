import discord
import pytz
import asyncio
import aiohttp
import random
import ssl
import certifi
import schedule
import os
import time as py_time
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
from discord.ext import commands, tasks

load_dotenv()

WAKACHAN=1100773835155968161
CHANNEL_ID = 1152878747331067914
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

def get_local_time(timezone_str):
    tz = pytz.timezone(timezone_str)
    local_time = datetime.now(tz)
    return local_time.strftime('%H:%M:%S')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    update_status.start()
    send_daily_random_number.start()

@bot.command()
async def time(ctx, timezone_str):
    try:
        local_time = get_local_time(timezone_str)
        await ctx.send(f'Local time in {timezone_str}:{local_time}')
    except pytz.UnknownTimeZoneError:
        await ctx.send('Invalid timezone. Please use a valid timezone')

@tasks.loop(hours=24)
async def send_daily_random_number():
    print("...send_daily_random_number method...")
    japan_tz = pytz.timezone('Asia/Tokyo')
    current_time = datetime.now(japan_tz)
    formatted_time = current_time.strftime('%m/%d: %H:%M')
    if current_time.hour == 20 and 0 <= current_time.minute <= 5:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            number = random.randint(1, 10) * 100
            wakachan = bot.get_user(WAKACHAN)
            await channel.send(f'{wakachan.mention}, {formatted_time} Time to save ¥{number}!')

@tasks.loop(seconds=1)
async def update_status():
    vancouver_time = get_local_time('America/Vancouver')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'Vancouver: {vancouver_time}'))

if __name__ == '__main__':
    bot.run(BOT_TOKEN)
