from clips import getclips
import datetime
from oneVideo import compile as comp
import threading
import time
import os
import shutil
from datetime import date

while True:
    start_time = time.time()
    currentdate = datetime.datetime.today().weekday()

    linkFile = open("mainFile" ,'r')
    print(linkFile)
    folder = '..\\currentVideos'
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
    for link in linkFile:

        # get clips
        clipsThread = threading.Thread(target=getclips(link))
        clipsThread.start()
        clipsThread.join()
        # combine clips
    while True:
        try:
            oneVideoThread = threading.Thread(target=comp('offlinetv' + str(date.today())))
            oneVideoThread.start()
            oneVideoThread.join()
            break
        except OSError:
            pass
    print("--- %s seconds ---" % (time.time() - start_time))
    time.sleep(10)
    while True:
        if currentdate != datetime.datetime.today().weekday():
            break
        time.sleep(10)
