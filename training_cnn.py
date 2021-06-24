from keras import activations
from keras import callbacks
from keras.backend import flatten
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Activation,Flatten,Dropout
from keras.layers import Conv2D,MaxPooling2D
from keras.callbacks import ModelCheckpoint
from numpy.core.defchararray import mod
from sklearn.model_selection import train_test_split
from sklearn.utils import validation
from matplotlib import pyplot as plt

data = np.load('data.npy')
target = np.load('target.npy')

model = Sequential()

#Trích lọc đặc trưng của ảnh
#Lớp CNN đầu tiên, theo sau là các lớp Relu và MaxPooling
model.add(Conv2D(200,(3,3),input_shape = data.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

#Lớp thứ hai 
model.add(Conv2D(100,(3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

#Làm phẳng lớp để xếp chồng output Convolution từ second convolution layer
model.add(Flatten())
model.add(Dropout(0.5))

#Tạo lớp Dense gồm 50 neural
model.add(Dense(50,activation='relu'))
#Lớp cuối cùng với 2 output
model.add(Dense(2,activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer='adam', metrics=['accuracy'])

#Test
train_data, test_data, train_target, test_target = train_test_split(data,target,test_size=0.1)

checkpoint = ModelCheckpoint('model-{epoch:03d}.model',monitor='val_loss',verbose=0,save_best_only=True, mode = 'auto')
history = model.fit(train_data,train_target,epochs=20, callbacks=[checkpoint],validation_split=0.2)

plt.plot(history.history['loss'], 'r', label = 'training loss')
plt.plot(history.history['val_loss'], label = 'validation loss')
plt.xlabel('# epochs')
plt.ylabel('loss')
plt.legend()
plt.show()


plt.plot(history.history['accuracy'],'r',label='training accuracy')
plt.plot(history.history['val_accuracy'],label='validation accuracy')
plt.xlabel('# epochs')
plt.ylabel('loss')
plt.legend()
plt.show()

print(model.evaluate(test_data,test_target))