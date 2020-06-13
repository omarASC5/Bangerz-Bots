import discord
from discord.ext import commands
from discord.utils import get
import os
import config as c
import youtube_dl
# import spotipy.util as util
# from bottle import route, run, request
# from spotipy.oauth2 import SpotifyClientCredentials
# import requests
# import user_playlists as playlists 
# pip install asyncio
# python3 -m pip install discord.py
# python3 -m pip install spotipy
# python3 -m pip install youtubedl
players = {}

test_song = 'spotify:track:4evmHXcjt3bTUHD1cvny97'

# client_credentials_manager = SpotifyClientCredentials(c.SPOTIFY_CLIENT_ID, client_secret=c.SPOTIFY_CLIENT_SECRET)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# results = sp.search(q='Drake', limit=20)
# for i, t in enumerate(results['tracks']['items']):
#     print (' ', i, t['name'])

import sys
import spotipy
import spotipy.oauth2 as oauth2

import pafy
import vlc

import urllib.request
from bs4 import BeautifulSoup

import asyncio
# time.sleep(120)

credentials = oauth2.SpotifyClientCredentials(
	client_id=c.SPOTIFY_CLIENT_ID,
	client_secret=c.SPOTIFY_CLIENT_SECRET)

token = credentials.get_access_token(as_dict=False)
spotify = spotipy.Spotify(auth=token)
playlists_table = {}
username = ""

# TODO: MAKE PLAYLISTS PUBLIC THAT YOU WANT TO BE ACCESSIBLE THROUGH THE COMMAND

def show_tracks(tracks, playlists_table, playlist_name):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        try:
            playlists_table[playlist_name].add((track['artists'][0]['name'], track['name']))
        except:
            continue
        # print()
        # print("   %d %32.32s %s" % (i, track['artists'][0]['name'],track['name']))


if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Whoops, need your username!")
    print("usage: python user_playlists.py [username]")
    sys.exit()


if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        # print()
        playlists_table[playlist['name']] = set()
        print(playlist['name'])
        # print ('  total tracks', playlist['tracks']['total'])
        results = sp.playlist(playlist['id'],
            fields="tracks,next")
        tracks = results['tracks']
        show_tracks(tracks, playlists_table, playlist['name'])
        while tracks['next']:
            tracks = sp.next(tracks)
            show_tracks(tracks, playlists_table, playlist['name'])
else:
    print("Can't get token for", username)

# print('yerrrr', playlists.username)
#sp.start_playback({"context_uri": test_song})
client = commands.Bot(command_prefix='$')
print(playlists_table.keys())
print(username)

# import pafy
# import vlc



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

@client.command(pass_context=True, aliases=['j, joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You aren't connected to a voice channel, my friend. :face_with_hand_over_mouth:")
        return
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
# @client.command()
# async def join(ctx):
#     channel = ctx.message.author.voice.channel
#     if not channel:
#         await ctx.send("You aren't connected to a voice channel, my friend. :face_with_hand_over_mouth:")
#         return
    
#     else:
#         voice = await channel.connect()

# TODO: Only allow song commands in the song channel
@client.command(pass_context=True, aliases=['y'])
async def yt(ctx, url : str):
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting song ready now")
    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading audio now\n')
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith('.mp3'):
            name = file
            print("Renamed File: {}".format(name), end='\n\n')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print(f'{name} has finished playing'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.2

    nname = name.rsplit('-', 2)
    await ctx.send(f'Playing {nname}')
    print('playing\n')

@client.command()
async def play(ctx):
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    textToSearch = 'toosie slide'
    query = urllib.parse.quote(textToSearch)
    youtube_URL = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(youtube_URL)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    youtubeResults = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        youtubeResults.append('https://www.youtube.com' + vid['href'])
        # print('https://www.youtube.com' + vid['href'])

    # youtube_URL = "https://www.youtube.com/watch?v=xWggTb45brM"
    for youtube_result in youtubeResults:
        try:
            video = pafy.new(youtube_result)
        except:
            continue

    best = video.getbest()
    playurl = best.url

    # NOTE: THE FOLLOWING TWO LINES OF CODE ARE RESPONSIBLE FOR  VIDEO STREAMING OF YOUTUBE VIDEOS
    # player = vlc.MediaPlayer(playurl)
    # player.play()


    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    vc.play(player.play())
    # player.play()
    # print(r.content)
    # vc.play(sp.start_playback({"context_uri": test_song}))
    # vc.play(discord.FFmpegPCMAudio('Nick Jonas - The Difference (Audio).mp3'), after=lambda e: print('done', e))

@client.command()
async def leave(ctx):
    guild = ctx.message.guild
    voice_client = guild.voice_client
    await voice_client.disconnect()




# @client.command(pass_context=True)
# async def yt(ctx, url):
#     # TODO: https://www.youtube.com/watch?v=Bp9SZYqIWIM
#     vc = await channel.connect()
#     vc.play(discord.FFmpegPCMAudio(executable="C:/path/ffmpeg.exe", source="mp3.mp3"))

# client.add_cog(YTDLSource(client))
client.run(c.DISCORD_TOKEN)
