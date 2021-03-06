import discord
import random
from discord.ext import commands

client = discord.Client()

@client.event
async def on_ready():
    general_channel = client.get_channel(817437302367191123)
    greeting_msg = ['Yo!' , 'Hello!' , 'Wassup!']
    await general_channel.send(random.choice(greeting_msg))


client.run('ODE3NjYxOTMzNzM4MTMxNDg2.YEMxBA.sp0aj1JE5Ywmdit4qVj2bTRa9LM')
