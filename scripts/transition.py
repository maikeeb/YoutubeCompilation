from moviepy.editor import *


def oneTransition(clipName, tranName):
    TextClip(clipName, color='white', size=(1920, 1080), bg_color='black', fontsize=50).set_duration(3).fadeout(
        0.5).fadein(0.5).write_videofile(
        'C:\\Users\\leagu\\PycharmProjects\\Selenium\\clip montage maker\\currentVideos\\' + str(tranName) + '.mp4',
        fps=60)


if __name__ == '__main__':
    oneTransition('hello', '1')
