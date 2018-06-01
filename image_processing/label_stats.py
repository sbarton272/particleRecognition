from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import os
from ast import literal_eval
import shutil

def txt_reader(file):
    txt_info = open(file,'r')
    txt = []
    centers = []
    radii = []
    labels = []
    for line in txt_info:
        if line == '\n':
            pass
        else:
            line = line.strip('\n')
            txt.append(line)
    center_stop = txt.index('Radius Size:')
    radius_stop = txt.index('Defect Label:')
    label_stop = txt.index('Image Size:')
    for loc in txt[1:center_stop]:
        centers.append(literal_eval(loc))
    for loc in txt[center_stop+1:radius_stop] :
        radii.append(int(loc))
    for loc in txt[radius_stop+1:label_stop] :
        labels.append(loc)
    image_size = literal_eval(txt[-1])
    return centers, radii, labels, image_size
