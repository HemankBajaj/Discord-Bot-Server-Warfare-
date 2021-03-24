import json
import random
import os
from discord.ext import commands
import requests
from dotenv import load_dotenv

load_dotenv('.env')

with open('players.json') as f:
    players = json.load(f)

bot = commands.Bot(command_prefix='-war ')

greeting_msg = ['Yo!', 'Hello!', 'Wassup!', 'How do you do?', 'Hi', 'Namaste', 'Sat Sri Akal', 'Aloha']
i = random.randint(0, len(greeting_msg)-1)
@bot.event
async def on_ready():
    general_channel = bot.get_channel(817437302367191123)
    await general_channel.send(str(greeting_msg[i]))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown. Please wait {error.retry_after:.2f}s')


@bot.command(aliases=['join', 'signUp'])
@commands.cooldown(1, 86400, commands.BucketType.user)
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

@bot.command(aliases=['remove'])
# @commands.cooldown(1, 86400, commands.BucketType.user)
async def delete(ctx, name:str):
    players.pop(name)
    await ctx.send("Account of " + name + " deleted successfully.")
    with open("players.json", "w") as file:
        json.dump(players, file)

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
@commands.cooldown(1, 10, commands.BucketType.user)
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
                   + "\nXP = " + str(players[name]["xp"]))

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
@commands.cooldown(1, 45, commands.BucketType.user)
async def buy(ctx, name: str, item: str, x: int):

    if item == "tanks":
        if players[name]["coins"] > 400 * x:
            players[name]["tanks"] += x
            players[name]["coins"] -= 400 * x
            players[name]["xp"] += int(2 * x)
            await ctx.send("Bought {} tanks.\nCurrent Balance = {}".format(x, players[name]["coins"]))
    if item == "fighterJets":
        if players[name]["coins"] > 800 * x:
            players[name]["fighterJets"] += x
            players[name]["coins"] -= 800 * x
            players[name]["xp"] += int(5 * x)
            await ctx.send("Bought {} fighter jets.\nCurrent Balance = {}".format(x, players[name]["coins"]))
        else:
            await ctx.send("Baraabar Paisa la re baba!")
    if item == "soldiers":
        if players[name]["coins"] > 3 * x:
            players[name]["soldiers"] += x
            players[name]["coins"] -= 3 * x
            players[name]["xp"] += int(1 * x / 500)
            await ctx.send("Bought {} soldiers.\nCurrent Balance = {}".format(x, players[name]["coins"]))
        else:
            await ctx.send("Baraabar Paisa la re baba!")
    if item == "meds":
        if players[name]["coins"] > 25 * x:
            players[name]["meds"] += x
            players[name]["coins"] -= 25 * x
            players[name]["xp"] += int(x / 15)
            await ctx.send("Bought {} meds.\nCurrent Balance = {}".format(x, players[name]["coins"]))
        else:
            await ctx.send("Baraabar Paisa la re baba!")
    if item == "bombs":
        if players[name]["coins"] > 50 * x:
            players[name]["bombs"] += x
            players[name]["coins"] -= 50 * x
            players[name]["xp"] += int(3 * x / 100)
        else:
            await ctx.send("Baraabar Paisa la re baba!")
        await ctx.send("Bought {} bombs.\nCurrent Balance = {}".format(x, players[name]["coins"]))
    with open("players.json", "w") as file:  # updates json file after function execution
        json.dump(players, file)

@bot.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def train(ctx, name: str):
    increase_xp = random.randint(1, 5) + random.randint(0, 3) + random.randint(0, 2)
    players[name]["xp"] += increase_xp
    with open("players.json", "w") as file:  # updates json file after function execution
        json.dump(players, file)
    await ctx.send(name + "\n+ {} XP.\nTotal XP {}".format(increase_xp, players[name]["xp"]))


