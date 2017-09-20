import subprocess
import os.path
import pandas as pd
import ffmpeg
import srt


def subtitle_streams(in_name):
    streams = ffmpeg.get_streams(in_name)
    streams = list(filter(lambda x: x['kind'] == 'Subtitle', streams))
    return streams


def extract_subtitle(in_name, out_basename):
    streams = subtitle_streams(in_name)
    if not streams:
        return

    first = streams[0]
    ext = "srt"

    out_fullname = f"{out_basename}.{ext}"

    subprocess.run(["ffmpeg", "-y", "-vn", "-an", "-i", in_name,
                    "-map", f"{first['index']}:{first['part']}'", out_fullname],
                   stderr=subprocess.PIPE)


def parse_subtitle(in_name):
    with open(in_name, 'r') as f:
        return list(srt.parse(f.read()))


def get_subtitle_ranges(srt):
    result = []
    for s in srt:
        start = int(s.start.total_seconds() * 48000)
        end = int(s.end.total_seconds() * 48000)
        result.append({'start': start, 'end': end, 'text': s.content})
    return result


def read_subtitle_ranges(in_name):
    out_basename = "subtitle"
    extract_subtitle(in_name, out_basename)
    data = parse_subtitle(in_name)
    ranges = get_subtitle_ranges(data)
    return ranges
