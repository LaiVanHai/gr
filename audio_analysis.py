from tkFileDialog import askopenfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import draw_chart as dc
import check_silence as cs
import operation_file as fil
import basic_frequency as bf
import speech_process as sp


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
frame_time = 0.04

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

def draw_normal():
  dc.draw_chart(sound_file)

def check_silence():
  cs.check_silence(sound_file, frame_time, const_sound)

def draw_chart_basic_frequency():
  dc.draw_chart_basic_frequency(sound_file, frame_time, const_sound)

def speech_process():
  sp.speech_process(sound_file, frame_time, const_sound)

#==========================Button===================n======
textBox=Text(f1, height=2, width=15)
textBox.grid(row=2, column=0)
buttonCommit=Button(f1, height=1, width=5, text="Commit",
  command=lambda: retrieveInput())
buttonCommit.grid(row=2, column=1)
btnExit = Button(f1,text="Quit",bd=10,bg="pink", command=lambda: exitProgram()).grid(row=8, column=0)
#=======================ve do thi=======================
fig = plt.figure(1)
t = np.arange(0.0,3.0,0.01)

canvas = FigureCanvasTkAgg(fig, master=f2)
plot_widget = canvas.get_tk_widget()


plot_widget.grid(row=0, column=0)
btnDraw = Button(f1,text="Draw",command=lambda: draw_normal()).grid(row=4, column=0)
btnDraw2 = Button(f1,text="Draw2",command=lambda: draw_chart_basic_frequency()).grid(row=5, column=0)
btnCheck = Button(f1,text="Check",command=lambda: check_silence()).grid(row=4, column=1)
btnFindMaxLocal = Button(f1,text="Speech_process",command=lambda: speech_process()).grid(row=5, column=1)
root.mainloop()
