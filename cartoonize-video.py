import os
import io
import uuid
import sys
import yaml
import traceback

with open('./config.yaml', 'r') as fd:
    opts = yaml.safe_load(fd)

sys.path.insert(0, './white_box_cartoonizer/')

import cv2
from PIL import Image
import numpy as np

from cartoonize import WB_Cartoonize

if not opts['run_local']:
    from video_api import api_request
    # Algorithmia (GPU inference)
    import Algorithmia

## Init Cartoonizer and load its weights 
wb_cartoonizer = WB_Cartoonize(os.path.abspath("white_box_cartoonizer/saved_models/"), opts['gpu'])

def convert_bytes_to_image(img_bytes):
    """Convert bytes to numpy array

    Args:
        img_bytes (bytes): Image bytes read from flask.

    Returns:
        [numpy array]: Image numpy array
    """
    
    pil_image = Image.open(io.BytesIO(img_bytes))
    if pil_image.mode=="RGBA":
        image = Image.new("RGB", pil_image.size, (255,255,255))
        image.paste(pil_image, mask=pil_image.split()[3])
    else:
        image = pil_image.convert('RGB')
    
    image = np.array(image)
    
    return image

def cartoonize():
    try:
        filename = "input.mp4"
        original_video_path = os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], filename)
        
        # Slice, Resize and Convert Video to 15fps
        modified_video_path = os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], filename.split(".")[0] + "_modified.mp4")
        #change the size if you want higher resolution :
        ############################
        # Recommnded width_resize  #
        ############################
        #width_resize = 1920 for 1080p: 1920x1080.
        #width_resize = 1280 for 720p: 1280x720.
        #width_resize = 854 for 480p: 854x480.
        #width_resize = 640 for 360p: 640x360.
        #width_resize = 426 for 240p: 426x240.
        width_resize=480

        #change the variable value to change the time_limit of video (In Seconds)
        time_limit = 10
        os.system("ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -t {} -filter:v scale={}:-2 -r 15 -c:a copy '{}'".format(os.path.abspath(original_video_path), time_limit, width_resize, os.path.abspath(modified_video_path)))
        #Note: You can also remove the -t parameter to process the full video
        #use below code to process the full video
        #os.system("ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -filter:v scale={}:-2 -r 15 -c:a copy '{}'".format(os.path.abspath(original_video_path), width_resize, os.path.abspath(modified_video_path)))

        # if local then "output_uri" is a file path
        output_uri = wb_cartoonizer.process_video(modified_video_path)
    
    except Exception as e:
        print(traceback.print_exc())

if __name__ == "__main__":
    cartoonize()