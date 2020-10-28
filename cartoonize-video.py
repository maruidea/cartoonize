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

def cartoonize():
    try:
        wb_cartoonizer.process_video('static/uploaded_videos/input.mp4')
    
    except Exception as e:
        print(traceback.print_exc())

if __name__ == "__main__":
    cartoonize()