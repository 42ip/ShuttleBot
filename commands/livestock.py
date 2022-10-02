import json,sys 
from random import randint
link  = "http://inaph.nddb.coop/Chart/AnimalRegistered"



async def livestock(message,channel):
    # x = message.split()
    data = {}
    givetot = randint(0,1) == 1
    ret = []
    with open(sys.path[0] + "/file.json",'r') as f:
        data = json.loads(f.read())
        names = [k for k in data["Karnataka"].keys()]
        data = data["Karnataka"]
        names.remove("districts")
        key = names[randint(0,len(names) - 1)]
        if (givetot):
            ret.append((key,("total " if "total" not in key.lower() else "")+ key + " In karnataka : "  + "{}".format(data[key])))
        else:
            district = data["districts"]
            district = data["districts"][randint(0,len(district) - 1)]
            ret.append((key,key + " in " + district['District name'] + " , Karnataka : " + "{}".format(district[key])))

        embed = discord.Embed(title="Shuttle has beamed up the " + key,
                          description="Here is what i found", color=0x00ffff)
        for k, v in ret:
            embed.add_field(name=k, value=v, inline=False)
        await message.channel.send(embed=embed)





