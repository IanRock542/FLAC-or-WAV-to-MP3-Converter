import os, threading, pydub
from pydub.utils import which
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilenames
from tinytag import TinyTag
from cgitb import text
from json.tool import main

pydub.AudioSegment.converter = which("ffmpeg")

root = tk.Tk()
root.title("Audio File Converter")
root.geometry('500x150')

c =ttk.Frame(root, padding=(5,5, 12, 0))
c.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
lbl = ttk.Label(c, text='File to be converted')


def select_files(filetype: str) -> str:
    """
    Controls which file types are shown and able to be selected depending on which file selection button is pressed.
    """
    return askopenfilenames(
        title=f"Open {filetype} files",
        filetypes=((f"{filetype} files", f"*.{filetype.lower()}"),)
    )

def convert_wav(wav_files: str) -> None:
    """
    Converts Mp3 files to WAV files
    """
    
    try:
        for wav_file in wav_files:
            lbl = tk.Label(c, text=wav_file)
            lbl.grid(column=1, row=0)
            mp3_file = os.path.splitext(wav_file)[0] + '.mp3'
            tag = TinyTag.get(wav_file)
            sound = pydub.AudioSegment.from_wav(str(wav_file)).export(mp3_file, 
            format="mp3", bitrate="320k", 
            tags={'album': tag.album,'artist': tag.artist, 'title': tag.title,
             'date': tag.year, 'track': tag.track}
            )
            
        pb.stop()
    except pydub.exceptions.CouldntDecodeError:
        messagebox.showinfo(message="Could not decode the select file(s).")
    else:
        if wav_files:
            finished(wav_files)
    

def convert_flac(flac_files: str) -> None:
    """
    Converts Mp3 files to FLAC files
    """
    
    try:
        for flac_file in flac_files:
            lbl = tk.Label(c, text=flac_file)
            lbl.grid(column=1, row=0)
            mp3_file = os.path.splitext(flac_file)[0] + '.mp3'
            tag = TinyTag.get(flac_file)
            sound = pydub.AudioSegment.from_file(str(flac_file)).export(mp3_file, 
            format="mp3", bitrate="320k", 
            tags={'album': tag.album,'artist': tag.artist, 'title': tag.title,
            'date': tag.year, 'track': tag.track}
            )   
            
        pb.stop()

    except pydub.exceptions.CouldntDecodeError: 
        messagebox.showinfo(message="Could not decode the select file(s).")
    else:
        if flac_files:
            finished(flac_files)
    

def finished(files: str) -> None:
    """
    Displays a message box when the conversion completes.
    """
    messagebox.showinfo(message=f"Converted {files}.")

def start_flac_thread() -> None:
    """
    Creates thread to allow progressbar to run concurrently with convert_flac().
    """
    flac_files = select_files('FLAC')
    pb.start()
    t = threading.Thread(target=convert_flac, args=(flac_files,))
    t.start()

def start_wav_thread() -> None:
    """
    Creates thread to allow progressbar to run concurrently with convert_wav().
    """
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

pb = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='determinate')

#Grid widgets
convert_wav_btn.grid(column=0, row=0, sticky = tk.W, padx = 20)
convert_flac_btn.grid(column=0, row=1, sticky = tk.W, padx = 20)
c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)
lbl.grid(column=1, row=0)
pb.grid(column=0, row=2, pady=5)

if __name__ == "__main__":
    root.mainloop()