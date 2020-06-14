import discord
from discord.ext import commands
from discord.utils import get
import os
import config as c
import youtube_dl
import random
import asyncio
import shutil
import time
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
f = open("username.txt", "r")
sp_username = str(f.readline())
# TODO: MAKE PLAYLISTS PUBLIC THAT YOU WANT TO BE ACCESSIBLE THROUGH THE COMMAND
if sp_username != "":
    def show_tracks(tracks, playlists_table, playlist_name):
        for i, item in enumerate(tracks['items']):
            track = item['track']
            try:
                playlists_table[playlist_name].append((track['artists'][0]['name'], track['name']))
            except:
                continue
            # print()
            # print("   %d %32.32s %s" % (i, track['artists'][0]['name'],track['name']))
    if token:
        sp2 = spotipy.Spotify(auth=token)
        playlists = sp2.user_playlists(sp_username)
        for playlist in playlists['items']:
            # print()
            playlists_table[playlist['name']] = list()
            print(playlist['name'])
            # print ('  total tracks', playlist['tracks']['total'])
            results = sp2.playlist(playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks, playlists_table, playlist['name'])
            while tracks['next']:
                tracks = sp2.next(tracks)
                show_tracks(tracks, playlists_table, playlist['name'])
    else:
        print("Can't get token for", sp_username)

    print(playlists_table.keys())
    print(sp_username)


# print('yerrrr', playlists.username)
#sp.start_playback({"context_uri": test_song})
client = commands.Bot(command_prefix='$')


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

@client.command(pass_context=True)
async def username(ctx, new_username=''):
    sp_username = str(new_username)
    f = open('username.txt', 'w')
    f.write(sp_username)
    f.close()
    await ctx.send(f'Username {sp_username} successfully stored!')
    playlists_table.clear()
    if sp_username != "":
        def show_tracks(tracks, playlists_table, playlist_name):
            for i, item in enumerate(tracks['items']):
                track = item['track']
                try:
                    playlists_table[playlist_name].append((track['artists'][0]['name'], track['name']))
                except:
                    continue
                # print()
                # print("   %d %32.32s %s" % (i, track['artists'][0]['name'],track['name']))
        if token:
            sp2 = spotipy.Spotify(auth=token)
            playlists = sp2.user_playlists(sp_username)
            for playlist in playlists['items']:
                # print()
                playlists_table[playlist['name']] = list()
                print(playlist['name'])
                # print ('  total tracks', playlist['tracks']['total'])
                results = sp2.playlist(playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks, playlists_table, playlist['name'])
                while tracks['next']:
                    tracks = sp2.next(tracks)
                    show_tracks(tracks, playlists_table, playlist['name'])
        else:
            print("Can't get token for", sp_username)

        print(playlists_table.keys())
        print(sp_username)
    else:
        
        def show_tracks(tracks, playlists_table, playlist_name):
            for i, item in enumerate(tracks['items']):
                track = item['track']
                try:
                    playlists_table[playlist_name].append((track['artists'][0]['name'], track['name']))
                except:
                    continue
                # print()
                # print("   %d %32.32s %s" % (i, track['artists'][0]['name'],track['name']))
        if token:
            sp2 = spotipy.Spotify(auth=token)
            playlists = sp2.user_playlists(sp_username)
            for playlist in playlists['items']:
                # print()
                playlists_table[playlist['name']] = list()
                print(playlist['name'])
                # print ('  total tracks', playlist['tracks']['total'])
                results = sp2.playlist(playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks, playlists_table, playlist['name'])
                while tracks['next']:
                    tracks = sp2.next(tracks)
                    show_tracks(tracks, playlists_table, playlist['name'])
        else:
            print("Can't get token for", sp_username)

        print(playlists_table.keys())
        print(sp_username)

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

queues = {}
# TODO: Only allow song commands in the song channel
@client.command(pass_context=True)
async def yt(ctx, search : str):
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

    url = search
    def check_queue():
        Queue_infile = os.path.isdir('./Queue')
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath('Queue'))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queue song(s)")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath('Queue') + '\\' + first_file)
            if length != 0:
                print('Song done, playing next queued')
                print(f'Songs still in queue: {still_q}')
                song_there = os.path.isfile('song.mp3')
                if song_there:
                    os.remove('song.mp3')
                shutil.move(song_path, main_location)
                for file in os.listdir('./'):
                    if file.endswith('.mp3'):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.5

            else:
                queues.clear()
                return
        else:
            queues.clear()
            print('No songs were queued before the ending of the last song\n')

    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir('./Queue')
    try:
        Queue_folder = './Queue'
        if Queue_infile is True:
            print('Removed old Queue Folder')
            shutil.rmtree(Queue_folder)
    except:
        print('No old Queue folder')

    await ctx.send("Getting song ready now")
    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'default_search': 'ytsearch'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading audio now\n')
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith('.mp3'):
            name = file
            print("Renamed File: {}".format(name), end='\n\n')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.5

    if name:
        nname = name.rsplit('-', 2)
    await ctx.send(f'Playing: {nname[1]} by {nname[0]}')
    print('playing\n')
    # best = video.getbest()
    # playurl = best.url

    # NOTE: THE FOLLOWING TWO LINES OF CODE ARE RESPONSIBLE FOR  VIDEO STREAMING OF YOUTUBE VIDEOS
    # player = vlc.MediaPlayer(playurl)
    # player.play()


    # Instance = vlc.Instance()
    # player = Instance.media_player_new()
    # Media = Instance.media_new(playurl)
    # Media.get_mrl()
    # player.set_media(Media)
    # vc.play(player.play())
    # player.play()
    # print(r.content)
    # vc.play(sp.start_playback({"context_uri": test_song}))
    # vc.play(discord.FFmpegPCMAudio('Nick Jonas - The Difference (Audio).mp3'), after=lambda e: print('done', e))

