from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QDialog
import cv2 as cv
import numpy as np
import os
from keras.models import load_model
from keras.saving.saved_model.load import load

class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi('outwindow.ui', self)
        self.image = None

    @pyqtSlot()
    def startVideo(self, camera_name):
        '''
        camera_name: link of camera or usb camera in Device
        '''
        if len(camera_name) == 1:
            self.capture = cv.VideoCapture(int(camera_name))
        else:
            self.capture = cv.VideoCapture(camera_name)
        
    def face_mask_rec_(self, frame):
        model = load_model('mask_detectot.model')

        haar_face = cv.CascadeClassifier('haar_face.xml')

        labels_dict = {1:'With Mask',0:'Without Mask'}
        color_dict = {0:(0,0,255),1:(0,255,0)}

        while(True):
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

            return frame

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, 1)

    def displayImage(self, image, window = 1):
        image = cv.resize(image,(995,520))
        try:
            image = self.face_mask_rec_(image)
        except Exception as e:
            print(e)
        
        qformat = QImage.Format_Indexed8
        if len(image.shape) ==3:
            if image.shape[2] ==4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0],image.strides[0],qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.label.setPixmap(QPixmap.fromImage(outImage))
            self.label.setScaledContents(True)