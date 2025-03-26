# -*- coding: utf-8 -*-

import cv2
from pathlib import Path
import numpy as np
import pandas as pd


def convertToRGB(
        imageConverted,
        normalize = 256
    ):
    
    bits = getImgBits(imageConverted)
    if bits == 16:
        imageConverted = (imageConverted/normalize).astype('uint8') # Move from 16bits to 8bits for debugging
    if len(imageConverted.shape) < 3:
        imageConverted = cv2.cvtColor(imageConverted, cv2.COLOR_GRAY2RGB) # Move from RGB so this allow color for debugging

    return imageConverted

def getImgBits(
        image
    ):
    
    if image.dtype == "uint16":
        bits = 16
    else:
        bits = 8
        
    return bits

def convertTo8Bits(
        image,
        normalize = 256
    ):
    
    bits = getImgBits(image)
    if bits != 8:
         image = (image/normalize).astype('uint8')
         
    return image

def create_folder(
        folder_path
    ):

    folder = Path(folder_path)
    folder.mkdir(parents=True, exist_ok=True)  # Creates the folder if it doesn't exist