@client.command()
async def sp_playlists(ctx):
    if sp_username == "":
        await ctx.send('Please set a spotify username with command: $username [your_username]')

    index = 1
    for playlist in playlists_table.keys():
        await ctx.send(f'{index}. {playlist}')
        index += 1
    await ctx.send('Please call command: $sp_playlist (without the s at the end) with a playlist number')

@client.command()
async def sp_playlist(ctx, index : int, shuffle = ""):
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

    i = 1
    found_playlist = ''
    found_songs = []
    for playlist, songs in playlists_table.items():
        if i == index:
            found_playlist = playlist
            found_songs = songs
            break
        i += 1
    await ctx.send(f'Found playlist: {found_playlist}')
    random_song = random.choice(found_songs)
    await ctx.send(f'Playing: {random_song[1]} by {random_song[0]}')
    url = random_song[1] + " " + random_song[0]
    def check_queue():
        Queue_infile = os.path.isdir('./Queue')
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath('Queue'))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queue song(s)")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath('Queue') + '\\' + first_file)
            if length != 0:
                print('Song done, playing next queued')
                print(f'Songs still in queue: {still_q}')
                song_there = os.path.isfile('song.mp3')
                if song_there:
                    os.remove('song.mp3')
                shutil.move(song_path, main_location)
                for file in os.listdir('./'):
                    if file.endswith('.mp3'):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.5

            else:
                queues.clear()
                return
        else:
            queues.clear()
            print('No songs were queued before the ending of the last song\n')

    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir('./Queue')
    try:
        Queue_folder = './Queue'
        if Queue_infile is True:
            print('Removed old Queue Folder')
            shutil.rmtree(Queue_folder)
    except:
        print('No old Queue folder')

    await ctx.send("Getting song ready now")
    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'default_search': 'ytsearch'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading audio now\n')
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith('.mp3'):
            name = file
            print("Renamed File: {}".format(name), end='\n\n')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.5

    if name:
        nname = name.rsplit('-', 2)
    await ctx.send(f'Playing: {nname[1]} by {nname[0]}')
    print('playing\n')
    
    def q2(url):
        Queue_infile = os.path.isdir('./Queue')
        if Queue_infile is False:
            os.mkdir('Queue')

        DIR = os.path.abspath(os.path.realpath('Queue'))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True

        while add_queue:
            if q_num in queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num

        queue_path = os.path.abspath(os.path.realpath('Queue') + f'\song{q_num}.%(ext)s')

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'default_search': 'ytsearch'
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading audio now\n')
            ydl.download([url])
        # await ctx.send('Adding song ' + str(q_num) + ' to the queue')

        print('Song added to queue')

    def next_song():
        random_song = random.choice(found_songs)
        print('playing', random_song)
        url = random_song[1] + " " + random_song[0]
        q2(url)
        return random_song

    for _ in range(10):
        next_song_name = next_song()
        # Playing next: {song_name} by {artist}
        await ctx.send(f'Playing next: {next_song_name[1]} by {next_song_name[0]}')

    while True:
        for _ in range(5):
            next_song_name = next_song()
            # Playing next: {song_name} by {artist}
            await ctx.send(f'Playing next: {next_song_name[1]} by {next_song_name[0]}')
            await asyncio.sleep(250)
    # If the queue is empty add 10 more songs

    # search(random_song[1])

@client.command(pass_context=True, aliases=['pa, pau'])
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()

        await ctx.send("Music paused")

    else:
        print("Music not playing: failed pause")
        await ctx.send("Music not playing: failed pause")

@client.command(pass_context=True, aliases=['re, res'])
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")

    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")

@client.command(pass_context=True, aliases=['s, ski'])
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    
    queues.clear()
    
    if voice and voice.is_playing():
        print("Music skipped")
        voice.stop()
        await ctx.send("Music skipped")

    else:
        print("No music playing: failed to skip")
        await ctx.send("No music playing: failed to skip")

@client.command()
async def leave(ctx):
    guild = ctx.message.guild
    voice_client = guild.voice_client
    await voice_client.disconnect()


@client.command(pass_context=True, aliases=['q, que'])
async def queue(ctx, search : str):
    url = search
    Queue_infile = os.path.isdir('./Queue')
    if Queue_infile is False:
        os.mkdir('Queue')

    DIR = os.path.abspath(os.path.realpath('Queue'))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True

    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath('Queue') + f'\song{q_num}.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'default_search': 'ytsearch'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading audio now\n')
        ydl.download([url])
    await ctx.send('Adding song ' + str(q_num) + ' to the queue')

    print('Song added to queue')
client.run(c.DISCORD_TOKEN)
