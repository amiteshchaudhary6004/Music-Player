# module 200
from tkinter import *
import time, os
import tkinter.messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from pygame import mixer
from mutagen.mp3 import MP3
mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x700')
        self.root.title('Music Player')
        self.root.configure(background='white')
        self.paused = False
        self.playlist = []
        self.current_index = 0

        def play_music():
            if self.paused:
                mixer.music.unpause()
                self.label1['text'] = 'Music Unpaused...'
                self.paused = False
            else:
                try:
                    mixer.music.load(self.playlist[self.current_index])
                    mixer.music.play()
                    self.label1['text'] = 'Music Playing...'
                    self.lengthbar()
                    self.music_name_label['text'] = os.path.basename(self.playlist[self.current_index])
                except:
                    pass

        # Label
        self.label1 = Label(self.root, text="Let's Play a Music...", bg='black', fg='Yellow', font='20')
        self.label1.pack(side=BOTTOM, fill=X)

        # Music name display label at the top
        self.music_name_label = Label(self.root, text='', bg='white', fg='black', font=('Helvetica', 15))
        self.music_name_label.pack(side=TOP, pady=20)

        # Pause music function
        def pause_music():
            self.paused = True
            mixer.music.pause()
            self.label1['text'] = 'Music Paused...'

        # Stop music function
        def stop_music():
            mixer.music.stop()
            self.label1['text'] = 'Music Stopped...'
            self.paused = False

        # Volume mute function
        def mute():
            self.scale.set(0)

        # Volume up function
        def up():
            self.scale.set(80)

        # Volume control function
        def volumeup(val):
            volume = int(val) / 100
            mixer.music.set_volume(volume)
            self.label1['text'] = f'Volume: {int(val)}%'

        # Select folder function
        def select_folder():
            folder_selected = filedialog.askdirectory()
            if folder_selected:
                os.chdir(folder_selected)
                songs = os.listdir(folder_selected)
                songlist.delete(0, END)
                self.playlist = []
                for song in songs:
                    if song.endswith(".mp3"):
                        songlist.insert(END, song)
                        self.playlist.append(os.path.join(folder_selected, song))

        # Play selected song from the Listbox
        def play_song():
            selected_song = songlist.curselection()
            if selected_song:
                self.current_index = selected_song[0]
                play_music()

        songlist = Listbox(root, bg='white', fg='black')
        songlist.pack(fill=BOTH, expand=True)
        songlist.bind('<Double-1>', lambda x: play_song())

        # About function
        def about():
            tkinter.messagebox.showinfo('About us','Created By Amitesh')

        # Next music function
        def next_music():
            self.current_index += 1
            if self.current_index >= len(self.playlist):
                self.current_index = 0
            play_music()

        def previous_music():
            self.current_index -= 1
            if self.current_index < 0:
                self.current_index = len(self.playlist) - 1
            play_music()

        # Menu bar
        self.menubar = Menu(self.root)
        self.root.configure(menu=self.menubar)

        # Add Organise menu with Select Folder command
        organise_menu = Menu(self.menubar, tearoff=False)
        organise_menu.add_command(label='Select Folder', command=select_folder)
        self.menubar.add_cascade(label='File', menu=organise_menu)

        self.submenu3 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help', menu=self.submenu3)
        self.submenu3.add_command(label='About', command=about)

        self.submenu4 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Exit', command=self.root.destroy)

        # Load and resize images
        self.left_image = Image.open('image/left.png').resize((70, 70), Image.LANCZOS)
        self.right_image = Image.open('image/right.png').resize((60, 60), Image.LANCZOS)
        self.play_image = Image.open('image/play.png').resize((60, 60), Image.LANCZOS)
        self.pause_image = Image.open('image/pause.png').resize((60, 60), Image.LANCZOS)
        self.stop_image = Image.open('image/stop.png').resize((60, 60), Image.LANCZOS)
        self.volumeup_image = Image.open('image/volumeup.png').resize((40, 40), Image.LANCZOS)
        self.volumedown_image = Image.open('image/volumedown.png').resize((40, 40), Image.LANCZOS)

        self.photo_B1 = ImageTk.PhotoImage(self.left_image)
        self.photo_B2 = ImageTk.PhotoImage(self.right_image)
        self.photo_B3 = ImageTk.PhotoImage(self.play_image)
        self.photo_B4 = ImageTk.PhotoImage(self.pause_image)
        self.photo_B5 = ImageTk.PhotoImage(self.stop_image)
        self.photo_B6 = ImageTk.PhotoImage(self.volumedown_image)
        self.photo_B7 = ImageTk.PhotoImage(self.volumeup_image)

        # Adding left button (for "Next" function)
        self.left_button = Button(self.root, image=self.photo_B1, bd=0, bg='white', command=previous_music)
        self.left_button.place(x=180, y=595)

        # Adding right button
        self.right_button = Button(self.root, image=self.photo_B2, bd=0, bg='white', command=next_music)
        self.right_button.place(x=260, y=600)

        # Adding play button
        self.play_button = Button(self.root, image=self.photo_B3, bd=0, bg='white', command=play_music)
        self.play_button.place(x=360, y=600)

        # Adding pause button
        self.pause_button = Button(self.root, image=self.photo_B4, bd=0, bg='white', command=pause_music)
        self.pause_button.place(x=460, y=600)

        # Adding stop button
        self.stop_button = Button(self.root, image=self.photo_B5, bd=0, bg='white', command=stop_music)
        self.stop_button.place(x=560, y=600)

        # Adding volume down button
        self.volumedown_button = Button(self.root, image=self.photo_B6, bd=0, command=mute, bg='white')
        self.volumedown_button.place(x=800, y=610)

        # Volume scale
        self.scale = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, command=volumeup, bg='black', fg='white')
        self.scale.set(50)
        self.scale.place(x=840, y=610)

        # Adding volume up button
        self.volumeup_button = Button(self.root, image=self.photo_B7, bd=0, command=up, bg='white')
        self.volumeup_button.place(x=950, y=610)

root = Tk()
obj = MusicPlayer(root)
root.mainloop()