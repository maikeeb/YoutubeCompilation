from moviepy.editor import *
from moviepy.video.tools.drawing import circle

clip = VideoFileClip(
    "C:\\Users\\leagu\\PycharmProjects\\Selenium\\offlinetv montage maker\\currentVideos\\718lilypichu0.mp4")

text = TextClip("some text", fontsize=12, color='white').set_pos("center").set_duration(30)

clippppppppppppppppppppppp = CompositeVideoClip([clip, text])

clippppppppppppppppppppppp.write_videofile('test.mp4', fps=30)
