import discord

async def help(message):
    commands = ["1. hello : Know the bot",
                "2. apod : Astronomical Picture Of The Day",
                "3. mars : NAVCAM picture from planet Mars", 
                "4. earth: Become the planet Earth, a 6 septillion kg blue ball",
                "5. plot : DM the nearest satellite for a new movie plot",
                "6. splash: Generate random photos. Use >splash help to learn more",
                "7. travel : Enter 'travel <placeName>' to get an image from there" ]
    msg = "Hey, heard a SOS! Here's all you need to know: \n Prefix : > \n"
    for val in commands:
        msg += val + '\n'
    await message.reply(msg)