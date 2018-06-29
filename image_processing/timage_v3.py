import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob
from ncempy.io import dm
from matplotlib.image import imsave
from matplotlib import cm
from skimage import transform
from skimage import exposure
from ast import literal_eval
import shutil
from skimage import io

#Image preprocessing scripts for CNN development

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

def txt_reader(file):
    txt_info = open(file,'r')
    txt = []
    centers = []
    radii = []
    for line in txt_info:
        if line == '\n':
            pass
        else:
            line = line.strip('\n')
            txt.append(line)
    center_stop = txt.index('Radius Size:')
    radius_stop = txt.index('Defect Label:')
    for loc in txt[1:center_stop]:
        centers.append(literal_eval(loc))
    for loc in txt[center_stop+1:radius_stop] :
        radii.append(int(loc))
    image_size = literal_eval(txt[-1])
    return centers, radii, image_size


def spot_maker(location, radius, label_mask):
    for x in np.arange(location[0]-radius,location[0]+radius,1):
        for y in np.arange(location[1]-radius,location[1]+radius,1):
            dx = x - location[0]
            dy = y - location[1]
            if np.sqrt((dx**2+dy**2)) <= radius \
            and int(x) < label_mask.shape[0] and int(y) < label_mask.shape[1]:
                label_mask[int(y),int(x)] = 1
    return label_mask

def mask_maker(file):
    centers, radii, image_size = txt_reader(file)
    label_mask = np.zeros(image_size)
    for idx,radius in enumerate(radii):
        label_mask = spot_maker(centers[idx],radius,label_mask)
    return label_mask

def mask_pipeline(directory):
    file_list = glob(directory+'/text_files/*.txt')
    name_list = [name.split('/')[-1].split('.')[0] for name in file_list]
    for idx, file in enumerate(file_list):
        if len(open(file,'r').readlines()) == 0:
            pass
        else:
            label_mask = mask_maker(file)
            plt.imsave(directory+'/labels/'+name_list[idx]+'.png',label_mask, cmap='gray')
        shutil.move(file,directory+'/old_text_files/')
    print('done!')
