import sys, os
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton
import re
class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(300, 300)

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

            links = []
            p = re.compile('[.].+')
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                    ch = " ".join(links)
                    a = p.findall(ch)
                    ch2 = " ".join(a)
                    if ch2 == '.pcap' or ch2 == '.pcapng':
                        links.remove(str(url.toLocalFile()))
                        links.append(str(url.toLocalFile()))
                    else :
                        links.remove(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)
        else:
            event.ignore()

class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(900, 600)

        self.listbox_view = ListBoxWidget(self)

        self.btn = QPushButton('작업 시작', self)
        self.btn.setGeometry(450, 400, 200, 50)
        self.btn.clicked.connect(lambda: print(self.getSelectedItem()))

    def getSelectedItem(self):
        item = QListWidgetItem(self.listbox_view.currentItem())
        return item.text()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())