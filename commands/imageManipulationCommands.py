import requests
from PIL import Image, ImageDraw
import io,random,discord
async def earth(message,channel):
    if len(message.mentions) == 0:
        person = message.author
    else:
        person = message.mentions[0]
        
    response = requests.get(person.avatar_url)
    image_bytes = io.BytesIO(response.content)
    im2 = Image.open(image_bytes)
    response = requests.get(
        'https://cdn.mos.cms.futurecdn.net/3upZx2gxxLpW7MBbnKYQLH-1200-80.jpg')
    image_bytes = io.BytesIO(response.content)
    im1 = Image.open(image_bytes)
    im2 = im2.resize((470, 470))
    mask_im = Image.new("L", im2.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((0, 0, im2.width, im2.height), fill=150 )
    im = im1.copy()
    im.paste(im2, (35, 40), mask_im)

    msgs = ["Zuckerberg told me that you were blue today, well, you are now the Blue Planet! <:deadinside:762920553941303327>",
            "You are now a 12,000 km wide ball called Earth. Congratulations <:poggies:886538902184292393>",
            "I present to you the face of the planet with 7.8 billion people who contributed nothing to the space <:superAngry:843088789349335050>"]

    with io.BytesIO() as image_binary:
        im.save(image_binary, 'PNG')
        image_binary.seek(0)
        picture = discord.File(image_binary, "space.png")
        await channel.send(random.choice(msgs))
        await channel.send(file=picture)