import gpt_2_simple as gpt2

async def plot(channel,session):
    await channel.send('Contacting the nearest satellite for a new movie plot <:peepobigbrain:863049707361665024>')
    text = gpt2.generate(session, run_name='run1',
    length=50,
    prefix="<|startoftext|>",
    truncate="<|endoftext|>\n",
    include_prefix=False,return_as_list = True)
    # print(text[0])
    await channel.send(text[0])