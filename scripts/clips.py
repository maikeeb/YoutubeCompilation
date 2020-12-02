from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import time
import urllib.request
import shutil
from transition import oneTransition
import threading
from multiprocessing import Process
from moviepy.editor import *

downloadList = []
currentVideoL = [0, ""]
transtionL = []


def overlay(viewCountF, name):
    final_clip = [
        CompositeVideoClip(
            [VideoFileClip("..\\currentVideos\\" + viewCountF + name.strip(
                '\n') + '0' + '.mp4'),
             TextClip(name.strip(
                 '\n'), color='white', bg_color='red', method='label',
                 fontsize=50).set_duration(3).fadeout(
                 0.5).fadein(0.5).set_position((45, 600))])]

    concatenate_videoclips(final_clip).write_videofile(
        "..\\currentVideos\\" + viewCountF + name.strip(
            '\n') + '0.5' + '.mp4', fps=60, remove_temp=True, threads=12)


def getclips(name):
    currentVideo = 0
    browser = webdriver.Firefox()

    # goes to there channel then goes to there clips
    browser.get('https://www.twitch.tv/%s/clips?filter=clips&range=24hr' % name)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                     'div:nth-child(1) > article:nth-child(1) >'
                                                                     ' div:nth-child(2) > div:nth-child(1) >'
                                                                     ' div:nth-child(5) > a:nth-child(1)')))

    # finds all the video link elements
    videos = browser.find_elements_by_css_selector(
        'div:nth-child(1) > article:nth-child(1) > div:nth-child(2)'
        ' > div:nth-child(1) > div:nth-child(5) > a:nth-child(1)')

    video_links = [elem.get_attribute('href') for elem in videos]  # this gets all the video links out of the elements
    print(video_links)
    for link in video_links[:10]:
        browser.get(link)  # goes to the link

        # makes the browser wait until the video mp4 appears
        WebDriverWait(browser, 560).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                          '.video-player__container > video:nth-child(1)')))
        time.sleep(1)
        while currentVideo in currentVideoL:
            currentVideo = browser.find_element_by_css_selector(  # gets the url of the raw video
                '.video-player__container > video:nth-child(1)').get_attribute(
                "src")

        print(currentVideo)
        currentVideoL.append(currentVideo)

        # WebDriverWait(browser, 560).until(EC.presence_of_element_located((By.CSS_SELECTOR,
        #  'h2.tw-ellipsis')))
        # videoTitle = browser.find_element_by_css_selector(  # gets the video title
        #   'h2.tw-ellipsis').get_attribute("title")

        WebDriverWait(browser, 560).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                          '.tw-stat__value')))
        viewCount = browser.find_element_by_css_selector(
            '.tw-stat__value').text

        # transtionL.append(threading.Thread(target=oneTransition, args=(videoTitle,
        # viewCount + name.strip('\n') + '1')))
        # transtionL[-1].start()  # takes the video title and makes a shit transition
        print(currentVideo)
        downloadList.append(threading.Thread(
            target=urllib.request.urlretrieve, args=(currentVideo,  # gets video url and downloads it
                                                     "..\\currentVideos\\" + viewCount + name.strip(
                                                         '\n') + '0' + '.mp4')))
        print("..\\currentVideos\\" + viewCount + name.strip('\n') + '0' + '.mp4')
        if video_links.index(link) == 0:
            viewCountF = viewCount

        while True:
            try:
                downloadList[-1].start()
                break
            except ValueError:
                print("Failed to grab url")
                currentVideo = browser.find_element_by_css_selector(  # gets the url of the raw video
                    '.video-player__container > video:nth-child(1)').get_attribute(
                    "src")
            except Exception as e:
                print(e)
    browser.close()
    for video in downloadList:
        try:
            video.join()
        except Exception as e:
            print(e)

    # os.rename("..\\currentVideos\\" + viewCountF + name.strip(
    #    '\n') + '0' + '.mp4', 'bruh.mp4')
    threaddddd = Process(target=overlay, args=(viewCountF, name))
    threaddddd.start()
    threaddddd.join()
    os.remove("..\\currentVideos\\" + viewCountF + name.strip(
        '\n') + '0' + '.mp4')

    """ # returns the time in a list of [hours, minutes] from where the clip is in the vod
     placeInVod = \
         browser.find_element_by_css_selector('a.tw-align-middle').get_attribute('href').split("t=")[2].split('m')[
             0].split('h')"""


if __name__ == '__main__':
    start_time = time.time()
    getclips("zubatlel")
    print("--- %s seconds ---" % (time.time() - start_time))
