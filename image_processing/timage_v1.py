import skimage as sk
from skimage import io
from skimage import exposure
import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob
from ncempy.io import convert2png as c2p

def imm(image):
    fig, ax = plt.subplots(figsize=(10,10))
    ax.imshow(image, cmap = 'gray')
    ax.axis('off')

def clean_xray(img):
    image = sk.img_as_float(img.copy())
    if type(image) is not np.ndarray:
        raise TypeError('Input must be numpy ndarray.')
    else:
        p1 = np.percentile(image, 0.0001)
        p80, p99 = np.percentile(image, (80, 99.99))
        print("mean:",image.mean(),'p80: ',p80,'p99: ',p99)
        image[image > p99] = p80
        image[image<p1] = p1
    return sk.img_as_ubyte(image)

# def auto_adjust_TEM(image):
#     image = exposure.equalize_adapthist(exposure.adjust_sigmoid(clean_xray(image)))
#     return image

def adjust_pipeline(directory_list):
    for directory in directory_list:
        try:
            os.mkdir(directory+'/adjustedPNG')
            new_directory = directory+'/adjustedPNG'
        except:
            new_directory = directory+'/adjustedPNG'
        dm3s = glob(directory+ '/*.dm3')
        for dm3 in dm3s:
            c2p.main(dm3)
        images = io.ImageCollection(directory+"/*.png")
        file_list = images.files
        name_list = [name.split('/')[-1].split('.')[0] for name in file_list]
        for idx, img in enumerate(images):
            image = clean_xray(img)
            plt.imsave(new_directory+'/'+name_list[idx]+'.png',image, cmap='gray')
        print('done!')
