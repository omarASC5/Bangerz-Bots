import discord
import spotipy
from discord.ext import commands
import config as c
import youtube_dl

players = {}

sp = spotipy.Spotify()
test_song = 'spotify:track:4evmHXcjt3bTUHD1cvny97'

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(c.SPOTIFY_CLIENT_ID, client_secret=c.SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

results = sp.search(q='Drake', limit=20)
for i, t in enumerate(results['tracks']['items']):
    print (' ', i, t['name'])


#sp.start_playback({"context_uri": test_song})
client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(activity=discord.Game(name="Playing straight 🔥🔥🔥"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')
        
    if 'gang' in message.content.lower():
        await message.channel.send('gang gang 💯')
        
    if 'pop out' in message.content.lower():
        await message.channel.send("I'm with the Gang.")
        
    if 'dad' in message.content.lower():
        await message.channel.send("Big Daddy, what up?")  
    await client.process_commands(message)

@client.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(client.latency, 1)))

@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You aren't connected to a voice channel, my friend. :face_with_hand_over_mouth:")
        return
    
    else:
        voice = await channel.connect()
        
@client.command()
async def play(ctx):
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
   # vc.play(sp.start_playback({"context_uri": test_song}))
    vc.play(discord.FFmpegPCMAudio('Nick Jonas - The Difference (Audio).mp3'), after=lambda e: print('done', e))

@client.command()
async def leave(ctx):
    guild = ctx.message.guild
    voice_client = guild.voice_client
    await voice_client.disconnect()


@client.command()
async def yt(ctx, url):
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    player = await vc.create_ytdl_player(url)
    vc.play(player)
client.run(c.TOKEN)
