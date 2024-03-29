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
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()

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

def check_queue(ctx, voice):
    Queue_infile = os.path.isdir('./Queue')
    if Queue_infile is True:
        DIR = os.path.abspath(os.path.realpath('Queue'))
        length = len(os.listdir(DIR))
        still_q = length - 1

        try:
            first_file = os.listdir(DIR)[0]
            next_song_to_play = spotify_processor.song_queue.pop(0)
            spotify_processor.current_song = \
            f'Playing {next_song_to_play[1]} by {next_song_to_play[0]}'
            # await ctx.send(spotify_processor.current_song)
            
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

            voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue(ctx, voice))
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

async def bot_remove_old_song_file():
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

def bot_rename_file_song_mp3():
    for file in os.listdir("./"):
        if file.endswith('.mp3'):
            name = file
            print("Renamed File: {}".format(name), end='\n\n')
            os.rename(file, 'song.mp3')

async def bot_queue_song_by_url(ctx, voice, url):
    # Prepare the download
    await ctx.send("Getting song ready now")
    # voice = get(client.voice_clients, guild=ctx.guild)

    # Download the song
    music = Music()
    music.download_song(url)

    # Rename the recently downloaded song file to song.mp3
    bot_rename_file_song_mp3()

    # Play the song.mp3 file in the voice channel
    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue(ctx, voice))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.5

    # Display the song being played
    with youtube_dl.YoutubeDL(music.ydl_opts) as ydl:
        # Store a dictionary with additional info on current song in Music object
        info_dict = ydl.extract_info(url, download=False)
        music.info_dict = info_dict

        # Store the song title
        video_title = info_dict['entries'][0]['title']
        music.video_title = video_title

        # Store the song title spotify_processor too
        spotify_processor.current_song = video_title

        # Save the length of the song in music object
        video_duration = info_dict['entries'][0]['duration']
        music.video_duration = video_duration

        # Save the URL to the song in the music object
        web_page_url = info_dict['entries'][0]['webpage_url']
        music.web_page_url = web_page_url

        # Display info about the song to the user
        await ctx.send(video_title)
        await ctx.send(web_page_url)
        print('playing\n', video_title)
    return music

# TODO: Only allow song commands in the song channel
@client.command(pass_context=True)
async def yt(ctx, url : str):
    # The bot joins the voice channel, if not already present
    voice = await bot_join_voice(ctx)
    if not voice:
        return
        
    # Remove the old song file
    await bot_remove_old_song_file()

    # Remove the old queue folder
    bot_remove_old_queue_folder()

    # Downloads the song based off the search term
    await bot_queue_song_by_url(ctx, voice, url)

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

def bot_find_random_song_in_playlist(spotify_processor):
    random_song = spotify_processor.random_song()
    spotify_processor.song_queue.append(random_song)
    return random_song
    
@client.command()
async def sp_playlist(ctx, index : int):
    # The bot joins the voice channel, if not already present
    voice = await bot_join_voice(ctx)
    if not voice:
        return

    # Remove the old song file
    await bot_remove_old_song_file()

    # Remove the old queue folder
    bot_remove_old_queue_folder()

    # Select the playlist that user wants by index
    spotify_processor.select_playlist(index)
    await ctx.send(f'Found playlist: {spotify_processor.selected_playlist}.')

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
        random_song = random.choice(spotify_processor.selected_songs)
        spotify_processor.song_queue.append(random_song)
        print('playing', random_song)
        url = random_song[1] + " " + random_song[0]
        q2(url)
        return random_song

    ###########

    # Find a random song in the spotify playlist
    random_song = bot_find_random_song_in_playlist(spotify_processor)
    await ctx.send(f'Playing: {random_song[1]} by {random_song[0]}')

    # The url is the search term entered to youtube through youtube_dl
        # To download the song
    url = random_song[1] + " " + random_song[0]
    # Everything afterwards is the same logic as the $yt command

    music = await bot_queue_song_by_url(ctx, voice, url)

    ###########

    Queue_infile = os.path.isdir('./Queue')
    if Queue_infile is False:
        os.mkdir('Queue')

    DIR = os.path.abspath(os.path.realpath('Queue'))
    q_num = len(os.listdir(DIR))
    while q_num != 4:
        next_song_name = next_song()
        q_num = len(os.listdir(DIR))

    ##########

    while True:
        next_song_name = next_song()
            # Playing next: {song_name} by {artist}
            # await ctx.send(f'Playing next: {next_song_name[1]} by {next_song_name[0]}')
        await asyncio.sleep(250)


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
    # TODO: Only allow the skip command to work if there is a Queue folder with at least one song
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

@client.command(pass_context=True, aliases=['c, cur', 'curr'])
async def current(ctx):
    await ctx.send(spotify_processor.current_song)

def bot_clear_queue():
    queues.clear()
    bot_remove_old_queue_folder()
    # CLear all exisiting variables and recreate with new username
    spotify_processor.__init__(
        os.environ["SPOTIFY_CLIENT_ID"],
        os.environ["SPOTIFY_CLIENT_SECRET"],
        str(open("username.txt", "r").readline())
    )

@client.command(pass_context=True, aliases=['cl, clea',])
async def clear(ctx):
    bot_clear_queue()
    await ctx.send('Queue cleared!')

@client.command(pass_context=True, aliases=['q, que'])
async def queue(ctx):
    str_to_print = '';
    for val, song in enumerate(spotify_processor.song_queue):
        str_to_print += f'{val + 1}. {song[1]} by {song[0]}\n'
    if str_to_print == '':
        await ctx.send('No songs in the queue')
    else:
        await ctx.send('Songs in the queue:')
        await ctx.send(f'''```{str_to_print}```''')

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