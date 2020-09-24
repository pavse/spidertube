#!/usr/bin/python3 -u
import time
from pytube import YouTube
from pathlib import Path
import pickle

text_file = open("links.txt", "r")
lines = text_file.readlines()
text_file.close()


def download_stream(stream):
    print("  Stream: ", end="")
    print(stream)
    file_path = Path(stream.default_filename)
    if file_path.is_file():
        print("File already exists: \"{}\"".format(stream.default_filename))
    else:
        try:
            stream.download()
            return True
        except BaseException as streamException:
            print(streamException)
            print("Download failed")
    return False


class VideoURL:
    def __init__(self, orig_url):
        self.orig_url = orig_url.strip()
        self.v_id = ""
        self.status = "new"
        self.description = "unknown"


def pickled_items(filename):
    """ Unpickle a file of pickled data. """
    result = []
    try:
        with open(filename, "rb") as f:
            try:
                result = pickle.load(f)
            except EOFError as __E:
                print(__E)
    except IOError as __IO:
        print(__IO)
    return result


print('URLs in database file:')
db = pickled_items('database.pkl')
for v in db:
    print("Pickled URL: {} {}".format(v.status, v.orig_url))

for line in lines:
    print("URL: " + line.strip())
    v = VideoURL(line)
    try:
        yt = YouTube(line)
        v.description = yt.title
        if yt.length < 1800:
            v.status = "tried"
            for video_stream in yt.streams.filter(progressive=True).order_by('resolution').desc():
                print(
                    "Downloading \"{0}\" {1}:{2:02d} {3} @ {4} fps".format(
                        yt.title, int(yt.length / 60), yt.length % 60, video_stream.resolution, video_stream.fps)
                )
                if download_stream(video_stream):
                    v.status = "done"
                    break
        else:
            v.status = "skip"
            print("Skipping {0}:{1:02d} video \"{2}\"".format(int(yt.length / 60), yt.length % 60, yt.title))
    except BaseException as ytException:
        print(ytException)
        print("Cannot open the URL")
        v.status = "fail"
        time.sleep(20)
    finally:
        print("----------")
        time.sleep(2)
    db.append(v)

with open('database.pkl', 'wb') as output:
    pickle.dump(db, output, 1)

# EXAMPLE
# yt.author  'Красный Угол'
# yt.length  579  (seconds)
# yt.streams
# yt.title   '04. Суд будет Страшным настолько, что святые ангелы будут трепетать от Страха...'


def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))
