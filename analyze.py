import subprocess
import os.path
import pandas as pd
import numpy as np
import ffmpeg
import subtitle
from scipy.signal import argrelextrema
import struct
import wave


def zero_crossing_rate(x):
    return np.sum(np.abs(np.ediff1d(x))) / len(x)


def average_min(x):
    mins_idxes = argrelextrema(x, np.less)
    mins = [x[i] for i in mins_idxes]
    return np.mean(mins)


def average_max(x):
    maxs_idxes = argrelextrema(x, np.greater)
    maxs = [x[i] for i in maxs_idxes]
    return np.mean(maxs)


def write_wav(dat, i):
    noise_output = wave.open(f"noise{i}.wav", 'w')
    noise_output.setparams((1, 2, 48000, 0, 'NONE', 'not compressed'))

    values = []

    for x in dat:
        packed_value = struct.pack('h', x)
        values.append(packed_value)

    value_str = b''.join(values)
    noise_output.writeframes(value_str)

    noise_output.close()


def analyze(in_name):
    df = ffmpeg.read_audio_dataframe(in_name)
    ranges = subtitle.read_subtitle_ranges("subtitle.srt")
    arr = []

    for r in ranges:
        view = df.loc[r['start']:r['end']]
        arr.append([view[0].mean(0), zero_crossing_rate(view[0]),
                    average_min(view.values), average_max(view.values), r['text']])
        # write_wav(view[0], r['start'])

    data = pd.DataFrame(arr, columns=['mean', 'zcr', 'min', 'max', 'text'])
    return data
