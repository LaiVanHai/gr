import numpy as np

def basic_frequency(data, srate):
  #du lieu, tan so
  # dem so buoc nhay can thuc hien de xac dinh diem cuc dai
  break_point = int(srate/80) # nguong tan so tu 80 -> 400
  i = 0 + int(srate/450)
  n = i + break_point
  t_max = 0 # luu vi tri cua cuc dai

  t_max = np.argmax(data[i:n])
  t_max = t_max + i

  return (srate/t_max)
