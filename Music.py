import os
import youtube_dl

class Music:
	def __init__(self):
		'''Class that manages the downloading of youtube songs/videos.'''
		self.info_dict = {}
		self.video_title = ""
		self.video_duration = 0
		self.web_page_url = ""
		self.ydl_opts = {
			'format': 'bestaudio/best',
			'quiet': True,
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
			'default_search': 'ytsearch',
			'ignore-errors': True,
			'no_overwrites': True,
			'no_warnings': True,
			'quiet': True
    }
	
	def download_song(self, url, video_mode = False):
		'''Function that downloads a song by search team or URL.'''

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