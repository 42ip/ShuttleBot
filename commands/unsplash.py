import requests
import json
import geograpy

async def unsplash(text, channel, message, splashKey):
    placeName = geograpy.get_place_context(text=text)

    if len(placeName.cities) > 0:
        response = requests.get(
            'https://api.unsplash.com/photos/random/?client_id={}&query={}'.format(splashKey,placeName.cities[0]))
        if response.status_code == 200:
            vals = response.json()
            await channel.send('Here is a photo from {} for you :wink:'.format(placeName.cities[0]))
            await channel.send(vals['urls']['small'])

    elif len(placeName.countries) > 0:
        response = requests.get(
            'https://api.unsplash.com/photos/random/?client_id={}&query={}'.format(splashKey,placeName.countries[0]))
        if response.status_code == 200:
            vals = response.json()
            await channel.send('Here is a photo from {} for you :wink:'.format(placeName.countries[0]))
            await channel.send(vals['urls']['small'])
    

    elif len(placeName.regions) > 0:
        response = requests.get(
            'https://api.unsplash.com/photos/random/?client_id={}&query={}'.format(splashKey,placeName.regions[0]))
        if response.status_code == 200:
            vals = response.json()
            await channel.send('Here is a photo from the country {} for you :wink:'.format(placeName.regions[0]))
            await channel.send(vals['urls']['small'])
    
    else:
        await message.reply("A man who is said to be from the ocean stole some of our drives :astronaut:, maybe this unknown place's info was in it <:sadge:886538902352068628>")