import subprocess
import os.path
import wave
import pandas as pd
import numpy as np
import re
import struct


def get_streams(in_name):
    result = subprocess.run(["ffmpeg", "-i", in_name],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    err = result.stderr.decode('utf-8').split('\n')

    streams = []

    for line in err:
        match = re.match(
            r"^\s*Stream #([0-9]+):([0-9]+).*: (\w+): (\w+)", line)
        if match:
            (stream, part, kind, form) = match.group(1, 2, 3, 4)
            streams.append({'index': int(stream), 'part': int(part),
                            'kind': kind, 'format': form})

    return streams


def extract_audio(in_name, out_name):
    subprocess.run(["ffmpeg", "-i", in_name, "-vn", "-ac", "1",
                    out_name])


def read_wave(in_name):
    with wave.open(in_name, 'rb') as wave_read:
        nframes = wave_read.getnframes()
        frames = wave_read.readframes(nframes)
        sampwidth = wave_read.getsampwidth()
        dat = np.ndarray((int(len(frames) / sampwidth),), '<h', frames)
        return dat


def read_audio_dataframe(in_name):
    out_name = "output.wav"
    if(not os.path.exists(out_name)):
        extract_audio(in_name, out_name)
    d = read_wave(out_name)
    df = pd.DataFrame(data=d)
    return df
