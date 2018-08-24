import numpy as np
from keras.models import Model
from keras.layers import *
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras import backend as K
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.losses import binary_crossentropy
from keras import metrics

trainX = np.load('/global/scratch/cgroschner/trainSynthImages.npy')
trainY = np.load('/global/scratch/cgroschner/trainSynthMasks.npy')
testX = np.load('/global/scratch/cgroschner/testSynthImages.npy')
testY = np.load('/global/scratch/cgroschner/testSynthMasks.npy')
trainX = trainX.astype('float32')/trainX.max()
testX = testX.astype('float32')/testX.max()
trainY = np.squeeze(trainY,axis = 4)
testY = np.squeeze(testY,axis =4)

inputs = Input((512,512,1))
zeros = ZeroPadding2D(padding=(8, 8))(inputs)
conv1 = Conv2D(64,(3,3),padding = 'valid', activation='relu')(zeros)
conv2 = Conv2D(64,(3,3),padding = 'valid', activation = 'relu')(conv1)
pool1 = MaxPool2D((2,2),padding = 'valid',strides=2)(conv2)
conv3 = Conv2D(128,(3,3), padding='valid',activation='relu')(pool1)
pool2 = MaxPool2D((2,2),padding='valid',strides = 2)(conv3)
conv5 = Conv2D(256,(3,3),padding = 'valid',activation='relu')(pool2)
up1 = UpSampling2D((2,2))(conv5)
up2 = UpSampling2D((2,2))(up1)
norm1 = BatchNormalization()(up2)
final = Conv2D(1,(1,1),activation='softmax')(norm1)
model3 = Model(inputs=inputs,outputs=final)

model3.compile(loss='binary_crossentropy', optimizer=Adam(lr=1e-4), metrics=['accuracy'])
callbacks_list = [EarlyStopping(monitor='val_acc',patience=1),ModelCheckpoint(filepath='/global/scratch/cgroschner/encoder3000train.h5',monitor ='val_acc', save_best_only=True)]

model3.fit(trainX, trainY,batch_size=20,epochs=5,verbose=1,shuffle=True, callbacks=callbacks_list,validation_data=(testX,testY))
model.save('/global/scratch/cgroschner/encoder3000train.h5')
predY = model.predict(testX,batch_size=10,verbose=1)
print(metrics.binary_accuracy(testY, predY))
