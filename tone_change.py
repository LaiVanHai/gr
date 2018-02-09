from Tkinter import *

def error_show():
  r = Tk()
  r.title("Error")
  r.geometry("150x50")
  rlbl = Label(r, text="\n[!] Tone_type_error")
  rlbl.pack()
  r.mainloop()

def init_tone(stacking_count, tone_type):
  if tone_type == "ThanhHuyen":
    return (stacking_count, stacking_count)
  elif tone_type == "ThanhSac":
    return (0, stacking_count)
  if tone_type == "ThanhNang":
    return (2*stacking_count, 2*stacking_count)
  else:
    error_show()


def tone_change(count_stack, tone_type):
  if tone_type == "ThanhHuyen":
    count_stack -= 1
    return count_stack
  elif tone_type == "ThanhSac":
    count_stack += 1
    return count_stack
  else:
    error_show()
