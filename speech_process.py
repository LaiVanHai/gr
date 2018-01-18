from pylab import*
import numpy as np
import matplotlib.pyplot as plt
import operation_file as fil
import check_silence as cs
import basic_frequency as bf

def stacking(data1, data2):
  # xep chong data 1 vao data 2
  size1 = len(data1)
  size2 = len(data2)
  break_point = int(size2/3)

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


def speech_process(sound_file, frame_time, const_sound):
  # truyen vao: ten file, do dai frame, nguong am thanh

  return_value_open_file = fil.read_file(sound_file)
  data = return_value_open_file[0]
  srate = return_value_open_file[1]
  npoint = frame_time * srate

  return_value_check_silence= cs.check_silence(sound_file, frame_time, const_sound)
  time_start = return_value_check_silence[0]
  time_end = return_value_check_silence[1]

  arr_start = (int)(time_start*srate/1000) # mau bat dau khoang am thanh
  arr_end = (int)(time_end*srate/1000) # mau ket thuc khoang am thanh

  jump_length = int(srate/80)
  from_max_length = int(srate/450)

  t = 0 # dem so lan quet
  max = 0 # luu gia tri cuc dai
  t_max = 0 # luu vi tri cuc dai
  max_local = []
  r_sound = [] # tinh tan so co ban
  k = 0
  start = 0
  end = start+jump_length
  data_output = [] # luu du lieu sau khi xu ly

  while (end < arr_end):
    t_max = np.argmax(data[(start + from_max_length):end])
    start = t_max + start + from_max_length
    max_local.append(start)
    end = start + jump_length

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

  fil.write_file("output.wav", data_output, srate)

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
    return_value = bf.basic_frequency(r_sound, srate)
    basic_frequency_result.append(return_value)
    r_sound = []

  plt.figure(1)
  plt.title('Signal Wave...')
  plt.clf()
  plt.plot(basic_frequency_result, 'bo')
  ylabel('R(k)')
  xlabel('k')
  plt.ylim((0,150))

  plt.show()

  return basic_frequency_result
  # tra ve mang nhung vi tri cua tan so F0
