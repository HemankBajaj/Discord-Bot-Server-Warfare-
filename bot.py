import discord
import random
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')


client = discord.Client()

@client.event
async def on_ready():
    general_channel = client.get_channel(817437302367191123)
    greeting_msg = ['Yo!', 'Hello!', 'Wassup!']
    await general_channel.send(random.choice(greeting_msg))


client.run(os.getenv('DISCORD_TOKEN'))

