import time
import scapy.all as S
import yara
from threading import Thread
import pyautogui
from UI_mainWindow import *
from PyQt5.QtCore import  QCoreApplication
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.name = pyautogui.prompt("출력파일 이름을 입력해주세요^^")
        if bool(self.name) == False:
            exit()
        super().__init__()
        self.setupUi(self)  #UI_MainWindow의 함수 부분 즉, 화면 출력 하는 부분
        #self.setWindowTitle("Packet_Analysis")
        # self.resize(900, 600)
        # self.stack = QtWidgets.QStackedLayout(self)
        # self.stack2 = SecondWindow(self)
        # self.stack.addWidget(self)
        # self.stack.addWidget(self.stack2)
        self.thread1 = None
        self.pushButton.clicked.connect(self.start_getSelectedItem)  # 버튼 누르면 실행되는 부분
        self.pushButton_2.clicked.connect(QCoreApplication.instance().quit) # 버튼 누르면 종료
    def start_getSelectedItem(self):  # 파일이 커지면 ui에서 멈추기때문에 쓰레드 사용
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.thread1 = Thread(target=self.getSelectedItem, args=())
        self.thread1.start()

        time.sleep(0.1) #안붙이면 이상하게 쓰레드와 pyqt5가 충돌이나서 sleep을검

    def getSelectedItem(self):  # 경로 및 분석구간
        # return item.text()
        # layout.addWidget(self.pushButton)
        item = QListWidgetItem(self.listView.currentItem())
        file_path = item.text()
        if bool(file_path) == False:
            self.alert1 = pyautogui.alert('분석할 파일을 클릭하고 눌러주세요')
            self.pushButton.setEnabled(True)  # 작업 시작 버튼
            self.pushButton_2.setEnabled(True) #작업 종료 버튼
        else:
            self.progressBar.setRange(0, 0)
            pkts = S.rdpcap(file_path)  # 업로드한 pcap파일 읽어오는 곳
            self.progressBar.setMaximum(len(pkts))
            result = []
            rules = yara.compile("rule")  # yara룰 매칭부분
            for i, pkt in enumerate(pkts):
                self.progressBar.setValue(i)
                try:
                    matched = rules.match(data=pkt.payload[2].load)  # 페이로드 부분에 야라룰 매치
                    if matched:
                        result.append(pkt)  # 매치가 되면 result 리스트에 저장
                except:
                    continue
            S.wrpcap(self.name + '.pcap', result)  # 리스트를 pcap파일로 출력 self.name은 이름출력
            self.progressBar.reset()  # 다중 반복 시 진행률표시 바 초기화
            self.pushButton.setEnabled(True)  # 다시 버튼 활성화
            self.pushButton_2.setEnabled(True)
            pyautogui.alert('분석이 완료되었습니다.\n다른 파일도 선택하여 분석 가능합니다.')
        # self.show()


app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec()