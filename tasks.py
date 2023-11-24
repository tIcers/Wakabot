import pytz
import random
import asyncio
import discord
from datetime import datetime, date, timedelta
from db import update_total_savings
from discord.ext import tasks

WAKACHAN=1100773835155968161
CHANNEL_ID = 1152878747331067914

async def schedule_daily_task(bot):
    japan_tz = pytz.timezone('Asia/Tokyo')
    now = datetime.now(japan_tz)
    next_run = now.replace(hour=20, minute=0, second=0, microsecond=0)
    if now.hour >= 20:
        next_run += timedelta(days=1)  
    delay_seconds = (next_run - now).total_seconds()
    await asyncio.sleep(delay_seconds)
    send_daily_random_number.start()

@tasks.loop(hours=24)
async def send_daily_random_number(bot):
    print("Task started: send_daily_random_number")
    japan_tz = pytz.timezone('Asia/Tokyo')
    current_time = datetime.now(japan_tz)
    formatted_time = current_time.strftime('%m/%d: %H:%M')
    print(f"Current time in Japan: {formatted_time}")
    if current_time.hour == 20:
        print("It's time to send the message")
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            try:
                number = random.randint(1, 10) * 100
                update_total_savings(number)
                wakachan = bot.get_user(WAKACHAN)
                await channel.send(f'{wakachan.mention}, {formatted_time} Time to save ¥{number}!')
                print("Message sent successfully")
            except Exception as e:
                print(f"Error sending message:{e}")
        else:
            print(f"Channel with ID {CHANNEL_ID} not found")
def get_local_time(timezone_str):
    tz = pytz.timezone(timezone_str)
    local_time = datetime.now(tz)
    return local_time.strftime('%H:%M:%S')
@tasks.loop(seconds=1)
async def update_status(bot):
    vancouver_time = get_local_time('America/Vancouver')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'Vancouver: {vancouver_time}'))