@bot.command(aliases=['spin'])
@commands.cooldown(1, 120, commands.BucketType.user)
async def spinAndWin(ctx, name: str):
    if players[name]["coins"]>=600:
        players[name]["coins"] -= 600
        prize = random.choice(['xp', 'coins', 'tanks', 'fighterJets', 'soldiers', 'bombs', 'meds'])
        if prize == 'xp':
            bonus = random.randint(1, 10)
            players[name]["xp"] += bonus
            await ctx.send('+ {} XP'.format(bonus))
        if prize == 'coins':
            bonus = random.randint(20, 300) + random.randint(20, 600) + random.randint(60, 600)
            players[name]["coins"] += bonus
            await ctx.send(name+' won {} fighter jets'.format(bonus))
        if prize == 'tanks':
            bonus = random.randint(1, 5) + random.randint(0, 5)
            players[name]["tanks"] += bonus
            await ctx.send(name+' won {} tanks'.format(bonus))
        if prize == 'fighterJets':
            bonus = random.randint(1, 3) + random.randint(0, 2)
            players[name]["fighterJets"] += bonus
            await ctx.send(name+' won {} fighter jets'.format(bonus))
        if prize == 'soldiers':
            bonus = random.randint(50, 500) + random.randint(50, 500) + random.randint(50, 500) + random.randint(
                50, 500)
            players[name]["soldiers"] += bonus
            await ctx.send(name+' won {} soldiers'.format(bonus))
        if prize == 'bombs':
            bonus = random.randint(3, 10) + random.randint(3, 10) + random.randint(4, 10)
            players[name]["bombs"] += bonus
            await ctx.send(name+' won {} bombs'.format(bonus))
        if prize == 'meds':
            bonus = random.randint(5, 30) + random.randint(5, 30)
            players[name]["meds"] += bonus
            await ctx.send(name+' won {} meds'.format(bonus))

        with open("players.json", "w") as file:  # updates json file after function execution
            json.dump(players, file)
    else:
        await ctx.send("PAISE KAM HAIN BRO!" + str(600 - players[name]["coins"]) + "coins aur laao!")
