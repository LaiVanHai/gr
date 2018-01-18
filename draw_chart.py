from pylab import*
import matplotlib.pyplot as plt
from Tkinter import *
import operation_file as fil
import check_silence as cs
import basic_frequency as bf

def draw_start_silence(n):
  # ve duong ke bat dau cua khoang co am thanh
  plt.axvline(n, color='y')
  plt.show

def draw_end_silence(n):
  # ve duong ke ket thuc cua khoang co am thanh
  plt.axvline(n, color='r')
  plt.show


def draw_chart(sound_file):
  # nhan vao duong dan file, do dai ve thoi gian cua frame

  if sound_file != "":

    return_value = fil.read_file(sound_file)
    timeArray = return_value[2]
    sound = return_value[0]

    plt.figure(1)
    plt.title('Signal Wave...')
    plt.clf()
    plt.plot(timeArray, sound)
    ylabel('Amplitude')
    # xlabel('Sample point')
    xlabel('Time(ms)')

    plt.show()

  else:
    r = Tk()
    r.title("Notice")
    r.geometry("150x50")
    rlbl = Label(r, text="\n[!] Draw chart error!!")
    rlbl.pack()
    r.mainloop()


def draw_chart_basic_frequency(sound_file, frame_time, const_sound):
  # truyen vao: ten file, do dai frame, nguong am thanh

  return_value_open_file = fil.read_file(sound_file)
  data = return_value_open_file[0]
  srate = return_value_open_file[1]
  npoint = frame_time * srate

  return_value_check_silence= cs.check_silence(sound_file, frame_time, const_sound)
  time_start = return_value_check_silence[0]
  time_end = return_value_check_silence[1]

  i = 0
  x = 0
  s = 0
  e = 0
  basic_frequency_result = []
  r_sound = []

  start_point = int(srate * time_start/1000)
  end_point = int(srate * time_end/1000)

  # dem so frame trong file can xu ly
  nframe = int((time_end - time_start)/(frame_time*1000))

  print("srate:", srate)

  for i in range(0, int(nframe), 1):
    for k in range(0, int(npoint*0.8), 1):
      x = 0
      n0 = int(npoint) - 1 - k
      for n in range(1, n0, 1):
        t = n + i*int(npoint)
        x = x + data[start_point+t]*data[start_point+t+k]
      r_sound.append(x)
    return_value = bf.basic_frequency(r_sound, srate)
    basic_frequency_result.append(return_value)
    r_sound = []

  print("frame num:", nframe)
  plt.figure(1)
  plt.title('Signal Wave...')
  plt.clf()
  plt.plot(basic_frequency_result, 'ro')
  ylabel('R(k)')
  xlabel('k')
  plt.ylim((0,150))
  # fig.canvas.draw()
  plt.show()

  return basic_frequency_result
  # Tra ve mang luu cac vi tri cua tan so F0
