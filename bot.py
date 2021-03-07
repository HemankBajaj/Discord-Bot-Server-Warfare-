import discord
import random
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')

client = discord.Client()
bot = commands.Bot(command_prefix='-war')

class Player:
    def __init__(self, player_name, player_id):
        self.name = player_name
        self.id = player_id
        self.xp = 50                                                   # for account creation lol
        self.coins = 2000
        self.tanks = 20
        self.fighterJets = 10
        self.soldiers = 5000
        self.bombs = 100
        self.meds = 300
        self.victories = 0
        self.defeats = 0

    def train(self):
        increase_xp = random.randint(1, 10)
        self.xp += increase_xp

    def buy_tanks(self, x):
        self.coins -= 400 * x
        self.tanks += x
        self.xp += int(2*x)

    def buy_fighterJets(self, x):
        self.coins -= 800 * x
        self.fighterJets += x
        self.xp += int(5*x)

    def buy_soldiers(self, x):
        self.coins -= 3 * x
        self.soldiers += x
        self.xp += int(1*x/500)

    def buy_bombs(self, x):
        self.coins -= 10 * x
        self.bombs += x
        self.xp += int(x/15)

    def buy_meds(self, x):
        self.coins -= 25 * x
        self.meds += x
        self.xp += int(3*x/100)

    def spinAndWin(self):
        self.coins -= 600
        prize = random.choice(['xp', 'coins', 'tanks', 'fighterJets', 'soldiers', 'bombs', 'meds'])
        if prize == 'xp':
            self.xp += random.randint(1, 10)
        if prize == 'coins':
            self.coins += random.randint(20, 300) + random.randint(20, 600) + random.randint(60, 600)
        if prize == 'tanks':
            self.tanks += random.randint(1, 5) + random.randint(0, 5)
        if prize == 'fighterJets':
            self.fighterJets += random.randint(1, 3) + random.randint(0, 2)
        if prize == 'soldiers':
            self.soldiers += random.randint(50, 500) + random.randint(50, 500) + random.randint(50, 500) + random.randint(50, 500)
        if prize == 'bombs':
            self.bombs += random.randint(3, 10) + random.randint(3, 10) + random.randint(4, 10)
        if prize == 'meds':
            self.meds += random.randint(5, 30) + random.randint(5, 30)
        def battle(self, player):
        if isinstance(player, Player):

            chance_factor = random.randint(0,1)

            xp_self_num = self.xp
            xp_player_num = player.xp
            xp_den = self.xp + player.xp
            self_xp = 0.3*xp_self_num/xp_den
            pl_xp = 0.3*xp_player_num/xp_den

            bombs_self_num = self.bombs
            bombs_player_num = player.bombs
            bombs_den = self.bombs + player.bombs
            self_bombs = 0.08 * bombs_self_num / bombs_den
            pl_bombs = 0.08 * bombs_player_num / bombs_den

            soldiers_self_num = self.soldiers
            soldiers_player_num = player.soldiers
            soldiers_den = self.soldiers + player.soldiers
            self_soldiers = 0.02 * soldiers_self_num / soldiers_den
            pl_soldiers = 0.02 * soldiers_player_num / soldiers_den

            meds_self_num = self.meds
            meds_player_num = player.meds
            meds_den = self.meds + player.meds
            self_meds = 0.05 * meds_self_num / meds_den
            pl_meds = 0.05 * meds_player_num / meds_den

            fighterJets_self_num = self.fighterJets
            fighterJets_player_num = player.fighterJets
            fighterJets_den = self.fighterJets + player.fighterJets
            self_fighterJets = 0.20 * fighterJets_self_num / fighterJets_den
            pl_fighterJets = 0.20 * fighterJets_player_num / fighterJets_den

            tanks_self_num = self.tanks
            tanks_player_num = player.tanks
            tanks_den = self.tanks + player.xp
            self_tanks = 0.15 * tanks_self_num / tanks_den
            pl_tanks = 0.15 * tanks_player_num / tanks_den

            if chance_factor == 1:
                y = 0
            else:
                y = 1

            self_score = self_bombs + self_xp + self_meds + self_fighterJets + self_tanks + self_soldiers + 0.2*(1-y)
            pl_score = pl_bombs + pl_xp + pl_meds + pl_fighterJets + pl_tanks + pl_soldiers + 0.2*y

            if self_score > pl_score:
                winner = self.name
                self.victories += 1
                player.defeats += 1

                self.xp += random.randint(5,10)
                player.xp += random.randint(1,5)

                self.tanks = int(self.tanks*random.randint(60,90)/100)
                player.tanks = int(player.tanks * random.randint(30, 60) / 100)

                self.bombs = int(self.bombs * random.randint(60, 90) / 100)
                player.bombs = int(player.bombs * random.randint(30, 60) / 100)

                self.soldiers = int(self.soldiers * random.randint(60, 90) / 100)
                player.soldiers = int(player.soldiers * random.randint(30, 60) / 100)

                self.meds = int(self.meds * random.randint(60, 90) / 100)
                player.meds = int(player.meds * random.randint(30, 60) / 100)

                self.fighterJets = int(self.fighterJets * random.randint(60, 90) / 100)
                player.fighterJets = int(player.fighterJets * random.randint(30, 60) / 100)

                alpha = random.randint(30,60)
                self.coins += int(alpha*player.coins/100)
                player.coins = int((100 - alpha)*player.coins/100)

            else:
                winner = player.name
                player.victories += 1
                player.defeats += 1

                player.xp += random.randint(5, 10)
                self.xp += random.randint(1, 5)

                player.tanks = int(player.tanks * random.randint(60, 90) / 100)
                self.tanks = int(self.tanks * random.randint(30, 60) / 100)

                player.bombs = int(player.bombs * random.randint(60, 90) / 100)
                self.bombs = int(self.bombs * random.randint(30, 60) / 100)

                player.soldiers = int(player.soldiers * random.randint(60, 90) / 100)
                self.soldiers = int(self.soldiers * random.randint(30, 60) / 100)

                player.meds = int(player.meds * random.randint(60, 90) / 100)
                self.meds = int(self.meds * random.randint(30, 60) / 100)

                player.fighterJets = int(player.fighterJets * random.randint(60, 90) / 100)
                self.fighterJets = int(self.fighterJets * random.randint(30, 60) / 100)

                alpha = random.randint(30, 60)
                player.coins += int(alpha * self.coins / 100)
                self.coins = int((100 - alpha) * self.coins/100)

        else:
            raise TypeError


hemank = Player('Hemank', '001')
harshit = Player('Harshit', '002')
list_pl = [hemank, harshit]
@client.event
async def on_ready():
    general_channel = client.get_channel(817437302367191123)
    greeting_msg = ['Yo!', 'Hello!', 'Sup!', 'How do you do?', 'Hi', 'Namaste', 'Sat Sri Akal', 'Aloha', 'Konichiva', 'Have a good day', 'Be positive']
    await general_channel.send(random.choice(greeting_msg))

@bot.command(aliases=[' battle', 'battle', ' fight', 'fight'])
async def battle(ctx, player):
    if isinstance(player, Player):
        hemank.battle(player)
        await ctx.send("Winner:" + winner)
    else:
        raise TypeError


client.run(os.getenv('DISCORD_TOKEN'))
