from pylab import*
from Tkinter import *
from tkFileDialog import askopenfilename
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import wave
from scipy.io import wavfile
from pygame import mixer
from scipy.io.wavfile import write

import matplotlib
matplotlib.use('TkAgg')

class Layout(Frame):
  def __init__(self, parent):
    Frame.__init__(self, parent)

    self.parent = parent
    self.initUI()

  def initUI(self):
    self.parent.title("Simple Menu")

    menuBar = Menu(self.parent)
    self.parent.config(menu=menuBar)

    fileMenu = Menu(menuBar)
    fileMenu.add_command(label="Exit", command=self.onExit)
    menuBar.add_cascade(label="File", menu=fileMenu)

  def onExit(self):
    self.quit()

root = Tk()
root.geometry("800x600+500+500")
root.title("Audio analysis")
app = Layout(root)

sound_file = ""
const_sound = 0
status = 0
sound = []
r_sound = [] # bien doi ham tu tuong quan
result = []
number_frame = 0
point_in_frame = 0
sample_point = 0
frame_time = 0.04
samplerate = 0
timeArray = []
N = 500
K = 150
max_local = [] # luu vi tri cua cac cuc dai dia phuong
time_start = 0
time_end = 0
local_time_length = 0
data_output = []
basic_frequency_result = []


# 150/640*0.04
varFile = StringVar()
varConst = StringVar()
varFile.set("Sound Processor")
varConst.set("")

Tops = Frame(root, width = 800, height = 50, bg="powder blue", relief=SUNKEN)
Tops.pack(side=TOP)
f1 = Frame(root, width = 200, height = 600, bg="powder blue", relief=SUNKEN)
f1.pack(side=LEFT)
f2 = Frame(root, width = 1000, height = 600, bg="powder blue", relief=SUNKEN)
f2.pack(side=RIGHT)

#===================Info=======================
lblInfo = Label(Tops, font=('arial', 14, 'bold'), textvariable = varFile, fg="Steel Blue", bd=10, anchor='w')
lblInfo.grid(row=0, column=0)
lblInfo2 = Label(Tops, font=('arial', 14, 'bold'), textvariable = varConst, fg="Steel Blue", bd=10, anchor='w')
lblInfo2.grid(row=1, column=0)

btnSelectFile = Button(f1, padx=8, pady=8, bd=2, fg="black", font=('arial', 10),
  text="Choose File", bg="white", command=lambda: openFile()).grid(row=1, column=0)
btnPlay = Button(f1,text="Play Original",command=lambda: playWav()).grid(row=1, column=1)

#=====================Function============================
def retrieveInput():
  global const_sound
  inputValue=textBox.get("1.0","end-1c")
  if checkNumber(inputValue) == 1:
    const_sound = float(inputValue)
    varConst.set("Const: " + inputValue)
    root.update_idletasks()

def retrieveInput2():
  global local_time_length
  inputValue=textBox2.get("1.0","end-1c")
  if checkNumber(inputValue) == 1:
    local_time_length = int(inputValue)

def openFile():
  Tk().withdraw()
  global sound_file
  sound_file = askopenfilename()
  print(sound_file)
  varFile.set("File path: " + sound_file)
  root.update_idletasks()

def checkNumber(n):
  try:
    x = float(n)
    return 1
  except ValueError:
    r = Tk()
    r.title("Notice")
    r.geometry("250x50")
    rlbl = Label(r, text="\n[!] Not valid number.")
    rlbl.pack()
    r.mainloop()

def exitProgram():
  sys.exit(0)

def basic_frequency(data, break_point, srate):
  #du lieu, buoc nhay, tan so
  global basic_frequency_results
  i = 0 + int(srate/450)
  n = i + break_point
  max = 0 # luu gia tri cuc dai
  t_max = 0 # luu vi tri cua cuc dai
  for k in range(i, n, 1):
    if (max < data[k]):
      t_max = k
      max = data[k]

  basic_frequency_result.append(srate/t_max)

def stacking(data1, data2):
  # xep chong data 1 vao data 2
  size1 = len(data1)
  size2 = len(data2)
  break_point = int(size2/5)

  point = size1 - break_point
  j = -1 # bien duyet mang data 2
  while(point < (size1 - 1)):
    j += 1
    point += 1
    data1[point] = data1[point] + data2[j]

  while(j < (size2 - 1)):
    j += 1
    data1.append(data2[j])

  return data1


