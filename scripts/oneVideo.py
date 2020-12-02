from moviepy.editor import *
import os
from natsort import natsorted


def compile(name):
    L = []

    for root, dirs, files in os.walk("../currentVideos"):

        # files.sort()
        files = natsorted(files)
        for file in files:
            if os.path.splitext(file)[1] == '.mp4':
                filePath = os.path.join(root, file)
                video = VideoFileClip(filePath)
                L.append(video)

    final_clip = concatenate_videoclips(L)
    final_clip.to_videofile(
        "C:\\Users\\leagu\\PycharmProjects\\Selenium\\clip montage maker\\fullVideos\\%s.mp4" % name,
        fps=60, remove_temp=True)


if __name__ == '__main__':
    compile("test")