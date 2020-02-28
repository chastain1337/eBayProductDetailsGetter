from PyQt5 import QtCore, QtGui, QtWidgets
import api
import sys
import threading


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.folder = None

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(515, 515)
        MainWindow.setWindowTitle
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")

        spacerItem = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.HeaderLabel = QtWidgets.QLabel(self.centralwidget)
        self.HeaderLabel.setTextFormat(QtCore.Qt.AutoText)
        self.HeaderLabel.setObjectName("HeaderLabel")

        self.tokenInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.tokenInput.setObjectName("tokenInput")

        self.startDateLabel = QtWidgets.QLabel(self.centralwidget)
        self.startDateLabel.setObjectName("startDateLabel")

        self.startDatePicker = QtWidgets.QDateEdit(self.centralwidget)
        self.startDatePicker.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.startDatePicker.setCalendarPopup(True)
        self.startDatePicker.setDate(QtCore.QDate(2014, 1, 1))
        self.startDatePicker.setObjectName("startDatePicker")

        self.endDateLabel = QtWidgets.QLabel(self.centralwidget)
        self.endDateLabel.setObjectName("endDateLabel")

        self.endDatePicker = QtWidgets.QDateEdit(self.centralwidget)
        self.endDatePicker.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.endDatePicker.setCalendarPopup(True)
        self.endDatePicker.setDate(QtCore.QDate(2014, 1, 1))
        self.endDatePicker.setObjectName("endDatePicker")

        self.browseLabel = QtWidgets.QLabel(self.centralwidget)
        self.browseLabel.setObjectName("browseLabel")

        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setObjectName("browseButton")
        self.browseButton.clicked.connect(self.launchBrowse)

        self.getButton = QtWidgets.QPushButton(self.centralwidget)
        self.getButton.setObjectName("getButton")
        self.getButton.clicked.connect(self.onClick)

        self.status_dateRange = QtWidgets.QLabel(
            self.centralwidget)  # current date range (max 120 days)
        self.status_dateRange.setObjectName("status_dateRange")
        self.status_numberofEntries = QtWidgets.QLabel(
            self.centralwidget)  # total entires in that date range
        self.status_numberofEntries.setObjectName("status_numberofEntries")
        self.status_pageNumber = QtWidgets.QLabel(
            self.centralwidget)       # page number
        self.status_pageNumber.setObjectName("status_pageNumber")
        self.status_totalNumberOfEntries = QtWidgets.QLabel(
            self.centralwidget)  # total entires
        self.status_totalNumberOfEntries.setObjectName(
            "status_totalNumberOfEntries")
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.errorMessage = QtWidgets.QLabel(self.centralwidget)
        self.errorMessage.setObjectName("errorMessage")

        # Mount everything to the form in order
        self.mountWidgetInForm(self.HeaderLabel)
        self.mountWidgetInForm(self.tokenInput)
        self.formLayout.setItem(
            self.indexCounter, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.indexCounter += 1
        self.mountWidgetInForm(self.startDateLabel)
        self.mountWidgetInForm(self.startDatePicker)
        self.mountWidgetInForm(self.endDateLabel)
        self.mountWidgetInForm(self.endDatePicker)
        self.mountWidgetInForm(self.browseLabel)
        self.mountWidgetInForm(self.browseButton)
        self.formLayout.setItem(
            self.indexCounter, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.indexCounter += 1
        self.mountWidgetInForm(self.getButton)
        self.mountWidgetInForm(self.errorMessage)
        self.formLayout.setItem(
            self.indexCounter, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.indexCounter += 1
        self.mountWidgetInForm(self.status_dateRange)
        self.mountWidgetInForm(self.status_pageNumber)
        self.mountWidgetInForm(self.status_numberofEntries)
        self.mountWidgetInForm(self.status_totalNumberOfEntries)

        self.retranslateUi(MainWindow)

    indexCounter = 0

    def launchBrowse(self):
        fileDialogue = QtWidgets.QFileDialog()
        fileDialogue.setFileMode(QtWidgets.QFileDialog.Directory)
        self.folder = fileDialogue.getExistingDirectory(
            self.centralwidget, "Choose Folder", "")
        if not self.folder is None:
            self.browseLabel.setText(self.folder)

    def mountWidgetInForm(self, widget):
        self.formLayout.setWidget(
            self.indexCounter, QtWidgets.QFormLayout.LabelRole, widget)
        self.indexCounter += 1

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "eBay Product Details Getter"))
        self.tokenInput.setPlaceholderText(
            _translate("MainWindow", "Paste Token"))
        self.startDateLabel.setText(_translate("MainWindow", "Start Date"))
        self.endDateLabel.setText(_translate("MainWindow", "End Date"))
        self.getButton.setText(_translate("MainWindow", "Get Product Details"))
        self.HeaderLabel.setText(_translate(
            "MainWindow", "eBay Details Getter"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))
        self.browseLabel.setText(_translate(
            "MainWindow", "Choose File(s) Destination"))

    def setErrorMessage(self, msg):
        self.errorMessage.setText("An error has occured:<br>%s" % msg)

    def clearErrorMessage(self):
        self.errorMessage.setText("")

    def onClick(self):

        self.getButton.setDisabled(True)
        self.clearErrorMessage()
        try:
            if not self.folder is None:
                handleThread = threading.Thread(
                    target=api.handleClick, args=(self,))
                handleThread.start()
            else:
                self.setErrorMessage("No folder selected.")
                self.getButton.setDisabled(False)
        except Exception as e:
            self.setErrorMessage(e)
            self.getButton.setDisabled(False)
