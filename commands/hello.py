import discord
import random

async def hello(introList,channel):
    embedVar = discord.Embed(title="Hey, My name is Shuttle.",description=random.choice(introList),color=0x00ffff)
    embedVar.set_thumbnail(url = 'attachment://shuttleLogo.png')
    await channel.send(embed= embedVar)