#!/usr/bin/python3 -u
import time
from pytube import YouTube

text_file = open("links.txt", "r")
lines = text_file.readlines()
text_file.close()


def download_stream(stream):
    print("  Stream: ", end="")
    print(stream)
    downloaded = False
    try:
        stream.download()
        downloaded = True
    except BaseException as streamException:
        print(streamException)
        print("Download failed")
    return downloaded


for line in lines:
    print("URL: " + line.strip())
    try:
        yt = YouTube(line)
        if yt.length < 1800:
            for video_stream in yt.streams.filter(progressive=True).order_by('resolution').desc():
                print(
                    "Downloading \"{0}\" {0}:{1:02d} {1} @ {2} fps".format(
                        yt.title, int(yt.length / 60), yt.length % 60, video_stream.resolution, video_stream.fps)
                )
                if download_stream(video_stream):
                    break
            # for audio_stream in yt.streams.filter(file_extension='mp4', type='audio').order_by('bitrate').desc():
            #     print("Downloading \"{0}\" {1}".format(yt.title, audio_stream.abr))
            #     if download_stream(audio_stream):
            #         break
        else:
            print("Skipping {0}:{1:02d} video \"{2}\"".format(int(yt.length / 60), yt.length % 60, yt.title))
    except BaseException as ytException:
        print(ytException)
        print("Cannot open the URL")
        time.sleep(20)
    finally:
        print("----------")
        time.sleep(2)


# EXAMPLE
# yt.author  'Красный Угол'
# yt.length  579  (seconds)
# yt.streams
# yt.title   '04. Суд будет Страшным настолько, что святые ангелы будут трепетать от Страха...'


def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))
