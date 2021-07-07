from PyQt5 import QtSql, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from loginUI import Ui_Form
from outwindow import UI_outDialog
import sys

class myApp(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(myApp, self).__init__()
        self.setupUi(self)
        self.openDB()
        self.pushButton.clicked.connect(self.checkUser)

        self._new_window = None
        self.Videocapture_ = None

    def refreshAll(self):
        self.Videocapture_ = "1"

    def openDB(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("data.sqlite")
        if not self.db.open():
            print("Error")
        self.query = QtSql.QSqlQuery()

    def checkUser(self):
        usersname = self.lineEdit.text()
        password = self.lineEdit_2.text()
        print(usersname, password)
        self.query.exec_("select * from userdata where username = '%s' and pass = '%s';"%(usersname, password))
        self.query.first()
        if self.query.value("username") != None and self.query.value("pass") != None:
            print("Longin success!!!")
            self.refreshAll()
            print(self.Videocapture_)
            Form.hide()
            self.outputwindow_()
        else:
            print("Longin fail!!")
            self.show_err()

    def show_err(self):
        mess = QMessageBox()
        mess.setWindowTitle("Error")
        mess.setText("Your User Name or Password is wrong.Plese Try again!!")
        mess.setIcon(QMessageBox.Warning)
        mess.setStandardButtons(QMessageBox.Retry|QMessageBox.Cancel)
        

        x = mess.exec_()

    def outputwindow_(self):
        self._new_window = UI_outDialog()
        self._new_window.show()
        

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        Form = myApp()
        Form.show()
        sys.exit(app.exec_())