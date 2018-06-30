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
from scipy.io import loadmat


def loadData(directory, if_save = False):
    matList = glob(directory+'/*.mat')
    split = int(len(matFiles)*0.75)
    trainX = []
    trainY = []
    testX = []
    testY = []
    for file in matFiles[:split]:
        struct = loadmat(file)
        img = struct['sField']['imagesOutput'][0][0]
        mask = struct['sField']['locationParticles'][0][0]
        img = img.reshape(img.shape+ (1,)).astype('float32')
        mask = mask.reshape(img.shape+ (1,)).astype('float32')
        trainX.append(np.copy(img))
        trainY.append(np.copy(mask))
    trainX = np.asanyarray(trainX)
    trainY = np.asanyarray(trainY)


    for file in matFiles[split:]:
        struct = loadmat(file)
        img = struct['sField']['imagesOutput'][0][0]
        mask = struct['sField']['locationParticles'][0][0]
        img = img.reshape(img.shape+ (1,)).astype('float32')
        mask = mask.reshape(img.shape+ (1,)).astype('float32')
        testX.append(np.copy(img))
        testY.append(np.copy(mask))
    testY = np.asanyarray(testY)
    testX = np.asanyarray(testX)
    if if_save == True:
        np.save('trainSynthImages.npy',trainX)
        np.save('trainSynthMasks.npy',trainY)
        np.save('testSynthImages.npy',testX)
        np.save('testSynthMasks.npy',testY)
