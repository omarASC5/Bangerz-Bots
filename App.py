from tkinter import *
import config
from SpotifyProcessor import SpotifyProcessor
from Music import Music

class App:
	def __init__(self):
			'''Class that renders the GUI window application.'''
			self.username = ''
	
			# Initializes the window & title of tab
			self.app = Tk()
			self.app.title('Download Spotify Playlists')
			self.app.geometry('')
			# self.app.call('encoding', 'system', 'utf-8')

			# Text Box, Label Prompting username & Submit Button
			username_text = StringVar()
			username_label = Label(self.app, text='Spotify Username', font=('bold', 14), pady=15)
			username_label.pack()
			
			username_entry = Entry(self.app, textvariable=username_text, borderwidth = 4)
			username_entry.pack()

			username_button = Button(self.app, text="Submit", command = lambda: self.second_window(username_entry.get()))
			username_button.pack()

			warning_message = Label(self.app, text='NOTE: Spotify playlists MUST be made public', font=('bold', 16), pady=15)
			warning_message.pack()

			self.app.mainloop()

	def quit(self):
		'''Exit the current window application.'''
		self.app.destroy()

	def set_username(self, new_username):
		'''Change the username member variable.'''
		self.username = str(new_username)

	def second_window(self, new_username):
		'''After submitting the username, the window closes and a new one opens.
		Rendering publicly avaiable spotify playlists that can be downloaded.'''
		
		# Exits the current window
		self.set_username(new_username)
		self.quit()

		# Makes a new window
		self.app = Tk()
		self.app.title('Download Spotify Playlists')
		self.app.geometry('')
		
		# Initializes new spotify processor object: will do all processing
			# relating to finding playlists, songs, and downloading
		spotify_processor = SpotifyProcessor(
			config.SPOTIFY_CLIENT_ID,
			config.SPOTIFY_CLIENT_SECRET,
			str(self.username)
		)

		# Loads the list of playlist names
		spotify_processor.fill_playlists_names()
		playlists_names = spotify_processor.playlists_names

		# Title of window
		Label(self.app, 
         text="""Choose a playlist
to download:""",
         justify = LEFT,
         padx = 20).pack()

		# Checkboxes that toggle video_mode and/or random_mode
		CheckVar1 = IntVar()
		CheckVar2 = IntVar()
		C1 = Checkbutton(self.app, text = "Random Mode", variable = CheckVar1, \
										onvalue = 1, \
										width = 20)
		C2 = Checkbutton(self.app, text = "Video Mode", variable = CheckVar2, \
										onvalue = 1,
										width = 20)

		C1.pack()
		C2.pack()

		# Loop that renders all playlists under the user's account as bullet points
		v = IntVar()
		
		for val, playlists_name in enumerate(playlists_names):
			Radiobutton(self.app,
			text=playlists_name.encode('ascii', 'ignore'), # ignores unicode characters
			padx = 20,
			variable=v,
			value=val).pack(anchor=W)

		# Download Playlist Button
		playlist_button = Button(self.app, text="Download Playlist",command=lambda:
			spotify_processor.download_playlist(
				v.get() + 1, Music(), random_mode = bool(CheckVar1.get()), video_mode = bool(CheckVar2.get())
			)
		)
		playlist_button.pack()