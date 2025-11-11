import asyncio

import discord
from discord.ext import commands
from shuffler import Shuffler

cfg = Shuffler.open_file("config.json")
TOKEN = cfg.get("token")
DM_DELAY_SECONDS = 1.0
intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")

@bot.command()
async def mikolaj(ctx):
    failed = []
    shuffler = Shuffler("names.json")
    shuffler.start()
    results = shuffler.get_results()
    attendants = shuffler.attendants
    for pair in results["results"]:
        try:
            sender = pair["sender"]
            sender_nick = attendants["attendants"][sender]["nick"]
            receiver = pair["receiver"]
            receiver_nick = attendants["attendants"][receiver]["nick"]
            sender_id = attendants["attendants"][sender]["id"]
            dm_text = (
            f"Ho ho ho! 🎅 Z tej strony Święty Mikołaj!!\n"
            f"Słuchaj, **{sender}**. Mam do Ciebie sprawę...\n"
            f"Te jebane elfy znowu spartoliły robotę.\n"
            f"Pomóż mi, bo inaczej **{receiver}** (znany również pod pseudonimem: **{receiver_nick}**)"
            f" nie dostanie prezentu.\n"
            f"Zrobisz to dla mnie misiaczku? Powodzenia.\n"
            f"Twój, Święty Pan M."
            )
            user = await bot.fetch_user(sender_id)
            await user.send(dm_text)
            await asyncio.sleep(DM_DELAY_SECONDS)
        except Exception as e:
            failed.append((pair["sender"], str(e)))
    if failed:
        msg = "Nie udało się wysłać wiadomości do:\n" + "\n".join([f"- {f[0]} ({f[1]})" for f in failed])
        await ctx.send(msg)
    else:
        await ctx.send("Ho ho ho! 🎅 działa")

@bot.command()
async def test(ctx):
    failed = []
    shuffler = Shuffler("names.json")
    shuffler.start()
    results = shuffler.get_results()
    attendants = shuffler.attendants
    print(results)
    for pair in results["results"]:
        try:
            sender = pair["sender"]
            sender_nick = attendants["attendants"][sender]["nick"]
            receiver = pair["receiver"]
            receiver_nick = attendants["attendants"][receiver]["nick"]
            sender_id = attendants["attendants"][sender]["id"]
            dm_text = (
            f"To jest wiadomość testowa.\n"
            f"Sprawdzamy czy bot na losowanie osób na mikołajki działa.\n"
            f"Nazywasz się {sender} (nick: {sender_nick}).\n"
            f"Daj znać dla x (x) czy dostałeś wiadomość."
            )
            user = await bot.fetch_user(sender_id)
            await user.send(dm_text)
            await asyncio.sleep(DM_DELAY_SECONDS)
        except Exception as e:
            failed.append((pair["sender"], str(e)))
    if failed:
        msg = "Nie udało się wysłać wiadomości do:\n" + "\n".join([f"- {f[0]} ({f[1]})" for f in failed])
        await ctx.send(msg)
    else:
        await ctx.send("Działa")
bot.run(TOKEN)