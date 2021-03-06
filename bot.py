import discord
import random
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')

client = discord.Client()

class Player:
    def __init__(self, player_name, player_id):
        self.name = player_name
        self.id = player_id
        self.xp = 50                            # for account creation lol
        self.coins = 2000
        self.tanks = 20
        self.fighterJets = 10
        self.soldiers = 5000
        self.bombs = 100
        self.meds = 300
        self.victories = 0
        self.defeats = 0
        

@client.event
async def on_ready():
    general_channel = client.get_channel(817437302367191123)
    greeting_msg = ['Yo!', 'Hello!', 'Wassup!']
    await general_channel.send(random.choice(greeting_msg))



client.run(os.getenv('DISCORD_TOKEN'))

