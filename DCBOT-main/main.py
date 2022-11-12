import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ui import button, View
import asyncio
import youtube_dl
TOKEN = "ODgzMDEzNTEyNzg2NDc3MTY3.GpSY3T.7JrEY18fXR4uZY1WzOp6-8OJnV8cTnj8vG0SWo"
bot = commands.Bot(command_prefix='!')

url_library = [
    "https://www.youtube.com/watch?v=yspM1TUqxas",
    "https://www.youtube.com/watch?v=UAouLfZO5KA",
    "https://www.youtube.com/watch?v=Bq8tZCgmp6Q",
    "https://youtu.be/K45NwPrscbU",
    "https://youtu.be/y1lLw8M4zEE",
    "https://youtu.be/nRCEJy1JX9U"
]
url_storage = []
VCID1 = 847119740106309686
VCID2 = 856114513756291093
VCID3 = 856114578152488970
VCID4 = 884090500309712947
TXID1 = 847119740106309685
TXID2 = 883433732743233596
TXID3 = 1000635556985851935

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.get_channel(TXID2).send(content="上線囉!", view=initView())

class initView(View):
    @button(label="join 一般")
    async def join1_button_callback(self, button, interaction):
        await interaction.response.send_message('來摟', view=MyView())
        vc = await bot.get_channel(VCID1).connect()
        source = FFmpegPCMAudio("yeah-boy.mp3")
        vc.play(source)

    @button(label="join 二般")
    async def join2_button_callback(self, button, interaction):
        await interaction.response.send_message('來摟', view=MyView())
        vc = await bot.get_channel(VCID2).connect()
        source = FFmpegPCMAudio("yeah-boy.mp3")
        vc.play(source)

    @button(label="join 三般")
    async def join3_button_callback(self, button, interaction):
        await interaction.response.send_message('來摟', view=MyView())
        vc = await bot.get_channel(VCID3).connect()
        source = FFmpegPCMAudio("yeah-boy.mp3")
        vc.play(source)
        
    @button(label="join bot-testing")
    async def join4_button_callback(self, button, interaction):
        await interaction.response.send_message('來摟', view=MyView())
        vc = await bot.get_channel(VCID4).connect()
        source = FFmpegPCMAudio("yeah-boy.mp3")
        vc.play(source)

class MyView(View):

    @button(label="Button 1", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.edit_message(content='button1 clicked!')
        for channel in bot.voice_clients:
            source = FFmpegPCMAudio("kids_woah-6272.mp3")
            player = channel.play(source)

    @button(label="Button 2", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        await interaction.response.edit_message(content="button2 clicked!")
        for channel in bot.voice_clients:
            source = FFmpegPCMAudio("wow-male-voice-65342.mp3")
            player = channel.play(source)

    @button(label="Button 3", row=0, style=discord.ButtonStyle.primary)
    async def third_button_callback(self, button, interaction):
        await interaction.response.edit_message(content="button3 clicked!")
        for channel in bot.voice_clients:
            source = FFmpegPCMAudio("nolikenowatch.mp3")
            player = channel.play(source)

    @button(label="play", row=0, style=discord.ButtonStyle.success)
    async def play_button_callback(self, button, interaction):
        await interaction.response.send_modal(MyModal(title = "youtuble url"))
    
              
                     
    @button(label="leave", row=0, style=discord.ButtonStyle.danger)
    async def leave_button_callback(self, button, interaction):
        for channel in bot.voice_clients:
            await interaction.response.send_message('bye',view = initView())
            return await channel.disconnect()  
    
class PlayView(View):
    @button(label="pause", row=0, style=discord.ButtonStyle.primary)
    async def pause_button_callback(self, button, interaction):
        voice = discord.utils.get(bot.voice_clients, guild = interaction.guild)
        voice.pause()
        await interaction.response.edit_message(content = 'The music is now paused')
        return True     

    @button(label="resume", row=0, style=discord.ButtonStyle.success)
    async def resume_button_callback(self, button, interaction):
        voice = discord.utils.get(bot.voice_clients, guild = interaction.guild)
        voice.resume()
        await interaction.response.edit_message(content = 'Resumed')

    @button(label="stop", row=0, style=discord.ButtonStyle.danger)
    async def stop_button_callback(self, button, interaction):
        voice = discord.utils.get(bot.voice_clients, guild = interaction.guild)
        if voice.is_playing():
            voice.stop()
        await interaction.response.send_message(content = 'The music is now stoped',view = MyView())

                     

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="Youtube URL"))
        
    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Youtube URL", value=self.children[0].value)
        url = self.val
        voice = discord.utils.get(bot.voice_clients, guild = interaction.guild)
        if voice.is_playing():
            voice.stop()
        player = await YTDLSource.from_url(url, loop=bot.loop)
        for channel in bot.voice_clients:
            channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await interaction.response.send_message(content = f"**Now playing:** {player.title}", view=PlayView())

@bot.slash_command(name='play', description='This command plays music')
async def play(ctx, url):
    global url_storage
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        url_storage.append(url)
        return(await ctx.send_response('add to play list'))
    server = ctx.guild
    voice = server.voice_client
    async with ctx.typing():
        url_storage.append(url)
        for url in url_storage:
            player = await YTDLSource.from_url(url, loop=bot.loop)
            url_storage.remove(url)
            voice.play(player)
            await ctx.send_response(f'**Now playing:** {player.title}',view = PlayView())
        ctx.guild.voice_client.play(ctx,url_storage[0])


bot.run(TOKEN)