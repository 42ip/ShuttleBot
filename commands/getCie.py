# Code to scrape the results of any student from "http://exam.msrit.edu/"
from collections import defaultdict
import requests
from bs4 import BeautifulSoup as bs
import json,sys
import discord
import pandas as pd
import re
# import dataframe_image as dfi
import matplotlib.pyplot as plt
from PIL import Image
import io

async def createDataFrameAndSaveImage(d,author,name):
    subjectindices = [capt for capt in d]
    columns = d[subjectindices[0]][0] if name == 'cie' else ['Attended','Absent','Remaining','Percentage']
    rowdata = [d[capt][1] for capt in d] if name == 'cie' else [d[capt] for capt in d]
    df = None
    df = pd.DataFrame(rowdata,columns=columns)
    df.index = subjectindices
    f = plt.figure(figsize=(50,50/3))
    f.tight_layout()
    ax = f.add_subplot(1,1,1, frame_on=False) # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)
    ax.axis('tight')
   
    tab = pd.plotting.table(ax,df,cellLoc = 'center', rowLoc = 'center',loc='center')
    table_props=tab.properties()
    # print(table_props)
    table_cells=table_props['celld']
    for cell in table_cells.values():
        cell.set_width(0.8)
        cell.set_height(0.065)
        cell.set_fontsize(12)
    for i in range(0, len(df.columns)):
        for j in range(0,len(df) + 1):
            cell = tab[j, i]
            cell.set_height(0.1)
    tab.set_fontsize(25)

    tab.auto_set_column_width(range(0,len(df.columns)))
    plt.savefig(sys.path[0] + "/{}.png".format(name),transparent=True,pad_inches=0)
    # df_styled = df.style.background_gradient() #adding a gradient based on values in cell
    # dfi.export(df_styled,sys.path[0] + "/{}.png".format(name))
    im = Image.open(sys.path[0] + "/{}.png".format(name))
    with io.BytesIO() as image_binary:
        im.save(image_binary, 'PNG')
        image_binary.seek(0)
        picture = discord.File(image_binary, "{}.png".format(name))
        # await author.send("")
        await author.send(file=picture)

async def getCie(response,message,channel,getcie):
    isthere  = False
    ctx = message
    author = message.author.id
    # user= await client.get_user_info(author)
    isNotPrivate = True
    if isinstance(ctx.channel, discord.channel.DMChannel):
        isNotPrivate = False
    if isNotPrivate:
        await channel.send("Please dm me ;) i wont give cie stuff in groups")
        await message.author.send("Message me here with the command ``` >cie your_usn yyyy-mm-dd if you arent registered or just >cie ``` ")
        # await client.delete_message(message)
        return

    vals = response.split()
    username = password = " "
    if len(vals) == 1:
        j = {}
        with open('auth.json','r') as f:
            j = json.loads(f.read())
        if message.author.id in j:
            username,password = j[message.author.id]['username'],j['password']
        else:
            await message.author.send("You arent registered :( run the command in the following manner : ``` >cie your_usn yyyy-mm-dd ```")
            return
    elif len(vals) == 3:
        # assuming person is signing in. this will overwrite creds
        username = vals[1]
        password = vals[2]
        isthere = False
        j = {}
        with open('auth.json','r') as f:
            j = json.load(f)
        if message.author.id in j: isthere = True
        j[message.author.id] = {'username':username,'password':password}
        await message.author.send("Ah! i see you're updating <wink> " if isthere else "Welcome {} ! I'll send you your Cie stuff shortly..".format(message.author))
        with open('auth.json','w') as f:
            json.dump(j,f)

    data = {'task': 'login', 'option':'com_user','username': username,'passwd': password}
    with requests.Session() as s:
        s.verify = True
        # First sending log in data
        a = s.post("http://parents.msrit.edu/",data=data)
        scode1 = a.status_code
        # logging in
        a = s.get("http://parents.msrit.edu/",auth=(username,password))
        scode2 = a.status_code
        if scode1 != scode2 != 200:
            await message.author.send("Somethings wrong :( Try registering again" )
            return
        # getting the subject data
        r2 = s.get("http://parents.msrit.edu/index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard")
        soup = bs(r2.text,'lxml') 
        # each value in the indices array will link to the subject page of particular subject   
        indices = []
        aindices = []
        for a in soup.findAll('a', href=True):
            if 'ciedetails' in a['href']:
                indices.append(a['href'])
            elif 'attendencelist' in a['href']:
                aindices.append(a['href'])
        if getcie:
            headers = []
            subjects = []
            d = defaultdict(list)
            for site in indices:
                r = s.get("http://parents.msrit.edu/{}".format(site))
                soup = bs(r.text, 'lxml')
                capt = soup.find('caption').contents[0]  # type:ignore
                table = soup.find(
                    'table', {'class': 'uk-table cn-cie-table uk-table-responsive'})
                headers = []
                datas = []
                for header in table.findAll('th'):  # type:ignore
                    headers.append(header.contents[0].replace(" ", ""))
                    # headers.append(header.contents[0].replace(" ","") + '\t')
                for data in table.findAll('td'):  # type:ignore
                    datas.append(data.contents[0].replace(" ", ""))
                    # datas.append(data.contents[0].replace(" ","") + '\t')
                datas[7] += ''
                datas[8] += ''
                d[capt] = [headers, datas]
                headers = d[capt][0]
            await createDataFrameAndSaveImage(d,message.author,'cie')
            # print(ta([headers] + [d[i][1] for i in d ],tablefmt="fancy_grid",showindex=[''] + [i for i in d]))
            # for i in d:
            # print(i)
            # print(ta([d[i][0],d[i][1]],tablefmt="fancy_grid"))
            #     print(ta([d[i][0],d[i][1]]))

        else:
            d2 = {}
            for site in aindices:
                r = s.get("http://parents.msrit.edu/{}".format(site))
                soup = bs(r.text, 'lxml')
                capt = soup.find('div', {
                                'class': 'md-card-head md-bg-light-blue-600 uk-flex'}).find('span').contents[0]
                nos = re.findall('\[.*\]', soup.text)
                wantmarks = [x[1:-1] for x in nos]
                perc = 0
                perc = int(
                    int(wantmarks[0]) / sum([int(i) if i != '' else 0 for i in wantmarks[:-1]]) * 100)
                wantmarks[0] = "Attended: " + wantmarks[0]
                wantmarks[1] = "Absent: " + wantmarks[1]
                wantmarks[2] = "Remaining: " + wantmarks[2]
                wantmarks.append("You have {}% attendance".format(perc))
                d2[capt] = wantmarks
            await createDataFrameAndSaveImage(d2,message.author,'attendance')
        # print(ta([d2[i] for i in d2], tablefmt="fancy_grid",
        #       showindex=[i for i in d2]))
        
        # response = "Here are your CIE details: \n"
        # for i in d:
        #     response += i + '\n'
        #     response += "".join(d[i][0]) + "\n"
        #     response += "".join(d[i][1]) + "\n"
        #     response += "\n"
        # await message.author.send(response)
