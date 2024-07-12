import discord
import logging
import random
from discord.ext import commands

import TournamentsParser as prs

try:
    with open("TOKEN.txt", 'r') as token_file:
        token = token_file.read()
except FileNotFoundError:
    print("Файл с токеном не найден, создайте файл \"TOKEN.txt\" и поместите в него токен своего дискорд бота")
    token = None
prefix = '!'
intents = discord.Intents().all()

bot = commands.Bot(command_prefix=prefix, intents=intents)
logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def choose_mode(mode, dct):
    answ = []
    for key in dct:
        if dct[key]["type"] == mode.lower():
            answ.append(key)
    return answ


@bot.command()
async def айда(ctx):
    logging.info(f"{ctx.author} использовал команду айда")
    await ctx.reply(f"Г{'O'*random.randint(5,19)}ЙДААА")


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.guild)
async def вывести(ctx, *args):
    logging.info(f"{ctx.author} использовал команду вывести с параметрами {args}")
    json_data = prs.read_from_json()
    tourn = []
    settings = {}
    if args:
        for arg in args:
            if arg in ('1x1','2x2','3x3','4x4','5x5'):
                settings["players"] = arg
            elif arg in ('авиа','корабл','наземн','танк','смеш'):
                if arg in 'танк':
                    settings['veh'] = 'наземн'
                else:
                    settings['veh'] = arg
            elif arg in ('рб','аб','сб','рбм'):
                settings['type'] = arg
        for i in json_data.keys():
            if set(settings.items()).issubset(set(json_data[i].items())):
                tourn.append(i)

    else:
        tourn = list(json_data.keys())
    if tourn:
        for el in tourn:
            embed = discord.Embed(
                description=json_data[el]["date"],
                title=el
            )
            embed.set_thumbnail(url=json_data[el]["img_src"])
            view = discord.ui.View()
            button = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Подробнее", url=json_data[el]["href"])
            view.add_item(button)
            await ctx.send(embed=embed, view=view)
    else:
        await ctx.send('По заданному фильтру ничего не найдено')


@вывести.error
async def вывести_error(ctx: discord, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Подождите {error.retry_after:.2f} секунд перед повторным использованием команды")


@bot.command()
async def хелп(ctx):
    await ctx.reply(
    """
    Я умею:
    !вывести (рб, рбм, аб, сб) (1x1, 2x2, 3x3, 4x4, 5x5) (авиа, наземн, смеш, корабл)  -  Главная команда ради которой он и создавался
    !айда  -  Интересно что я делаю? Попробуй, узнаешь
    """
    )


if __name__ == "__main__":
    if token:
        if input("Обновить базу данных турниров? (y/n)").lower() in ('y', ''):
            print("Обновляем базу данных, ожидайте...")
            prs.update_json()
        bot.run(token)