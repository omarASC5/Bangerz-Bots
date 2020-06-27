import os
import youtube_dl

class Music:
	def __init__(self):
		'''Class that manages the downloading of youtube songs/videos.'''
		self.ydl_opts = {
			'quiet': True,
			'default_search': 'ytsearch',
			'outtmpl': './songs/%(title)s.%(ext)s',
			'ignore-errors': True,
			'no_overwrites': True,
			'no_warnings': True
    }
	
	def download_song(self, url, playlist_name, video_mode = False):
		'''Function that downloads a song by search team or URL.'''

		# The song will download in a directory named after the playlist name
		self.ydl_opts['outtmpl'] = f'./{playlist_name}/%(title)s.%(ext)s'

		# If in audio mode => alter the ydl_opts for audio instead of video
		if not video_mode:
			self.ydl_opts['format'] = 'bestaudio/best'
			self.ydl_opts['postprocessors'] = [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}]

		# Try to download the song from search term / url
		with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			try:
				ydl.download([url])
			except:
				pass