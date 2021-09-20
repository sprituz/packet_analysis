from PyQt5.QtCore import Qt, QUrl, QSize, QTimer,QThread
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QLabel
from PyQt5.QtWidgets import QMessageBox
import re





class ListBoxWidget(QListWidget):         #파일 경로들을 드래그앤 드롭으로 가져오는 부분
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        #self.resize(450, 450)       #리스트 박스 크기

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []                  #pcap or pcapng파일만 등록가능
            p = re.compile('[.].+')
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    ch = str(url.toLocalFile())
                    a = p.findall(ch) #.pcap or .pcapng list
                    ch2 = " ".join(a)
                    if ch2 == '.pcap' or ch2 == '.pcapng':
                        links.append(str(url.toLocalFile()))
                    else:
                        QMessageBox.information(self,'file extension','pcap or pcapng 파일만 넣어주세요.')
                else:
                    links.append(str(url.toString()))
            self.addItems(links)
        else:
            event.ignore()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout = QtWidgets.QGridLayout()
        #self.gridLayout.setObjectName("gridLayout")
        self.listView = ListBoxWidget(self.centralwidget)
        self.gridLayout.addWidget(self.listView, 0, 0, 1, 1)
        self.listView.setObjectName("listView")
        self.gridLayout_5.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_4.addWidget(self.pushButton, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_7.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_7, 1, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_2, 2, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Packet_Analysis"))
        self.label.setText(_translate("MainWindow", "pcap,pcapng파일을 드래그로 흰박스 안에 넣어주세요"))
        self.pushButton.setText(_translate("MainWindow", "작업 시작"))
        self.pushButton_2.setText(_translate("MainWindow", "작업 종료"))


