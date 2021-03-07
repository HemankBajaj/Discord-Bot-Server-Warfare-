import json
import discord
import random
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')

with open('players.json') as f:
    players = json.load(f)

bot = commands.Bot(command_prefix='-war ')


@bot.event
async def on_ready():
    general_channel = bot.get_channel(817437302367191123)
    greeting_msg = ['Yo!', 'Hello!', 'Wassup!', 'How do you do?', 'Hi', 'Namaste', 'Sat Sri Akal', 'Aloha']
    await general_channel.send(random.choice(greeting_msg))


@bot.command(aliases=['join', 'signUp'])
async def register(ctx, name: str):
    players[str(name)] = {"name": str(name),
                          "xp": 50,
                          "coins": 2000,
                          "tanks": 20,
                          "fighterJets": 10,
                          "soldiers": 5000,
                          "meds": 300,
                          "bombs": 100,
                          "victories": 0,
                          "defeats": 0
                          }
    with open("players.json", "w") as file:
        json.dump(players, file)
    await ctx.send("Successfully Registered " + players[name]["name"] + "\nXP = " + str(players[name]["xp"])
                   + "\nCOINS = " + str(players[name]["coins"])
                   + "\nTANKS = " + str(players[name]["tanks"])
                   + "\nFIGHTER JETS = " + str(players[name]["fighterJets"])
                   + "\nSOLDIERS = " + str(players[name]["soldiers"])
                   + "\nMEDS = " + str(players[name]["meds"])
                   + "\nBOMBS = " + str(players[name]["bombs"])
                   + "\nVICTORIES = " + str(players[name]["victories"])
                   + "\nDEFEATS = " + str(players[name]["defeats"]))


@bot.command()
async def profile(ctx, name: str):
    await ctx.send(players[name]["name"] + "\nXP = " + str(players[name]["xp"])
                   + "\nCOINS = " + str(players[name]["coins"])
                   + "\nTANKS = " + str(players[name]["tanks"])
                   + "\nFIGHTER JETS = " + str(players[name]["fighterJets"])
                   + "\nSOLDIERS = " + str(players[name]["soldiers"])
                   + "\nMEDS = " + str(players[name]["meds"])
                   + "\nBOMBS = " + str(players[name]["bombs"])
                   + "\nVICTORIES = " + str(players[name]["victories"])
                   + "\nDEFEATS = " + str(players[name]["defeats"]))


@bot.command()
async def getPlayers(ctx):
    s = ""
    for x in players:
        s = s + x + "\n"
    await ctx.send(s)


@bot.command()
async def career(ctx, name):
    await ctx.send(name + "'s Career\n" + "\nVICTORIES = " + str(players[name]["victories"])
                   + "\nDEFEATS = " + str(players[name]["defeats"]))


@bot.command()
async def coins(ctx, name):
    await ctx.send(name + "\nCOINS = " + str(players[name]["coins"])
                   + "\nTANKS = " + str(players[name]["tanks"]))

@bot.command(aliases= ['weapon'])
async def weapons(ctx, name):
    await ctx.send(name + "'s Weapons\n"
                   + "\nTANKS = " + str(players[name]["tanks"])
                   + "\nFIGHTER JETS = " + str(players[name]["fighterJets"])
                   + "\nSOLDIERS = " + str(players[name]["soldiers"])
                   + "\nMEDS = " + str(players[name]["meds"])
                   + "\nBOMBS = " + str(players[name]["bombs"]))


@bot.command()
async def shop(ctx):
    shop_str = """
              ****SHOP****
    
    To buy any product type:
    -war buy {ur player name} {item} {number}
    
    S.No.       Item             Cost(per item)
    
    1.          tanks                400 coins
    2.          fighterJets      800 coins
    3.          soldiers           3 coins
    4.          meds               25 coins
    5.          bombs             50 coins
    """
    await ctx.send(shop_str)


@bot.command()
async def buy(ctx, name: str, item: str, x: int):
    if item == "tanks":
        players[name]["tanks"] += x
        players[name]["coins"] -= 400 * x
        players[name]["xp"] += int(2 * x)
        await ctx.send("Bought {} tanks.\nCurrent Balance = {}".format(x, players[name]["coins"]))
    if item == "fighterJets":
        players[name]["fighterJets"] += x
        players[name]["coins"] -= 800 * x
        players[name]["xp"] += int(5 * x)
        await ctx.send("Bought {} fighter jets.\nCurrent Balance = {}".format(x, players[name]["coins"]))
    if item == "soldiers":
        players[name]["soldiesr"] += x
        players[name]["coins"] -= 3 * x
        players[name]["xp"] += int(1 * x / 500)
        await ctx.send("Bought {} soldiers.\nCurrent Balance = {}".format(x, players[name]["coins"]))
    if item == "meds":
        players[name]["meds"] += x
        players[name]["coins"] -= 25 * x
        players[name]["xp"] += int(x / 15)
        await ctx.send("Bought {} meds.\nCurrent Balance = {}".format(x, players[name]["coins"]))
    if item == "bombs":
        players[name]["bombs"] += x
        players[name]["coins"] -= 50 * x
        players[name]["xp"] += int(3 * x / 100)
        await ctx.send("Bought {} bombs.\nCurrent Balance = {}".format(x, players[name]["coins"]))
    with open("players.json", "w") as file:  # updates json file after function execution
        json.dump(players, file)


@bot.command()
async def train(ctx, name: str):
    increase_xp = random.randint(1, 5) + random.randint(0, 3) + random.randint(0, 2)
    players[name]["xp"] += increase_xp
    with open("players.json", "w") as file:  # updates json file after function execution
        json.dump(players, file)
    await ctx.send(name + "\n+ {} XP.\nTotal XP {}".format(increase_xp, players[name]["xp"]))


@bot.command(aliases=['spin'])
async def spinAndWin(ctx, name: str):
    players[name]["coins"] -= 600
    prize = random.choice(['xp', 'coins', 'tanks', 'fighterJets', 'soldiers', 'bombs', 'meds'])
    if prize == 'xp':
        bonus = random.randint(1, 10)
        players[name]["xp"] += bonus
        await ctx.send('+ {} XP'.format(bonus))
    if prize == 'coins':
        bonus = random.randint(20, 300) + random.randint(20, 600) + random.randint(60, 600)
        players[name]["coins"] += bonus
        await ctx.send('You won {} fighter jets'.format(bonus))
    if prize == 'tanks':
        bonus = random.randint(1, 5) + random.randint(0, 5)
        players[name]["tanks"] += bonus
        await ctx.send('You won {} tanks'.format(bonus))
    if prize == 'fighterJets':
        bonus = random.randint(1, 3) + random.randint(0, 2)
        players[name]["fighterJets"] += bonus
        await ctx.send('You won {} fighter jets'.format(bonus))
    if prize == 'soldiers':
        bonus = random.randint(50, 500) + random.randint(50, 500) + random.randint(50, 500) + random.randint(
            50, 500)
        players[name]["soldiers"] += bonus
        await ctx.send('You won {} soldiers'.format(bonus))
    if prize == 'bombs':
        bonus = random.randint(3, 10) + random.randint(3, 10) + random.randint(4, 10)
        players[name]["bombs"] += bonus
        await ctx.send('You won {} bombs'.format(bonus))
    if prize == 'meds':
        bonus = random.randint(5, 30) + random.randint(5, 30)
        players[name]["meds"] += bonus
        await ctx.send('You won {} meds'.format(bonus))

    with open("players.json", "w") as file:  # updates json file after function execution
        json.dump(players, file)


bot.run(os.getenv('DISCORD_TOKEN'))
