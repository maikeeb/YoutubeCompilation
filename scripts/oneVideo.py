from datetime import date

from moviepy.editor import *
from natsort import natsorted


def compile(name):
    L = []
    currentVideoLength = 0
    time_stamps_file = open("time stamps", 'w')
    streamer_links_file = open("streamer links", 'w')
    streamers = []
    for root, dirs, files in os.walk("../currentVideos"):
        files = natsorted(files)
        files.reverse()
        for file in files:
            print(file)

            if os.path.splitext(file)[1] == '.mp4':
                filePath = os.path.join(root, file)
                print(filePath)
                video = VideoFileClip(filePath, target_resolution=(1080, 1920))
                L.append(video.set_start(currentVideoLength - files.index(file)).fx(transfx.slide_in, 1, 'bottom'))
                print(file)
                # time stamp handler
                currentVideoLength = int(currentVideoLength)
                time_stamps_file.write(
                    str(currentVideoLength // 60) + ":" +
                    (str(currentVideoLength % 60) if len(str(currentVideoLength % 60)) == 2 else "0" + str(
                        currentVideoLength % 60))
                    + " - " + ''.join(i for i in file.strip('.mp4') if not i.isdigit()) + '\n')
                currentVideoLength += video.duration - 2
                # streamer link handler
                if (''.join(i for i in file.strip('.mp4') if not i.isdigit())) not in streamers:
                    streamer_links_file.write(
                        ''.join(i for i in file.strip('.mp4') if
                                not i.isdigit()) + ": " + "https://www.twitch.tv/" + ''.join(
                            ''.join(i for i in file.strip('.mp4') if not i.isdigit())) + '\n')
                    streamers.append(''.join(i for i in file.strip('.mp4') if not i.isdigit()))
                if currentVideoLength >= 481:  # and len(L) % 2 == 0: # 480 seconds is the length for mid roll ads
                    break
    time_stamps_file.close()
    streamer_links_file.close()
    final_clip = [CompositeVideoClip(L)]
    print(currentVideoLength)
    concatenate_videoclips(final_clip, padding=-1).write_videofile(
        "../fullVideos/%s.mp4" % name,
        fps=60, remove_temp=True, threads=12)


if __name__ == '__main__':
    """testing = ImageClip("test.png").set_duration(3)
    testing.write_videofile("testing.mp4",
                            fps=60, remove_temp=True, threads=8)"""

    compile('video1' + str(date.today()))
