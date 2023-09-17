import discord
import pytz
import asyncio
import aiohttp
import random
import os
import schedule
import asyncio
from dotenv import load_dotenv
from datetime import datetime
from discord.ext import commands, tasks
import time as py_time

load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # Convert to an integer
WAKACHAN = int(os.getenv('WAKACHAN'))  # Convert to an integer

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
    schedule.every().day.at("18:00").do(send_daily_random_number)

@bot.command()
async def time(ctx, timezone_str):
    try:
        local_time = get_local_time(timezone_str)
        await ctx.send(f'Local time in {timezone_str}: {local_time}')
    except pytz.UnknownTimeZoneError:
        await ctx.send('Invalid timezone. Please use a valid timezone')

@tasks.loop(hours=24)
async def send_daily_random_number():
    print("...send_daily_random_number method...")
    japan_tz = pytz.timezone('Asia/Tokyo')
    current_time = datetime.now(japan_tz)
    formatted_time = current_time.strftime('%m/%d: %H:%M')
    if current_time.hour == 18 and 0 <= current_time.minute <= 5:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            number = random.randint(1, 10) * 100
            wakachan = bot.get_user(WAKACHAN)
            await channel.send(f'{wakachan.mention}, {formatted_time} Time to save ¥{number}!')

@send_daily_random_number.before_loop
async def before_send_daily_random_number():
    await bot.wait_until_ready()

@tasks.loop(seconds=1)
async def update_status():
    vancouver_time = get_local_time('America/Vancouver')
    await bot.change_presence(activity=discord.Game(name=f'Vancouver: {vancouver_time}'))

@update_status.before_loop
async def before_update_status():
    await bot.wait_until_ready()

async def main_loop():
    bot.run(BOT_TOKEN)
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main_loop())
