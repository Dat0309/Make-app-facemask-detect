import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
import resource
#from outwindow import Ui_OutputDialog
from outwindow import UI_outDialog

class UI_Dialog(QDialog):
    def __init__(self):
        super(UI_Dialog, self).__init__()
        loadUi('mainwindow.ui',self)

        self.runButton.clicked.connect(self.runSlot)

        self._new_window = None
        self.Videocapture_ = None

    def refreshAll(self):
        self.Videocapture_ = "1"

    @pyqtSlot()
    def runSlot(self):
        '''
        Hàm được gọi khi người dùng nhấn nút Run trong cửa sổ chính
        '''
        print("Clicked Run")
        self.refreshAll()
        print(self.Videocapture_)
        ui.hide() #hide the main window
        self.outputwindow_() #Create and open new output window

    def outputwindow_(self):
        '''
        Cửa sổ hiển thị video trên GUI
        '''
        self._new_window = UI_outDialog()
        self._new_window.show()
        # self._new_window.startVideo(self.Videocapture_)
        print("Video Played")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI_Dialog()
    ui.show()
    sys.exit(app.exec_())