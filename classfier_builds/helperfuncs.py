from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage import io

def imm(image):
    """function to display a large grayscale image"""
    fig, ax = plt.subplots(figsize=(10,10))
    ax.imshow(image, cmap = 'gray')
    ax.axis('off')

def check_label(labels,images,idx,alpha = 0.25):
    """Takes in skimage ImageCollections for labels and original images and an index for an image
    to show the overlay of the created label mask and original image"""
    pic = alpha*np.reshape(labels[idx][:,:,0],(1024,1024)) + (1-alpha)*np.reshape(images[idx][:,:,0],(1024,1024))
    imm(pic)

def image_slice(directory, im_lbl):
    """used to break up the 1024x1024 images into 512x512 segments"""
    if im_lbl == 'image':
        file_list = glob(directory+'/images/*.png')
        new_directory = directory + '/sliced_images/'
    elif im_lbl == 'label':
        file_list = glob(directory+'/labels/*.png')
        new_directory = directory + '/sliced_labels/'
    name_list = [name.split('/')[-1].split('.')[0] for name in file_list]
    for idx, file in enumerate(file_list):
        image2split = plt.imread(file)
        image1 = image2split[:512,:512,:]
        plt.imsave(new_directory+name_list[idx]+'_a.png',image1, cmap='gray')
        image1 = image2split[512:,:512,:]
        plt.imsave(new_directory+name_list[idx]+'_b.png',image1, cmap='gray')
        image1 = image2split[:512,512:,:]
        plt.imsave(new_directory+name_list[idx]+'_c.png',image1, cmap='gray')
        image1 = image2split[512:,512:,:]
        plt.imsave(new_directory+name_list[idx]+'_d.png',image1, cmap='gray')
    print('done!')
