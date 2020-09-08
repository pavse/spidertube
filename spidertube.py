#!/usr/bin/python3

from pytube import YouTube

text_file = open("links.txt", "r")
lines = text_file.readlines()
text_file.close()

for line in lines[0:4]:
    print(line)
    yt = YouTube(line)
    s = yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
    print(s)

# EXAMPLE
# yt.author  'Красный Угол'
# yt.length  579  (seconds)
# yt.streams
# yt.title   '04. Суд будет Страшным настолько, что святые ангелы будут трепетать от Страха...'


def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))

# url = pl.video_urls
# print(len(url))
# for x in url:
#    print(url[x])
