from cgitb import text
import os, threading, pydub
from tinytag import TinyTag
from pydub.utils import which
from tkinter.filedialog import askopenfilenames
from tkinter import *
from tkinter import messagebox, ttk

pydub.AudioSegment.converter = which("ffmpeg")

root = Tk()
root.title("Audio File Converter")
root.geometry('500x150')

c = ttk.Frame(root, padding=(5,5, 12, 0))
c.grid(column=0, row=0, sticky=(N, W, E, S))
lbl = ttk.Label(c, text='File to be converted')


def select_files(filetype):
    if filetype == 'WAV':
        filetypes = (
            ('WAV files', '*.wav'),
            ('All files', '*.*'))
        filename = askopenfilenames(
            title='Open WAV files',
            filetypes=filetypes
            )
        return filename
    elif filetype =='FLAC':
        filetypes = (
            ('FLAC files', '*.flac'),
            ('All files', '*.*')
        )
        filename = askopenfilenames(
            title='Open FLAC files',
            filetypes=filetypes
        )
        return filename

def convert_wav(wav_files):
    try:
        for wav_file in wav_files:
            lbl = Label(c, text=wav_file)
            lbl.grid(column=1, row=0)
            mp3_file = os.path.splitext(wav_file)[0] + '.mp3'
            tag = TinyTag.get(wav_file)
            sound = pydub.AudioSegment.from_wav(wav_file).export(mp3_file, 
            format="mp3", bitrate="320k", 
            tags={'album': tag.album,'artist': tag.artist, 'title': tag.title,
             'date': tag.year, 'track': tag.track}
            )

        pb.stop()
    except pydub.exceptions.CouldntDecodeError:
        messagebox.showinfo(message="Could not decode the select file(s).")
    else:
        if wav_files:
            messagebox.showinfo(message=f"Converted {wav_files}.")
     
def convert_flac(flac_files):
    try:
        for flac_file in flac_files:
            lbl = Label(c, text=flac_file)
            lbl.grid(column=1, row=0)
            mp3_file = os.path.splitext(flac_file)[0] + '.mp3'
            tag = TinyTag.get(flac_file)
            sound = pydub.AudioSegment.from_file(flac_file).export(mp3_file, 
            format="mp3", bitrate="320k", 
            tags={'album': tag.album,'artist': tag.artist, 'title': tag.title,
            'date': tag.year, 'track': tag.track}
            )
           

        pb.stop()

    except pydub.exceptions.CouldntDecodeError: 
        messagebox.showinfo(message="Could not decode the select file(s).")
    else:
        if flac_files:
            messagebox.showinfo(message=f"Converted {flac_files}.")



def start_flac_thread():
    flac_files = select_files('FLAC')
    pb.start()
    t = threading.Thread(target=convert_flac, args=(flac_files,))
    t.start()


def start_wav_thread():
    wav_files = select_files('WAV')
    pb.start()
    t2 = threading.Thread(target=convert_wav, args=(wav_files,))
    t2.start()


#Create widgets
convert_wav_btn = ttk.Button(
    c, 
    text="Convert WAV",
    command=start_wav_thread,
    default="active"
)
convert_flac_btn = ttk.Button(
    c, 
    text="Convert FLAC", 
    command=start_flac_thread, 
    default="active"
)

pb = ttk.Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')

#Grid widgets
convert_wav_btn.grid(column=0, row=0, sticky = W, padx = 20)
convert_flac_btn.grid(column=0, row=1, sticky = W, padx = 20)
c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)
lbl.grid(column=1, row=0)
pb.grid(column=0, row=2, pady=5)

root.mainloop()