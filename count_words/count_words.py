# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 23:09:19 2022

@author: Simon Tam
"""

import numpy as np 
from scipy.io import wavfile

# Get Max Amplitude
def amplitude_envelope(signal,frame_length,hop_length):
    max_amplitude_frame=[]
    for i in range(0,len(signal),hop_length):
        max_amplitude_frame.append(max(signal[i:i+frame_length]))
    return np.array(max_amplitude_frame)

# Moving Average
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

# downsize ratio
downsize_ratio = 50
# valid sylllables amplitude threshold
slb_amp_th = 100
# min of peak of one sylllable's sound wave duration, in sec
slb_time_th = 0.05

# Read .wav file
samplerate, data = wavfile.read('./ptk_2.wav')

# time threshold to count threshold
amp_count_th = round(slb_time_th * samplerate / downsize_ratio)

# Get Absolute Value of the Amplitude
data_abs = np.absolute(data)
# Downsampling on original data
data_downsized = amplitude_envelope(data_abs, int(np.floor(downsize_ratio)), int(np.floor(downsize_ratio)))

# Get max of neighbours
data_ma = moving_average(data_downsized, amp_count_th)

# Plot a figure
# import matplotlib.pyplot as plt
# plt_1 = plt.figure(figsize=(240, 36))
# plt.plot(np.arange(len(data_ma)),data_ma)
# # Show
# plt.show()

ans = 0
# label of last val, local max or local min
last_lbl = 'min'
# value of last local max or local min
last_val = -1

# Analyze the sound wave
for i, val in enumerate(data_ma):
    
    # skip if amplitude is too small
    if last_lbl == 'min' and val < slb_amp_th:
        continue
    
    # max and min of neighbours
    max_nei = max(data_ma[max(0,i-amp_count_th):min(len(data_ma),i+amp_count_th)])
    min_nei = min(data_ma[max(0,i-amp_count_th):min(len(data_ma),i+amp_count_th)])
    
    # check if it is a valid max
    if val == max_nei and last_lbl == 'min' and val >= slb_amp_th:
        # update label and val
        last_lbl = 'max'
        last_val = val
    # check if it is a valid min
    elif val == min_nei and last_lbl == 'max' and val < last_val/2:
        # count as one valid sylllable
        ans += 1
        # update label and val
        last_lbl = 'min'
        last_val = val
    
print(f'"Pa Ta Ka" has been said {round(ans/3)} times')
