from PIL import Image
import glob

def giffer(path):
    frames = []
    for file in sorted(glob.glob(f"{path}/*.png")):
        frames.append(Image.open(file))
  
    frame_one = frames[0]
    frame_one.save("timelapse.gif", format="GIF", append_images=frames, 
                    save_all=True, duration=150, loop=0)
                    
                    
                    
if __name__ == "__main__":
    giffer("./pngs")
