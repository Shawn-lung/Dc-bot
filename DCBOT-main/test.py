import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run("ODgzMDEzNTEyNzg2NDc3MTY3.GpSY3T.7JrEY18fXR4uZY1WzOp6-8OJnV8cTnj8vG0SWo")
