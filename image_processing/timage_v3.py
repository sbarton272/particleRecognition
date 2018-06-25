import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob
from ncempy.io import dm
from matplotlib.image import imsave
from matplotlib import cm
from skimage import transform
from skimage import exposure

def xray_correct(image):
    if type(image) is not np.ndarray:
        raise TypeError('Input must be numpy ndarray.')
    image[image<0] = 0
    bad_loc = np.argwhere(image > ((image.mean()+1000)-image.std()))
    for loc in bad_loc:
        if loc[0]+1 > (image.shape[0]-1) or loc[0]-1 < 0 or loc[1]+1 > (image.shape[1]-1) or loc[1] - 1 < 0:
            new_pixel_int = image.mean()+(image.std()*5)
        else:
            neighbor_sum = image[loc[0]-1,loc[1]] + image[loc[0]+1,loc[1]] + image[loc[0],loc[1]-1] + image[loc[0],loc[1]+1]
            new_pixel_int = neighbor_sum /4
        image[loc[0],loc[1]] = new_pixel_int
    return image

def adjust_pipeline(directory_list):
    i = 0
    for directory in directory_list:
        try:
            os.mkdir(directory+'/adjustedPNG2')
            new_directory = directory+'/adjustedPNG2'
        except:
            new_directory = directory+'/adjustedPNG2'
        dm3s = glob(directory+ '/*.dm3')
        for dm3 in dm3s:
            img = dm.dmReader(dm3)['data']
            if img.shape[0] < 1024:
                pass
            elif img.shape[0] == 2048 and img.shape[1] == 2048:
                img = transform.resize(xray_correct(img),(1024,1024), anti_aliasing = True )
                name = dm3.split('/')[-1].split('.')[0]
                imsave(new_directory+'/'+name+'.png', img, format="png", cmap=cm.gray)
            elif img.shape[0] == 1024 and img.shape[1] == 1024:
                name = dm3.split('/')[-1].split('.')[0]
                imsave(new_directory+'/'+name+'.png', exposure.equalize_adapthist(xray_correct(img)), format="png", cmap=cm.gray)
        i += 1
        print('{} / {} directories complete'.format(i,len(directory_list)))
    print('done!')

def imm(image):
    fig, ax = plt.subplots(figsize=(10,10))
    ax.imshow(image, cmap = 'gray')
    ax.axis('off')
