import skimage as sk
from skimage import io
from skimage import exposure
import numpy as np
import matplotlib.pyplot as plt
import os

def imm(image):
    fig, ax = plt.subplots(figsize=(10,10))
    ax.imshow(image, cmap = 'gray')
    ax.axis('off')

def clean_xray(image):
    if type(image) is not np.ndarray:
        raise TypeError('Input must be numpy ndarray.')
    else:
        up_thres = image.mean() + 4*image.std()
        down_thres = image.mean() - 4*image.std()
        image[image>up_thres] = image.mean()
        image[image<down_thres] = image.mean()
    return image

def auto_adjust_TEM(image):
    image = exposure.equalize_adapthist(exposure.adjust_sigmoid(clean_xray(image)))
    return image

def adjust_pipeline(directory_list):
    for directory in directory_list:
        try:
            os.mkdir(directory+'/adjustedTif')
            new_directory = directory+'/adjustedTif'
        except:
            new_directory = directory+'/adjustedTif'
        images = io.ImageCollection(directory+"/*.tif")
        file_list = images.files
        name_list = [name.split('/')[-1].split('.')[0] for name in file_list]
        for idx, img in enumerate(images):
            img = auto_adjust_TEM(img)
            io.imsave(new_directory+'/'+name_list[idx]+'.png',img)
        print('done!')