@bot.command()
# @commands.cooldown(1, 120, commands.BucketType.user)
async def battle(ctx, name1:str, name2:str):

    chance_factor = random.randint(0, 1)

    xp_p1_num = players[name1]["xp"]
    xp_p2_num = players[name2]["xp"]
    xp_den = players[name1]["xp"] + players[name2]["xp"]
    p1_xp = 0.3 * xp_p1_num / xp_den
    p2_xp = 0.3 * xp_p2_num / xp_den

    bombs_p1_num = players[name1]["bombs"]
    bombs_p2_num = players[name2]["bombs"]
    bombs_den = players[name1]["bombs"] + players[name2]["bombs"]
    p1_bombs = 0.08 * bombs_p1_num / bombs_den
    p2_bombs = 0.08 * bombs_p2_num / bombs_den

    soldiers_p1_num = players[name1]["soldiers"]
    soldiers_p2_num = players[name2]["soldiers"]
    soldiers_den = players[name1]["soldiers"] + players[name2]["soldiers"]
    p1_soldiers = 0.02 * soldiers_p1_num / soldiers_den
    p2_soldiers = 0.02 * soldiers_p2_num / soldiers_den

    meds_p1_num = players[name1]["meds"]
    meds_p2_num = players[name2]["meds"]
    meds_den = players[name1]["meds"] + players[name2]["meds"]
    p1_meds = 0.05 * meds_p1_num / meds_den
    p2_meds = 0.05 * meds_p2_num / meds_den

    fighterJets_p1_num = players[name1]["fighterJets"]
    fighterJets_p2_num = players[name2]["fighterJets"]
    fighterJets_den = players[name1]["fighterJets"] + players[name2]["fighterJets"]
    p1_fighterJets = 0.20 * fighterJets_p1_num / fighterJets_den
    p2_fighterJets = 0.20 * fighterJets_p2_num / fighterJets_den

    tanks_p1_num = players[name1]["tanks"]
    tanks_p2_num = players[name2]["tanks"]
    tanks_den = players[name1]["tanks"] + players[name2]["tanks"]
    p1_tanks = 0.15 * tanks_p1_num / tanks_den
    p2_tanks = 0.15 * tanks_p2_num / tanks_den

    if chance_factor == 1:
        y = 0
    else:
        y = 1

    p1_score = p1_xp + p1_meds + p1_bombs + p1_tanks + p1_fighterJets + p1_soldiers + 0.2*(1-y)
    p2_score = p2_xp + p2_meds + p2_bombs + p2_tanks + p1_fighterJets + p2_soldiers + 0.2*y

    if p1_score > p2_score:
        players[name1]["victories"] += 1
        players[name2]["defeats"] += 1

        # xp
        p1_xp_inc = random.randint(5, 10)
        p2_xp_inc = random.randint(1, 5)
        players[name1]["xp"] += p1_xp_inc
        players[name2]["xp"] += p2_xp_inc

        # army resources
        p1_bombs_decreased = random.randint(10,40)
        p2_bombs_decreased = random.randint(40,70)
        players[name1]["bombs"] = int(players[name1]["bombs"]*(100 - p1_bombs_decreased)/100)
        players[name2]["bombs"] = int(players[name2]["bombs"]*(100 - p2_bombs_decreased)/100)

        p1_meds_decreased = random.randint(10, 40)
        p2_meds_decreased = random.randint(40, 70)
        players[name1]["meds"] = int(players[name1]["meds"] * (100 - p1_meds_decreased) / 100)
        players[name2]["meds"] = int(players[name2]["meds"] * (100 - p2_meds_decreased) / 100)

        p1_soldiers_decreased = random.randint(10, 40)
        p2_soldiers_decreased = random.randint(40, 70)
        players[name1]["soldiers"] = int(players[name1]["soldiers"] * (100 - p1_soldiers_decreased) / 100)
        players[name2]["soldiers"] = int(players[name2]["soldiers"] * (100 - p2_soldiers_decreased) / 100)

        p1_tanks_decreased = random.randint(10, 40)
        p2_tanks_decreased = random.randint(40, 70)
        players[name1]["tanks"] = int(players[name1]["tanks"] * (100 - p1_tanks_decreased) /100)
        players[name2]["tanks"] = int(players[name2]["tanks"] * (100 - p2_tanks_decreased) / 100)

        p1_fighterJets_decreased = random.randint(10, 40)
        p2_fighterJets_decreased = random.randint(40, 70)
        players[name1]["fighterJets"] = int(players[name1]["fighterJets"] * (100 - p1_fighterJets_decreased) / 100)
        players[name2]["fighterJets"] = int(players[name2]["fighterJets"] * (100 - p2_fighterJets_decreased) / 100)

        # wealth
        alpha = random.randint(30, 60)
        p1_coin_gain = int(alpha*players[name2]["coins"]/100)
        players[name1]["coins"] += p1_coin_gain
        players[name2]["coins"] = int((100 - alpha) * players[name2]["coins"]/ 100)
        if p1_coin_gain <= players[name2]["coins"]:
            s ="The battle was won by " + name1 + "\n"
            s += "\n**** Battle Statistics****\n\n"
            s += "***" + name1 + "***"
            s += "\nCoins Gained = " + str(p1_coin_gain)
            s += "\nXP increased = " + str(p1_xp_inc)
            s += "\nTANKS Lost = "  + str(p1_tanks_decreased) + "%"
            s += "\nFIGHTER JETS Lost = "  + str(p1_fighterJets_decreased) + "%"
            s += "\nBOMBS Lost = "  + str(p1_bombs_decreased) + "%"
            s += "\nSOLDIERS Lost = "  + str(p1_soldiers_decreased) + "%"
            s += "\nTANKS Lost = "  + str(p1_tanks_decreased) + "%" + "\n\n"

            s += "***" + name2 + "***"
            s += "\nCoins Lost = " + str(p1_coin_gain)
            s += "\nXP increased = " + str(p2_xp_inc)
            s += "\nTANKS Lost = " + str(p2_tanks_decreased) + "%"
            s += "\nFIGHTER JETS Lost = " + str(p2_fighterJets_decreased) + "%"
            s += "\nBOMBS Lost = " + str(p2_bombs_decreased) + "%"
            s += "\nSOLDIERS Lost = " + str(p2_soldiers_decreased) + "%"
            s += "\nTANKS Lost = " + str(p2_tanks_decreased) + "%" + "\n\n"
            await ctx.send(s)
        else:
            await ctx.send(name2 + "is too poor to be attacked.")

    elif p1_score < p2_score:
        players[name2]["victories"] += 1
        players[name1]["defeats"] += 1
        # xp
        p2_xp_inc = random.randint(5, 10)
        p1_xp_inc = random.randint(1, 5)
        players[name1]["xp"] += p1_xp_inc
        players[name2]["xp"] += p2_xp_inc

        # army resources
        p2_bombs_decreased = random.randint(10, 40)
        p1_bombs_decreased = random.randint(40, 70)
        players[name1]["bombs"] = int(players[name1]["bombs"] * (100 - p1_bombs_decreased) / 100)
        players[name2]["bombs"] = int(players[name2]["bombs"] * (100 - p2_bombs_decreased) / 100)

        p2_meds_decreased = random.randint(10, 40)
        p1_meds_decreased = random.randint(40, 70)
        players[name1]["meds"] = int(players[name1]["meds"] * (100 - p1_meds_decreased) / 100)
        players[name2]["meds"] = int(players[name2]["meds"] * (100 - p2_meds_decreased) / 100)

        p2_soldiers_decreased = random.randint(10, 40)
        p1_soldiers_decreased = random.randint(40, 70)
        players[name1]["soldiers"] = int(players[name1]["soldiers"] * (100 - p1_soldiers_decreased) / 100)
        players[name2]["soldiers"] = int(players[name2]["soldiers"] * (100 - p2_soldiers_decreased) / 100)

        p2_tanks_decreased = random.randint(10, 40)
        p1_tanks_decreased = random.randint(40, 70)
        players[name1]["tanks"] = int(players[name1]["tanks"] * (100 - p1_tanks_decreased) / 100)
        players[name2]["tanks"] = int(players[name2]["tanks"] * (100 - p2_tanks_decreased) / 100)

        p2_fighterJets_decreased = random.randint(10, 40)
        p1_fighterJets_decreased = random.randint(40, 70)
        players[name1]["fighterJets"] = int(players[name1]["fighterJets"] * (100 - p1_fighterJets_decreased) / 100)
        players[name2]["fighterJets"] = int(players[name2]["fighterJets"] * (100 - p2_fighterJets_decreased) / 100)

        alpha = random.randint(30, 60)
        p2_coin_gain = int(alpha * players[name1]["coins"] / 100)
        players[name2]["coins"] += p2_coin_gain
        players[name1]["coins"] = int((100 - alpha) * players[name1]["coins"] / 100)
        if p2_coin_gain <= players[name1]["coins"]:
            s = "The battle was won by " + name2
            "\n"
            s += "**** Battle Statistics****\n\n"
            s += "***" + name1 + "***"
            s += "\nCoins Lost = " + str(p2_coin_gain)
            s += "\nXP increased = " + str(p1_xp_inc)
            s += "\nTANKS Lost = " + str(p1_tanks_decreased) + "%"
            s += "\nFIGHTER JETS Lost = " + str(p1_fighterJets_decreased) + "%"
            s += "\nBOMBS Lost = " + str(p1_bombs_decreased) + "%"
            s += "\nSOLDIERS Lost = " + str(p1_soldiers_decreased) + "%"
            s += "\nTANKS Lost = " + str(p1_tanks_decreased) + "%" + "\n\n"

            s += "***" + name2 + "***"
            s += "\nCoins Gained = " + str(p2_coin_gain)
            s += "\nXP increased = " + str(p2_xp_inc)
            s += "\nTANKS Lost = " + str(p2_tanks_decreased) + "%"
            s += "\nFIGHTER JETS Lost = " + str(p2_fighterJets_decreased) + "%"
            s += "\nBOMBS Lost = " + str(p2_bombs_decreased) + "%"
            s += "\nSOLDIERS Lost = " + str(p2_soldiers_decreased) + "%"
            s += "\nTANKS Lost = " + str(p2_tanks_decreased) + "%" + "\n\n"

            await ctx.send(s)
        else:
            await ctx.send(name1 + " is too poor to be attacked.")

    else:
        await ctx.send('Both opponents were found to be of equal power, so fight some other day!')

    with open("players.json", "w") as file:  # updates json file after function execution
        json.dump(players, file)

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def suggest(ctx, txt):
    if txt == 'advice':
        response = requests.get('https://api.adviceslip.com/advice')
        await ctx.send(response.json()['slip']['advice'])

    if txt == 'activity':
        response = requests.get('http://www.boredapi.com/api/activity/')
        await ctx.send(response.json()['activity'])
    if txt == 'song':
        index = random.randint(0,127)
        url = "http://davidpots.com/jakeworry/017%20JSON%20Grouping,%20part%203/data.json"
        response = requests.get(url)
        await ctx.send(response.json()["songs"][index]["title"]+" by "+response.json()['songs'][index]["artist"])

