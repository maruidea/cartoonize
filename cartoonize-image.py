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

def convert_bytes_to_image(filename):
    """Convert bytes to numpy array

    Args:
        img_bytes (bytes): Image bytes read from flask.

    Returns:
        [numpy array]: Image numpy array
    """
    
    pil_image = Image.open(filename)
    if pil_image.mode=="RGBA":
        image = Image.new("RGB", pil_image.size, (255,255,255))
        image.paste(pil_image, mask=pil_image.split()[3])
    else:
        image = pil_image.convert('RGB')
    
    image = np.array(image)
    
    return image

def cartoonize():
    try:
        ## Read Image and convert to PIL (RGB) if RGBA convert appropriately
        image = convert_bytes_to_image('static/sample_images/input.jpg')

        img_name = str(uuid.uuid4())
        
        cartoon_image = wb_cartoonizer.infer(image)
        
        cartoonized_img_name = os.path.join('static/cartoonized_images', img_name + ".jpg")
        cv2.imwrite(cartoonized_img_name, cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR))
    except Exception as e:
        print(traceback.print_exc())

if __name__ == "__main__":
    cartoonize()