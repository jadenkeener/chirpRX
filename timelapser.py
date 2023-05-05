""" timelapser.py
Last Edited 5/4/23
By Jaden Keener and the NMT Dev Team

This block converts static png images into a timelapse in both .gif
and .mov format

Requires you to pass in png folder path.
"""

# Imports
from PIL import Image
import glob
import ffmpy
import argparse

""" Parse args
Only arg is PNG folder path
"""
parser = argparse.ArgumentParser()
parser.add_argument("-P", "--path", help = "PNG Folder Path", type=str)
args = parser.parse_args()


""" giffer function
This function grabs the image frames, sorts them, and makes a gif
using PIL
"""
def giffer(path):
    frames = []
    for file in sorted(glob.glob(f"{path}/*.png")):
        frames.append(Image.open(file))
  
    frame_one = frames[0]
    frame_one.save("timelapseGIF.gif", format="GIF", append_images=frames, 
                    save_all=True, duration=150, loop=0)
                    
                    
                    
if __name__ == "__main__":
    """ ensure that a path was passed """
    if args.path == None:
        raise ValueError("Error: You must pass a path argument (-P)")
    giffer(args.path)
    
    """ transform gif into mov with ffmpeg """
    ff = ffmpy.FFmpeg(inputs={'timelapseGIF.gif': None}, outputs={'timelapseMOV.mov': None})
    ff.run()
    
    print("Done!")
