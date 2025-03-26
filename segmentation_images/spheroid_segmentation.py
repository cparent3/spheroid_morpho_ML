# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pandas as pd
import time
import modules.functions as functions
import modules.segmentation as segmentation
from pathlib import Path


folder  = Path("data_segmentation/cell_line")

folder_out = Path("output")
functions.create_folder(folder_out)

# Get all the images files in the folder 
file_paths = [str(file) for file in folder.glob("*") if file.is_file()]

# Init variables
gaussianFilterSD = 1
threshMin = 500 
threshMax = 700  

dilationKernel = (5,5)

minGrayLevel = 40
maxGrayLevel = 25000
minArea = 400
maxArea = 20000
minCircularity = 0.1
minAspectRatio = 0.3


t0 = time.time()

 
# Initialize dataframe that will contain spheroids morphological properties
sphero_props_concat = pd.DataFrame()

for f, file_path in enumerate(file_paths):
    # Load image
    image = cv2.imread(file_path, -1)

    # Get the mask of the image
    mask, _, _ = segmentation.getMask(image, gaussianFilterSD, dilationKernel, threshMin, threshMax)
    
    # Identify the objects that are spheroids, save their properties in a dataframe sphero_props and get the image of the spheroids
    sphero_contours, sphero_props, _, _, sphero_masks = segmentation.getObjects(image, mask, minGrayLevel, maxGrayLevel, minArea, maxArea, minCircularity, minAspectRatio)
    sphero_contours_img = segmentation.debug_getObjects(image, sphero_contours, sphero_props)
    
    # Insert a column "Name" in sphero_props to identity the image/object to the properties
    name_file = Path(file_path).stem
    name = [name_file] if sphero_props.empty else [name_file] * len(sphero_props)
    sphero_props.insert(0, "Name", name)
    
    # Concatenate the spheroids properties of all the images in the same dataframe
    sphero_props_concat = pd.concat([sphero_props_concat, sphero_props], ignore_index=True)

    # Combine masks if different object detected on the image
    if len(sphero_masks) != 0:
        sphero_mask_comb = np.maximum.reduce(sphero_masks)
    else:
        sphero_mask_comb = np.zeros(image.shape)

    # Save images of interest for debuging
    cv2.imwrite(f"{folder_out}\\{name_file}.tiff", image*16)
    cv2.imwrite(f"{folder_out}\\{name_file}_segmented.tiff", sphero_contours_img)
    cv2.imwrite(f"{folder_out}\\{name_file}_mask.tiff", sphero_mask_comb)

    
# Save the spheroids morphological properties in a .csv file
sphero_props_concat.to_csv(f"{folder_out}\\morphological_features.csv", sep=';', decimal=',', index=False)

print("Pocessing time: %s sec " %round(time.time()-t0))