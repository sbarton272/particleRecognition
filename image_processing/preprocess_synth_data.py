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


def loadData(directory, if_save = False, selectImages = None):
    matFiles = glob(directory+'/*.mat')
    if selectImages == None:
        split = int(len(matFiles)*0.75)
    else:
        split = int(selectImages*0.75)
    print('split is:', split)
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
        trainX.append(np.copy(img[:512,:512]))
        trainX.append(np.copy(img[512:,:512]))
        trainX.append(np.copy(img[:512,512:]))
        trainX.append(np.copy(img[512:,512:]))
        trainY.append(np.copy(mask[:512,:512]))
        trainY.append(np.copy(mask[512:,:512]))
        trainY.append(np.copy(mask[:512,512:]))
        trainY.append(np.copy(mask[512:,512:]))
    trainX = np.asanyarray(trainX)
    trainY = np.asanyarray(trainY)

    if selectImages == None:
        for file in matFiles[split:]:
            struct = loadmat(file)
            img = struct['sField']['imagesOutput'][0][0]
            mask = struct['sField']['locationParticles'][0][0]
            img = img.reshape(img.shape+ (1,)).astype('float32')
            mask = mask.reshape(img.shape+ (1,)).astype('float32')
            testX.append(np.copy(img[:512,:512]))
            testX.append(np.copy(img[512:,:512]))
            testX.append(np.copy(img[:512,512:]))
            testX.append(np.copy(img[512:,512:]))
            testY.append(np.copy(mask[:512,:512]))
            testY.append(np.copy(mask[512:,:512]))
            testY.append(np.copy(mask[:512,512:]))
            testY.append(np.copy(mask[512:,512:]))
    else:
        for file in matFiles[split:selectImages]:
            struct = loadmat(file)
            img = struct['sField']['imagesOutput'][0][0]
            mask = struct['sField']['locationParticles'][0][0]
            img = img.reshape(img.shape+ (1,)).astype('float32')
            mask = mask.reshape(img.shape+ (1,)).astype('float32')
            testX.append(np.copy(img[:512,:512]))
            testX.append(np.copy(img[512:,:512]))
            testX.append(np.copy(img[:512,512:]))
            testX.append(np.copy(img[512:,512:]))
            testY.append(np.copy(mask[:512,:512]))
            testY.append(np.copy(mask[512:,:512]))
            testY.append(np.copy(mask[:512,512:]))
            testY.append(np.copy(mask[512:,512:]))
    testX = np.asanyarray(testX)
    testY = np.asanyarray(testY)
    if if_save == True:
        np.save('trainSynthImages.npy',trainX)
        np.save('trainSynthMasks.npy',trainY)
        np.save('testSynthImages.npy',testX)
        np.save('testSynthMasks.npy',testY)
    return trainX, trainY, testX, testY
