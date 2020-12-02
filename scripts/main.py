from clips import getclips
import datetime
from oneVideo import compile as comp
import threading
import time
import os
import shutil
from datetime import date
while True:
    currentdate = datetime.datetime.today().weekday()

    files = {0: open('twitch links monday', 'r'),
             1: open('twitch links tuesday', 'r'),
             2: open('twitch links wednesday', 'r'),
             3: open('twitch links thursday', 'r'),
             4: open('twitch links friday', 'r'),
             5: open('twitch links saturday', 'r'),
             6: open('twitch links sunday', 'r')}

    linkFile = files[currentdate]
    print(linkFile)
    for link in linkFile:
        folder = 'C:\\Users\\leagu\\PycharmProjects\\Selenium\\clip montage maker\\currentVideos'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                print("Deleted %s" % file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        # get clips
        clipsThread = threading.Thread(target=getclips(link))
        clipsThread.start()
        clipsThread.join()
        # combine clips
        while True:
            try:
                oneVideoThread = threading.Thread(target=comp(link.strip('\n') + str(date.today())))
                oneVideoThread.start()
                oneVideoThread.join()
                break
            except OSError:
                pass
        time.sleep(10)

    while True:
        if currentdate != datetime.datetime.today().weekday():
            break
        time.sleep(10)