def speech_process(data, npoint, srate):
  global max_local
  global time_start
  global time_end
  global local_time_length
  global data_output
  global frame_time
  global basic_frequency_result
  global r_sound

  arr_start = (int)(time_start*srate/1000) # mau bat dau khoang am thanh
  arr_end = (int)(time_end*srate/1000) # mau ket thuc khoang am thanh

  # print("bat dau am thanh:", arr_start)
  # print("ket thuc am thanh:", arr_end)
  # jump_length = (int)(local_time_length*srate/1000)
  jump_length = local_time_length

  t = 0 # dem so lan quet
  max = 0 # luu gia tri cuc dai
  t_max = 0 # luu vi tri cuc dai
  max_local = []
  r_sound = [] # tinh tan so co ban

  for i in range(arr_start, arr_end, 1):
    if t < jump_length:
      t = t + 1
      if (max < data[i]):
        t_max = i
        max = data[i]
    else:
      max_local.append(t_max)
      t = 0
      max = 0

  print("jump length:",jump_length)
  print("max_local_array:",len(max_local))

  for i in range(0, len(max_local)-1, 1):
    print(max_local[i])

  i = 0
  j = 1
  break_point = max_local[0] # khoang cach cua vi tri phan tu dau cua mang data va mang hamming
  data_output_sub = [] # mang luu gia tri cua moi frame khi nhan voi ham cua so
  while(max_local[j+2] <= arr_end):
    max0 = data[max_local[i]] # max cua frame dang xet
    max1 = 0 # max cuar hamming
    hamming_arr = []

    if (max0 < data[max_local[i+1]]):
      max0 = data[max_local[i+1]]
    if (max0 < data[max_local[i+2]]):
      max0 = data[max_local[i+2]]

    hamming_arr = np.hamming(max_local[i+2] - max_local[i] + 1)
    size = max_local[i+2] - max_local[i]
    for k in range(0, size, 1):
      if (max1 < hamming_arr[k]):
        max1 = hamming_arr[k]

    ratio = max1/max0  # ty le giua 2 gia tri cuc dai
    size = -1
    for k in range(max_local[i], max_local[i+2], 1):
      size += 1
      value = hamming_arr[size]/ratio*data[k]
      data_output_sub.append(value)

    if (data_output):
      data_output = stacking(data_output, data_output_sub)
    else:
      data_output = data_output_sub

    data_output_sub = []

    max0 = data[max_local[j]] # max cua frame dang xet
    max1 = 0 # max cuar hamming
    hamming_arr = []

    if (max0 < data[max_local[j+1]]):
      max0 = data[max_local[j+1]]
    if (max0 < data[max_local[j+2]]):
      max0 = data[max_local[j+2]]

    hamming_arr = np.hamming(max_local[j+2] - max_local[j] + 1)
    size = max_local[j+2] - max_local[j]
    for k in range(0, size, 1):
      if (max1 < hamming_arr[k]):
        max1 = hamming_arr[k]

    ratio = max1/max0  # ty le giua 2 gia tri cuc dai
    size = -1
    for k in range(max_local[j], max_local[j+2], 1):
      size += 1
      value = hamming_arr[size]/ratio*data[k]
      data_output_sub.append(value)

    data_output = stacking(data_output, data_output_sub)
    data_output_sub = []

    i += 1
    j += 1

    if ((j+2)>=len(max_local)):
      break

  print("data_output_length", len(data_output))
  # arr = np.array(data_output)
  # wavfile.write("output.wav", srate, arr)

  scaled = np.int16(data_output/np.max(np.abs(data_output)) * 32767)
  write("output.wav", srate, scaled)

  basic_frequency_before = basic_frequency_result
  # luu lai gia tri cua ham tu tuong quan luc dau
  basic_frequency_result = []
  npoint = frame_time * srate
  nframe = len(data_output)/npoint

  break_point = int(srate/80) # nguong tan so tu 80 -> 400

  print("srate:", srate)

  for i in range(0, int(nframe), 1):
    for k in range(0, int(npoint*0.8), 1):
      x = 0
      n0 = int(npoint) - 1 - k
      for n in range(1, n0, 1):
        t = n + i*int(npoint)
        x = x + data_output[t]*data_output[t+k]
      r_sound.append(x)
    basic_frequency(r_sound,break_point,srate)
    r_sound = []

  plt.figure(1)
  plt.title('Signal Wave...')
  plt.clf()
  plt.plot(basic_frequency_before, 'ro')
  plt.plot(basic_frequency_result, 'bo')
  ylabel('R(k)')
  xlabel('k')
  plt.ylim((0,150))

  # fig.canvas.draw()
  plt.show()

