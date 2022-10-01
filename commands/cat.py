import discord
import os
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io


async def pussi(message, channel):
    x = message.split()
    imgtype = 'gif'
    while imgtype == 'gif':
        im_url = requests.get("https://aws.random.cat/meow")
        json_data = json.loads(im_url.text)
        imgtype = json_data['file'][-3:]

    response = requests.get(json_data['file'])
    image_bytes = io.BytesIO(response.content)
    im = Image.open(image_bytes).convert("RGB")
    draw = ImageDraw.Draw(im)
    w, h = im.size
    font = ImageFont.truetype("../fonts/Poppins-Regular.ttf", w//15)
    para = textwrap.wrap(' '.join(x[1:]), width=w//2)
    pad = 15
    H = 0
    for line in para:
        draw.text((0, H), line, (255, 255, 255), font=font)
        H = H + pad

    with io.BytesIO() as image_binary:
        type = "PNG"
        im.save(image_binary, type)
        image_binary.seek(0)
        picture = discord.File(image_binary, "pussi." + type.lower())
        await channel.send(file=picture)
