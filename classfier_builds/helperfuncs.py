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
    """used to break up the 1024x1024 images into 512x512 segments takes a
     diretory and string specifying whether it is slicing 'image' or  'label'"""
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

def image_slice_small(directory):
    """used to break up the 1024x1024 images into 64x64 segments takes a
     diretory that is the source"""
    image_file_list = glob(directory+'/images/*.png')
    image_new_directory = directory + '/small_sliced_images/'
    if os.path.isdir(image_new_directory) != True:
        os.mkdir(image_new_directory)
    label_file_list = glob(directory+'/labels/*.png')
    label_new_directory = directory + '/small_sliced_labels/'
    if os.path.isdir(label_new_directory) != True:
        os.mkdir(label_new_directory)
    image_name_list = [name.split('/')[-1].split('.')[0] for name in image_file_list]
    label_name_list = [name.split('/')[-1].split('.')[0] for name in label_file_list]
    if len(image_name_list) != len(label_name_list):
        raise RuntimeError('different number of images and labels')
    if image_name_list != label_name_list:
        raise RuntimeError('images and labels did not match')
    for idx, file in enumerate(image_file_list):
        image2split = io.imread(file, as_grey=True)
        label2split = io.imread(label_file_list[idx], as_grey=True)
        for x in range(0,15*64,64):
            for y in range(0,15*64,64):
                image = image2split[x:x+64,y:y+64]
                label = label2split[x:x+64,y:y+64]
                if np.any(np.isin([1],label)) == False:
                    pass
                else:
                    image_name = image_name_list[idx]+ '_' + str(x)+ str(y) + '.png'
                    label_name = image_name_list[idx]+ '_' + str(x)+ str(y) + '.png'
                    plt.imsave(image_new_directory+image_name,image, cmap='gray')
                    plt.imsave(label_new_directory+label_name,label, cmap='gray')
    print('done!')
