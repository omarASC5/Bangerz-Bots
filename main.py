import discord
from discord.ext import commands
from discord.utils import get
import os
from SpotifyProcessor import SpotifyProcessor
from Music import Music
import youtube_dl
import random
import asyncio
import shutil
import time
import sys
import spotipy
import spotipy.oauth2 as oauth2
import asyncio
from config import *

spotify_processor = SpotifyProcessor(
    os.environ["SPOTIFY_CLIENT_ID"],
    os.environ["SPOTIFY_CLIENT_SECRET"],
    str(open("username.txt", "r").readline())
)

# Loads the list of playlist names
spotify_processor.fill_playlists_names()

# Gets the public playlist names under the account
playlists_names = spotify_processor.playlists_names

# Print the playlists under the account
for val, playlists_name in enumerate(playlists_names):
    print(f'{val + 1}.', playlists_name)

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

@client.command(pass_context=True)
async def username(ctx, new_username=''):
    sp_username = str(new_username)
    f = open('username.txt', 'w')
    f.write(sp_username)
    f.close()

    # Set the username of the user to the object
    spotify_processor.spotify_username = sp_username

    # CLear all exisiting variables and recreate with new username
    spotify_processor.__init__(
        os.environ["SPOTIFY_CLIENT_ID"],
        os.environ["SPOTIFY_CLIENT_SECRET"],
        str(open("username.txt", "r").readline())
    )

    # Loads the list of playlist names
    spotify_processor.fill_playlists_names()

    # Gets the public playlist names under the account
    playlists_names = spotify_processor.playlists_names

    # Print the playlists under the account
    for val, playlists_name in enumerate(playlists_names):
        print(f'{val + 1}.', playlists_name)

    await ctx.send(f'Username {sp_username} successfully stored!')
    
@client.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(client.latency, 1)))

@client.command(pass_context=True, aliases=['j, joi'])
async def join(ctx):
    await bot_join_voice(ctx)

queues = {}

def check_queue(voice):
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
        
        song_path = os.path.abspath(os.path.realpath('Queue') + '/' + first_file)
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

            voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue(voice))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.5

        else:
            queues.clear()
            return
    else:
        queues.clear()
        print('No songs were queued before the ending of the last song\n')

def bot_remove_old_queue_folder():
    Queue_infile = os.path.isdir('./Queue')
    try:
        Queue_folder = './Queue'
        if Queue_infile is True:
            print('Removed old Queue Folder')
            shutil.rmtree(Queue_folder)
    except:
        print('No old Queue folder')

async def bot_join_voice(ctx):
    '''A helper function that allows to join the voice channel the user is in.
        If the user is not currently in a voice channel, it will say that.'''
    global voice
    message_to_send = ''
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        message_to_send = \
        "You aren't connected to a voice channel, my friend. :face_with_hand_over_mouth:"
        await ctx.send(message_to_send)
        return False

    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    return voice

# TODO: Only allow song commands in the song channel
@client.command(pass_context=True)
async def yt(ctx, search : str):
    voice = await bot_join_voice(ctx)
    if not voice:
        return
        
    url = search

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

    bot_remove_old_queue_folder()

    await ctx.send("Getting song ready now")
    voice = get(client.voice_clients, guild=ctx.guild)

    music = Music()
    music.download_song(url)

    for file in os.listdir("./"):
        if file.endswith('.mp3'):
            name = file
            print("Renamed File: {}".format(name), end='\n\n')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue(voice))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.5

    if name:
        nname = name.rsplit('-', 2)
        await ctx.send(f'Playing: {nname[1]} by {nname[0]}')
    print('playing\n')

@client.command()
async def sp_playlists(ctx):
    if spotify_processor.spotify_username == "":
        await ctx.send('Please set a spotify username with command: $username [your_username]')
    else:

        # Gets the public playlist names under the account
        playlists_names = spotify_processor.playlists_names

        # Print the playlists under the account
        str_to_print = '';
        for val, playlists_name in enumerate(playlists_names):
            str_to_print += f'{val + 1}. {playlists_name}\n'
        await ctx.send(f'''```{str_to_print}```''')

    await ctx.send('Please call command: $sp_playlist (without the s at the end) with a playlist number')

@client.command()
async def sp_playlist(ctx, index : int, shuffle = ""):
    voice = await bot_join_voice(ctx)
    if not voice:
        return

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

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue(voice))
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

        queue_path = os.path.abspath(os.path.realpath('Queue') + f'/song{q_num}.%(ext)s')

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

    for _ in range(3):
        next_song_name = next_song()
        # Playing next: {song_name} by {artist}
        # await ctx.send(f'Playing next: {next_song_name[1]} by {next_song_name[0]}')

    while True:
        # TODO: Limit / Cap the queue to 30 songs here
        for _ in range(2):
            next_song_name = next_song()
            # Playing next: {song_name} by {artist}
            # await ctx.send(f'Playing next: {next_song_name[1]} by {next_song_name[0]}')
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

# TODO: Current Song
@client.command(pass_context=True, aliases=['c, cur', 'curr'])
async def current(ctx):
    await ctx.send('Currently playing: song_name by artist_name')

# TODO: Clear Queue
@client.command(pass_context=True, aliases=['cl, clea',])
async def clear(ctx):
    queues.clear()
    await ctx.send('Queue cleared!')


# TODO: Print out the songs in the queue
@client.command(pass_context=True, aliases=['q, que'])
async def queue(ctx, search : str):
    await ctx.send('Songs in the queue:')
    # TODO: Print queued songs here

# TODO: Rename Command
@client.command(pass_context=True, aliases=['play_n, play_nex'])
async def play_next(ctx, search : str):
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

    queue_path = os.path.abspath(os.path.realpath('Queue') + f'/song{q_num}.%(ext)s')

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

client.run(os.environ["DISCORD_TOKEN"])