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


def getclips(name):
    browser = webdriver.Firefox()

    # goes to there channel then goes to there clips
    browser.get('https://www.twitch.tv/%s/clips?filter=clips&range=7d' % name)
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
    for link in video_links:
        browser.get(link)  # goes to the link

        # makes the browser wait until the video duration has appeared
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                         'a.tw-align-middle')))
        currentVideo = browser.find_element_by_css_selector(  # gets the url of the raw video
            '.video-player__container > video:nth-child(1)').get_attribute(
            "src")
        videoTitle = browser.find_element_by_css_selector(  # gets the video title
            '.tw-card-body > div:nth-child(1) > p:nth-child(1) > span:nth-child(1)').get_attribute("title")
        oneTransition(videoTitle, str(video_links.index(link) * 2))  # takes the video title and makes a shit transition
        while True:
            try:
                urllib.request.urlretrieve(currentVideo,  # gets video url and downloads it
                                           "C:\\Users\\leagu\\PycharmProjects\\Selenium\\clip montage maker\\currentVideos\\" + str(
                                               (video_links.index(link) * 2) + 1) + '.mp4')
                break
            except ValueError:
                print("Failed to grab url")
                currentVideo = browser.find_element_by_css_selector(  # gets the url of the raw video
                    '.video-player__container > video:nth-child(1)').get_attribute(
                    "src")
    """ # returns the time in a list of [hours, minutes] from where the clip is in the vod
     placeInVod = \
         browser.find_element_by_css_selector('a.tw-align-middle').get_attribute('href').split("t=")[2].split('m')[
             0].split('h')"""

    browser.close()


if __name__ == '__main__':
    getclips("doublelift")
