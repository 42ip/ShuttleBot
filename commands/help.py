import discord

async def help(message):
    commands = [("hello","Know the bot"),
                ("apod","Astronomical Picture Of The Day"),
                ("mars","NAVCAM picture from planet Mars"), 
                ("earth","Become the planet Earth, a 6 septillion kg blue ball"),
                ("plot","DM the nearest satellite for a new movie plot"),
                ("splash","Generate random photos. Use >splash help to learn more"),
                ("travel","Enter 'travel <placeName>' to get an image from there"),
                ("cie","Get all your exam details DM'd to you"),
                ("attendance","Get all your attendance details DM'd to you") ]
    embed = discord.Embed(title="Shuttle has arrived to help",description="I can run any of the below command",color=0x00ffff)
    for k,v in commands:
        embed.add_field(name=k,value=v,inline=False)
    # msg = "Hey, heard a SOS! Here's all you need to know: \n Prefix : > \n"
    # for val in commands:
    #     msg += val + '\n'
    # await message.reply(msg)
    await message.channel.send(embed = embed)