from Tkinter import *
import numpy as np
import operation_file as fil
import draw_chart as dc

def check_silence(sound_file, frame_time, const_sound):
  # truyen vao: ten file, do dai frame, nguong am thanh
  if (const_sound > 0):
    x = 0
    cur = []
    s = 0
    e = 0
    status = 0
    time_start = 0
    time_end = 0

    return_value = fil.read_file(sound_file)
    data = return_value[0]
    samplerate = return_value[1]
    npoint = frame_time * samplerate
    nframe = len(data)/npoint

    for i in range(0,int(nframe),1):
      for j in range(0,int(npoint),1):
        t = data[j+i*int(npoint)]
        x = x + t*t
      if np.sqrt(x) > const_sound:
        cur = []
        if status == 0:
          status = 1
          print("start", i)
          s = i*npoint/samplerate*1000
      else:
        cur = []
        if status == 1:
          status = 0
          print("end", i)
          e = i*npoint/samplerate*1000
          if ((e-s) >= 100):
            dc.draw_start_silence(s)
            dc.draw_end_silence(e)
            time_start = s
            time_end = e
      x = 0

    return (time_start, time_end)
    # tra ve vi tri bat dau va ket thuc cua khoang co am thanh
  else:
    r = Tk()
    r.title("Notice")
    r.geometry("150x50")
    rlbl = Label(r, text="\n[!] Energy threshold = 0")
    rlbl.pack()
    r.mainloop()