@bot.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def winMoney(ctx, name):
    prize = random.randint(50,500)
    players[name]["coins"] += prize
    await ctx.send("Hurray " + name + " won " + str(prize) + " coins!")
    with open("players.json", "w") as file:  # updates json file after function execution
        json.dump(players, file)


# @bot.command()
# @commands.cooldown(1, 120, commands.BucketType.user)
# async def random(ctx, name1):
#     li_players = []
#     for x in players:
#         li_players.append(x)
#     name2 = random.choice(li_players)
#
#     chance_factor = random.randint(0, 1)
#
#     xp_p1_num = players[name1]["xp"]
#     xp_p2_num = players[name2]["xp"]
#     xp_den = players[name1]["xp"] + players[name2]["xp"]
#     p1_xp = 0.3 * xp_p1_num / xp_den
#     p2_xp = 0.3 * xp_p2_num / xp_den
#
#     bombs_p1_num = players[name1]["bombs"]
#     bombs_p2_num = players[name2]["bombs"]
#     bombs_den = players[name1]["bombs"] + players[name2]["bombs"]
#     p1_bombs = 0.08 * bombs_p1_num / bombs_den
#     p2_bombs = 0.08 * bombs_p2_num / bombs_den
#
#     soldiers_p1_num = players[name1]["soldiers"]
#     soldiers_p2_num = players[name2]["soldiers"]
#     soldiers_den = players[name1]["soldiers"] + players[name2]["soldiers"]
#     p1_soldiers = 0.02 * soldiers_p1_num / soldiers_den
#     p2_soldiers = 0.02 * soldiers_p2_num / soldiers_den
#
#     meds_p1_num = players[name1]["meds"]
#     meds_p2_num = players[name2]["meds"]
#     meds_den = players[name1]["meds"] + players[name2]["meds"]
#     p1_meds = 0.05 * meds_p1_num / meds_den
#     p2_meds = 0.05 * meds_p2_num / meds_den
#
#     fighterJets_p1_num = players[name1]["fighterJets"]
#     fighterJets_p2_num = players[name2]["fighterJets"]
#     fighterJets_den = players[name1]["fighterJets"] + players[name2]["fighterJets"]
#     p1_fighterJets = 0.20 * fighterJets_p1_num / fighterJets_den
#     p2_fighterJets = 0.20 * fighterJets_p2_num / fighterJets_den
#
#     tanks_p1_num = players[name1]["tanks"]
#     tanks_p2_num = players[name2]["tanks"]
#     tanks_den = players[name1]["tanks"] + players[name2]["tanks"]
#     p1_tanks = 0.15 * tanks_p1_num / tanks_den
#     p2_tanks = 0.15 * tanks_p2_num / tanks_den
#
#     if chance_factor == 1:
#         y = 0
#     else:
#         y = 1
#
#     p1_score = p1_xp + p1_meds + p1_bombs + p1_tanks + p1_fighterJets + p1_soldiers + 0.2 * (1 - y)
#     p2_score = p2_xp + p2_meds + p2_bombs + p2_tanks + p1_fighterJets + p2_soldiers + 0.2 * y
#
#     if p1_score > p2_score:
#         players[name1]["victories"] += 1
#         players[name2]["defeats"] += 1
#
#         # xp
#         p1_xp_inc = random.randint(5, 10)
#         p2_xp_inc = random.randint(1, 5)
#         players[name1]["xp"] += p1_xp_inc
#         players[name2]["xp"] += p2_xp_inc
#
#         # army resources
#         p1_bombs_decreased = random.randint(10, 40)
#         p2_bombs_decreased = random.randint(40, 70)
#         players[name1]["bombs"] = int(players[name1]["bombs"] * (100 - p1_bombs_decreased) / 100)
#         players[name2]["bombs"] = int(players[name2]["bombs"] * (100 - p2_bombs_decreased) / 100)
#
#         p1_meds_decreased = random.randint(10, 40)
#         p2_meds_decreased = random.randint(40, 70)
#         players[name1]["meds"] = int(players[name1]["meds"] * (100 - p1_meds_decreased) / 100)
#         players[name2]["meds"] = int(players[name2]["meds"] * (100 - p2_meds_decreased) / 100)
#
#         p1_soldiers_decreased = random.randint(10, 40)
#         p2_soldiers_decreased = random.randint(40, 70)
#         players[name1]["soldiers"] = int(players[name1]["soldiers"] * (100 - p1_soldiers_decreased) / 100)
#         players[name2]["soldiers"] = int(players[name2]["soldiers"] * (100 - p2_soldiers_decreased) / 100)
#
#         p1_tanks_decreased = random.randint(10, 40)
#         p2_tanks_decreased = random.randint(40, 70)
#         players[name1]["tanks"] = int(players[name1]["tanks"] * (100 - p1_tanks_decreased) / 100)
#         players[name2]["tanks"] = int(players[name2]["tanks"] * (100 - p2_tanks_decreased) / 100)
#
#         p1_fighterJets_decreased = random.randint(10, 40)
#         p2_fighterJets_decreased = random.randint(40, 70)
#         players[name1]["fighterJets"] = int(players[name1]["fighterJets"] * (100 - p1_fighterJets_decreased) / 100)
#         players[name2]["fighterJets"] = int(players[name2]["fighterJets"] * (100 - p2_fighterJets_decreased) / 100)
#
#         # wealth
#         alpha = random.randint(30, 60)
#         p1_coin_gain = int(alpha * players[name2]["coins"] / 100)
#         players[name1]["coins"] += p1_coin_gain
#         players[name2]["coins"] = int((100 - alpha) * players[name2]["coins"] / 100)
#
#         s = "The battle was won by " + name1 + "\n"
#         s += "\n**** Battle Statistics****\n\n"
#         s += "***" + name1 + "***"
#         s += "\nCoins Gained = " + str(p1_coin_gain)
#         s += "\nXP increased = " + str(p1_xp_inc)
#         s += "\nTANKS Lost = " + str(p1_tanks_decreased) + "%"
#         s += "\nFIGHTER JETS Lost = " + str(p1_fighterJets_decreased) + "%"
#         s += "\nBOMBS Lost = " + str(p1_bombs_decreased) + "%"
#         s += "\nSOLDIERS Lost = " + str(p1_soldiers_decreased) + "%"
#         s += "\nTANKS Lost = " + str(p1_tanks_decreased) + "%" + "\n\n"
#
#         s += "***" + name2 + "***"
#         s += "\nCoins Lost = " + str(p1_coin_gain)
#         s += "\nXP increased = " + str(p2_xp_inc)
#         s += "\nTANKS Lost = " + str(p2_tanks_decreased) + "%"
#         s += "\nFIGHTER JETS Lost = " + str(p2_fighterJets_decreased) + "%"
#         s += "\nBOMBS Lost = " + str(p2_bombs_decreased) + "%"
#         s += "\nSOLDIERS Lost = " + str(p2_soldiers_decreased) + "%"
#         s += "\nTANKS Lost = " + str(p2_tanks_decreased) + "%" + "\n\n"
#
#         await ctx.send(s)
#
#     elif p1_score < p2_score:
#         players[name2]["victories"] += 1
#         players[name1]["defeats"] += 1
#
#         # xp
#         p2_xp_inc = random.randint(5, 10)
#         p1_xp_inc = random.randint(1, 5)
#         players[name1]["xp"] += p1_xp_inc
#         players[name2]["xp"] += p2_xp_inc
#
#         # army resources
#         p2_bombs_decreased = random.randint(10, 40)
#         p1_bombs_decreased = random.randint(40, 70)
#         players[name1]["bombs"] = int(players[name1]["bombs"] * (100 - p1_bombs_decreased) / 100)
#         players[name2]["bombs"] = int(players[name2]["bombs"] * (100 - p2_bombs_decreased) / 100)
#
#         p2_meds_decreased = random.randint(10, 40)
#         p1_meds_decreased = random.randint(40, 70)
#         players[name1]["meds"] = int(players[name1]["meds"] * (100 - p1_meds_decreased) / 100)
#         players[name2]["meds"] = int(players[name2]["meds"] * (100 - p2_meds_decreased) / 100)
#
#         p2_soldiers_decreased = random.randint(10, 40)
#         p1_soldiers_decreased = random.randint(40, 70)
#         players[name1]["soldiers"] = int(players[name1]["soldiers"] * (100 - p1_soldiers_decreased) / 100)
#         players[name2]["soldiers"] = int(players[name2]["soldiers"] * (100 - p2_soldiers_decreased) / 100)
#
#         p2_tanks_decreased = random.randint(10, 40)
#         p1_tanks_decreased = random.randint(40, 70)
#         players[name1]["tanks"] = int(players[name1]["tanks"] * (100 - p1_tanks_decreased) / 100)
#         players[name2]["tanks"] = int(players[name2]["tanks"] * (100 - p2_tanks_decreased) / 100)
#
#         p2_fighterJets_decreased = random.randint(10, 40)
#         p1_fighterJets_decreased = random.randint(40, 70)
#         players[name1]["fighterJets"] = int(players[name1]["fighterJets"] * (100 - p1_fighterJets_decreased) / 100)
#         players[name2]["fighterJets"] = int(players[name2]["fighterJets"] * (100 - p2_fighterJets_decreased) / 100)
#
#         alpha = random.randint(30, 60)
#         p2_coin_gain = int(alpha * players[name1]["coins"] / 100)
#         players[name2]["coins"] += p2_coin_gain
#         players[name1]["coins"] = int((100 - alpha) * players[name1]["coins"] / 100)
#
#         s = "The battle was won by " + name2
#         "\n"
#         s += "**** Battle Statistics****\n\n"
#         s += "***" + name1 + "***"
#         s += "\nCoins Lost = " + str(p2_coin_gain)
#         s += "\nXP increased = " + str(p1_xp_inc)
#         s += "\nTANKS Lost = " + str(p1_tanks_decreased) + "%"
#         s += "\nFIGHTER JETS Lost = " + str(p1_fighterJets_decreased) + "%"
#         s += "\nBOMBS Lost = " + str(p1_bombs_decreased) + "%"
#         s += "\nSOLDIERS Lost = " + str(p1_soldiers_decreased) + "%"
#         s += "\nTANKS Lost = " + str(p1_tanks_decreased) + "%" + "\n\n"
#
#         s += "***" + name2 + "***"
#         s += "\nCoins Gained = " + str(p2_coin_gain)
#         s += "\nXP increased = " + str(p2_xp_inc)
#         s += "\nTANKS Lost = " + str(p2_tanks_decreased) + "%"
#         s += "\nFIGHTER JETS Lost = " + str(p2_fighterJets_decreased) + "%"
#         s += "\nBOMBS Lost = " + str(p2_bombs_decreased) + "%"
#         s += "\nSOLDIERS Lost = " + str(p2_soldiers_decreased) + "%"
#         s += "\nTANKS Lost = " + str(p2_tanks_decreased) + "%" + "\n\n"
#
#         await ctx.send(s)
#
#     else:
#         await ctx.send('Both opponents were found to be of equal power, so fight some other day!')
#     with open("players.json", "w") as file:  # updates json file after function execution
#         json.dump(players, file)

bot.run(os.getenv('DISCORD_TOKEN'))
