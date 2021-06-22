
from keras.models import load_model
import cv2 as cv
from keras.saving.saved_model.load import load
import numpy as np
import os

model = load_model('model-011.model')

haar_face = cv.CascadeClassifier('haar_face.xml')

source = cv.VideoCapture(0)

labels_dict = {0:'Without Mask',1:'With Mask'}
color_dict = {0:(0,0,255),1:(0,255,0)}

while(True):
    ret, frame = source.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces = haar_face.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        face_img = gray[y:y+w,x:x+w]
        resized = cv.resize(face_img,(100,100))
        normalized = resized/255.0
        reshaped = np.reshape(normalized,(1,100,100,1))
        result = model.predict(reshaped)

        label = np.argmax(result,axis=1)[0]

        cv.rectangle(frame,(x,y),(x+w,y+h),color_dict[label],2)
        cv.rectangle(frame,(x,y-40),(x+w,y),color_dict[label],-1)
        cv.putText(frame,labels_dict[label], (x,y-10), cv.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255),2)

    cv.imshow('Frame',frame)
    key = cv.waitKey(1)

    if(key==27):#ESC
        break

source.release()
cv.destroyAllWindows


