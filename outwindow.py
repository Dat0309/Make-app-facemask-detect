import sys
import cv2 as cv
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from tensorflow.keras.models import load_model
import numpy as np
import resource

from numpy.core.fromnumeric import resize

class UI_outDialog(QDialog):
    
    
    def __init__(self):
        super(UI_outDialog, self).__init__()

        loadUi("outwindow.ui", self)

        self.logic = 0
        self.value = 1

        self.showBtn.clicked.connect(self.onClicked)

        self.captureBtn.clicked.connect(self.CaptureClicked)


    @pyqtSlot()
    def onClicked(self):
        haar_cascade = cv.CascadeClassifier('haar_face.xml')
        model = load_model('mask_detectot.model')
        cap = cv.VideoCapture(0)
        labels_dict = {0:'Without Mask',1:'With Mask'}
        color_dict = {0:(0,0,255),1:(0,255,0)}

        while (cap.isOpened()): 
            ret, frame = cap.read()
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = haar_cascade.detectMultiScale(gray,1.3,5)

            for (x,y,w,h) in faces:
                face_img = gray[y:y+w,x:x+w]
                resized = cv.resize(face_img,(100,100))
                normalized = resized/255.0
                reshaped = np.reshape(normalized,(1,100,100,1))
                result = model.predict(reshaped)

                label = np.argmax(result, axis=1)[0]

                cv.rectangle(frame,(x,y),(x+w,y+h),color_dict[label],2)
                cv.rectangle(frame,(x,y-40),(x+w,y),color_dict[label],-1)
                cv.putText(frame,labels_dict[label], (x,y-10), cv.FONT_HERSHEY_COMPLEX, 0.8,(255,255,255),2)
            
            if ret == True:
                #print("Here")
                self.displayImage(frame, 1)

                if(self.logic==2):

                    self.value = self.value + 1
                    #path = r'D:\TỰ HỌC\Face-Recogntion-PyQt\Face_Detection_PyQt_base\ImagesAttendance\%s.png'%(self.value)
                    cv.imwrite('%s.png'%(self.value),frame)

                    self.logic = 1
                if cv.waitKey(20) & 0xFF == ord('q'):
                    break
            else:
                print("return not found")
        cap.release()
        cv.destroyAllWindows()

    def CaptureClicked(self):
        self.logic = 2

    def exitClicked(self):
        self.logic = 3

    def displayImage(self, img, window = 1):
        qformat = QImage.Format_Indexed8

        if len(img.shape) ==3:
            if (img.shape[2]) ==4:
                qformat = QImage.Format_RGBA888

            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(img))
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI_outDialog()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print('Exiting')

