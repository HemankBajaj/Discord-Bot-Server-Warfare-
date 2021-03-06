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

    def train(self):
        increase_xp = random.randint(1,10)
        self.xp += increase_xp

    def spinAndWin(self):
        self.coins -= 600
        prize = random.choice(['xp', 'coins', 'tanks', 'fighterJets', 'soldiers', 'bombs', 'meds'])
        if prize == 'xp':
            self.xp += random.randint(1,10)
        if prize == 'coins':
            self.coins += random.randint(20,300) + random.randint(20,600) + random.randint(60,600)
        if prize == 'tanks':
            self.tanks += random.randint(1,5) + random.randint(0,5)
        if prize == 'fighterJets':
            self.fighterJets += random.randint(1,3) + random.randint(0,2)
        if prize == 'soldiers':
            self.soldiers += random.randint(50,500) + random.randint(50,500) + random.randint(50,500) + random.randint(50,500)
        if prize == 'bombs':
            self.bombs += random.randint(3,10) + random.randint(3, 10) + random.randint(4, 10)
        if prize == 'meds':
            self.meds += random.randint(5,30) + random.randint(5,30)

@client.event
async def on_ready():
    general_channel = client.get_channel(817437302367191123)
    greeting_msg = ['Yo!', 'Hello!', 'Wassup!']
    await general_channel.send(random.choice(greeting_msg))



client.run(os.getenv('DISCORD_TOKEN'))