def checkSilence(data, nframe, npoint):
  global status
  global result
  global time_start
  global time_end
  x = 0
  cur = []
  s = 0
  e = 0

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
          start_silence(s)
          end_silence(e)
          time_start = s
          time_end = e
    x = 0
  # print(len(data))
  # print(len(result))

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


#==========================Butto===================n======
textBox=Text(f1, height=2, width=15)
textBox.grid(row=2, column=0)
buttonCommit=Button(f1, height=1, width=5, text="Commit",
  command=lambda: retrieveInput())
buttonCommit.grid(row=2, column=1)
# btnExit = Button(f1,text="Quit",bd=10,bg="pink", command=lambda: exitProgram()).grid(row=8, column=0)
#==========Nhap do dai dia phuong============
textBox2=Text(f1, height=2, width=15)
textBox2.grid(row=3, column=0)
buttonCommit2=Button(f1, height=1, width=5, text="Send",
  command=lambda: retrieveInput2())
buttonCommit2.grid(row=3, column=1)
#=======================ve do thi=======================
fig = plt.figure(1)
t = np.arange(0.0,3.0,0.01)

canvas = FigureCanvasTkAgg(fig, master=f2)
plot_widget = canvas.get_tk_widget()

def start_silence(n):
  plt.axvline(n, color='y')
  fig.canvas.draw()

def end_silence(n):
  plt.axvline(n, color='r')
  fig.canvas.draw()

def draw_chart2(data, srate, npoint):
  # mang du lieu, tan so, so mau trong mot frame
  global r_sound
  global timeArray
  global status
  global basic_frequency_result

  i = 0
  x = 0
  s = 0
  e = 0
  basic_frequency_result = []

  print('npoint: ', npoint)
  r_sound = []

  start_point = int(srate * time_start/1000)
  end_point = int(srate * time_end/1000)

  # dem so frame trong file can xu ly
  nframe = int((time_end - time_start)/(frame_time*1000))

  # dem so buoc nhay can thuc hien de xac dinh diem cuc dai
  break_point = int(srate/80) # nguong tan so tu 80 -> 400

  print("srate:", srate)

  for i in range(0, int(nframe), 1):
    for k in range(0, int(npoint*0.8), 1):
      x = 0
      n0 = int(npoint) - 1 - k
      for n in range(1, n0, 1):
        t = n + i*int(npoint)
        x = x + data[start_point+t]*data[start_point+t+k]
      r_sound.append(x)
    basic_frequency(r_sound, break_point, srate)
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
  r_sound = []

def draw_chart():
  global number_frame
  global sound
  global point_in_frame
  global samplerate
  global timeArray
  global sample_point

  if sound_file != "":
    spf = wave.open(sound_file,'r')
    samplerate, sound = wavfile.read(sound_file)
    sound = sound / (2.**15)

    sample_point = spf.getnframes() # so mau
    point_in_frame = frame_time * samplerate
    number_frame = len(sound)/point_in_frame

    # print(sample_point/samplerate) # thoi gian cua file
    # signal = spf.readframes(-1)
    # signal = np.fromstring(signal, 'Int16')

    timeArray = arange(0, sample_point, 1)
    timeArray = timeArray / float(samplerate)
    timeArray = timeArray * 1000  #scale to milliseconds

    plt.figure(1)
    plt.title('Signal Wave...')
    # plt.plot(signal)
    plt.clf()
    plt.plot(timeArray, sound)
    ylabel('Amplitude')
    # xlabel('Sample point')
    xlabel('Time(ms)')


    # fig.canvas.draw()
    plt.show()

    # du lieu, so mau

  else:
    r = Tk()
    r.title("Notice")
    r.geometry("150x50")
    rlbl = Label(r, text="\n[!] Plese select file")
    rlbl.pack()
    r.mainloop()


plot_widget.grid(row=0, column=0)
btnDraw = Button(f1,text="Draw",command=lambda: draw_chart()).grid(row=4, column=0)
btnDraw2 = Button(f1,text="Draw2",command=lambda: draw_chart2(sound, samplerate, point_in_frame)).grid(row=5, column=0)
btnCheck = Button(f1,text="Check",command=lambda: checkSilence(sound, number_frame, point_in_frame)).grid(row=4, column=1)
btnFindMaxLocal = Button(f1,text="Speech_process",command=lambda: speech_process(sound, sample_point, samplerate)).grid(row=5, column=1)
root.mainloop()
