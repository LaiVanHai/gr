import wave
from scipy.io import wavfile
from Tkinter import *
from pylab import*
import numpy as np
from scipy.io.wavfile import write
from pygame import mixer

def read_file(sound_file):
  if sound_file != "":

    spf = wave.open(sound_file,'r')
    samplerate, sound = wavfile.read(sound_file)
    sound = sound / (2.**15)

    sample_point = spf.getnframes() # so mau
    # point_in_frame = frame_time * samplerate
    # number_frame = len(sound)/point_in_frame

    # print(sample_point/samplerate) # thoi gian cua file
    # signal = spf.readframes(-1)
    # signal = np.fromstring(signal, 'Int16')

    timeArray = arange(0, sample_point, 1)
    timeArray = timeArray / float(samplerate)
    timeArray = timeArray * 1000  #scale to milliseconds

    return (sound, samplerate, timeArray, sample_point)

  else:
    r = Tk()
    r.title("Error")
    r.geometry("150x50")
    rlbl = Label(r, text="\n[!] Open file error!!")
    rlbl.pack()
    r.mainloop()

def write_file(file_name, data, srate):
  scaled = np.int16(data/np.max(np.abs(data)) * 32767)
  if write(file_name, srate, scaled):
    r = Tk()
    r.title("Successfully")
    r.geometry("150x50")
    rlbl = Label(r, text="\n[!] Write file successfully!!")
    rlbl.pack()
    r.mainloop()

def playWav():
  if sound_file != "":
    spf = wave.open(sound_file,'r')
    mixer.init(spf.getframerate())
    try:
      d1 = mixer.Sound(sound_file)
    except:
      prompt = "Error: Sound file not found"
    d1.play()
  else:
    r = Tk()
    r.title("Notice")
    r.geometry("150x50")
    rlbl = Label(r, text="\n[!] Plese select file")
    rlbl.pack()
    r.mainloop()
