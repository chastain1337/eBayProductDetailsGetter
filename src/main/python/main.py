from fbs_runtime.application_context.PyQt5 import ApplicationContext
# , QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
from PyQt5.QtWidgets import QMainWindow
#from PyQt5.QtCore import pyqtSlot
#import api
import mainWindowUI
import sys
import os

if __name__ == '__main__':
    appctxt = ApplicationContext()

    # Set stylesheet
    appctxt.app.setStyleSheet(open('styles.css').read())

    MainWindow = QMainWindow()
    ui = mainWindowUI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(appctxt.app.exec_())
