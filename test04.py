# 위치조정 및 로딩 중
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from PyQt5.QtGui import QIcon

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.set_style()

    def set_style(self):
        with open("updateStyle", 'r') as f:
            self.setStyleSheet(f.read())

    # 메인페이지
    def initUI(self):
        learningButton = QPushButton('학습하기')
        testButton = QPushButton('Test')
        testComButton = QPushButton('Test 비교')

        testButton.clicked.connect(self.testOpen)

        h2box = QVBoxLayout()
        h2box.addStretch(1)
        h2box.addWidget(learningButton)
        h2box.addWidget(testButton)
        h2box.addWidget(testComButton)
        h2box.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(h2box)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

        # QDialog 설정
        self.dialog = QDialog()

        self.setWindowTitle('test')
        # self.setGeometry(800, 800, 800, 600)
        self.setFixedSize(800, 600)
        self.center()
        self.show()

    # 중앙 이동
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 테스트 페이지
    def testOpen(self):
        # 이미지 불러오기
        self.pixmap = QPixmap('./test/img01.jpg')
        self.lbl_img = QLabel()
        self.lbl_img.setPixmap(self.pixmap)
        # self.lbl_img.setContentsMargins(10, 10, 10, 10)
        # 사이즈 조정
        self.pixmap = self.pixmap.scaled(450, 500)
        self.lbl_img.setPixmap(self.pixmap)

        self.lbl_img2 = QLabel()
        self.lbl_img2.setPixmap(self.pixmap)
        self.lbl_img2.setContentsMargins(0, 10, 0, 10)
        # 사이즈 조정
        self.pixmap2 = self.pixmap.scaled(200, 200)
        self.lbl_img2.setPixmap(self.pixmap2)

        # 리스트 불러오기
        path = './test'
        fileList = os.listdir(path)

        # QListWidget 추가
        self.listwidget = QListWidget(self)

        # self.listwidget.move(100, 100)
        # self.listwidget.resize(10000, 50000)  # width, heigt 만큼 크기 조절
        # model = QStandardItemModel()

        for f in fileList:
            self.listwidget.addItem(f)

        # 리스트 클릭 이벤트
        self.listwidget.itemClicked.connect(self.chkItemClicked)

        # 폰트 및 글자
        label0 = QLabel('Test \n 파일 리스트', self)
        label0.setAlignment(Qt.AlignCenter)
        font0 = label0.font()
        font0.setPointSize(20)
        font0.setBold(True)
        label1 = QLabel('원본 이미지', self)
        label1.setAlignment(Qt.AlignCenter)
        font1 = label1.font()
        font1.setPointSize(15)
        font1.setBold(True)
        label2 = QLabel('결함 마스크', self)
        label2.setAlignment(Qt.AlignCenter)
        font2 = label2.font()
        font2.setPointSize(15)
        font2.setBold(True)
        label3 = QLabel('결과값', self)
        label3.setAlignment(Qt.AlignCenter)
        font3 = label3.font()
        font3.setPointSize(20)
        font3.setBold(True)
        label4 = QLabel('적용된 parameter', self)
        label4.setAlignment(Qt.AlignCenter)
        font4 = label4.font()
        font4.setPointSize(10)
        font4.setBold(True)
        label10 = QLabel('모델 선택', self)
        label10.setAlignment(Qt.AlignCenter)
        font10 = label10.font()
        font10.setPointSize(10)
        font10.setBold(True)

        label0.setFont(font0)
        label1.setFont(font1)
        label2.setFont(font2)
        label3.setFont(font3)
        label4.setFont(font4)
        label10.setFont(font10)

        # 이미지 박스 (우측)
        subImgBox = QVBoxLayout()
        subImgBox.addWidget(label1)
        subImgBox.addWidget(self.lbl_img2)
        subImgBox.addWidget(label2)
        subImgBox.addStretch(1)

        # 이미지 박스
        imgBox = QHBoxLayout()
        imgBox.addWidget(self.lbl_img)
        imgBox.addLayout(subImgBox)

        # 중간
        vbox = QVBoxLayout()
        # vbox.addWidget(self.lbl_img)
        vbox.addLayout(imgBox)
        vbox.addStretch(2)              # 그래프 넣을 곳

        # 좌측 (리스트)
        listBox = QVBoxLayout()
        # listBox.resize(100, 600)
        # listBox.setSizePolicy(0,0,100,600)
        listBox.addWidget(label0)
        listBox.addWidget(self.listwidget)

        # 결과
        label5 = QLabel('Epoch', self)
        # label5.resize(50, 50)  # width, heigt 만큼 크기 조절
        label6 = QLabel('Iteration', self)
        label7 = QLabel('Loss', self)
        label8 = QLabel('Accuracy', self)
        label9 = QLabel('Error Rate', self)
        label11 = QLabel('learning_rate', self)
        label12 = QLabel('batch_size', self)

        path = './test'
        fileList = os.listdir(path)

        # 모델 선택
        cb = QComboBox(self)
        for f in fileList:
            cb.addItem(f)
        # cb.addItem('Option1')
        # cb.addItem('Option2')
        cb.move(50, 50)

        startTest = QPushButton('Test 하기')
        getModel = QPushButton('모델 추출')
        testComButton = QPushButton('Test 비교하기')

        resultBox = QVBoxLayout()
        resultBox.addWidget(label3)
        resultBox.addStretch(1)
        resultBox.addWidget(label5)
        resultBox.addStretch(1)
        resultBox.addWidget(label6)
        resultBox.addStretch(1)
        resultBox.addWidget(label7)
        resultBox.addStretch(1)
        resultBox.addWidget(label8)
        resultBox.addStretch(1)
        resultBox.addWidget(label9)
        resultBox.addStretch(1)
        resultBox.addWidget(label4)
        resultBox.addStretch(1)
        resultBox.addWidget(label11)
        resultBox.addStretch(1)
        resultBox.addWidget(label12)
        resultBox.addStretch(2)
        resultBox.addWidget(label10)
        resultBox.addWidget(cb)
        resultBox.addStretch(3)
        resultBox.addWidget(startTest)
        resultBox.addWidget(getModel)
        resultBox.addWidget(testComButton)
        resultBox.addStretch(1)


        startTest.clicked.connect(self.roding)

        # 가로
        hbox = QHBoxLayout()
        hbox.addLayout(listBox)
        # 비율
        hbox.setStretchFactor(listBox, 2)
        hbox.addLayout(vbox)
        hbox.setStretchFactor(vbox, 6)
        hbox.addLayout(resultBox)
        hbox.setStretchFactor(resultBox, 2)
        # hbox.addStretch(1)              # 결과값 넣을 곳

        self.dialog.setLayout(hbox)

        self.roding = QDialog()

        # QDialog 세팅
        self.dialog.setWindowTitle('Dialog')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setFixedSize(1200, 800)
        # self.dialog.setStyleSheet("background-color: black; color: white;")
        self.center()
        self.dialog.show()
        self.hide()


    def chkItemClicked(self):
        print(self.listwidget.currentItem().text())
        self.pixmap = QPixmap('./test/'+self.listwidget.currentItem().text())

        self.pixmap = self.pixmap.scaled(450,500)
        self.lbl_img.setPixmap(self.pixmap)

        self.pixmap2 = self.pixmap.scaled(200, 200)
        self.lbl_img2.setPixmap(self.pixmap2)

    def roding(self):
        label0 = QLabel('Test 중 ...', self)
        label0.setAlignment(Qt.AlignCenter)
        font0 = label0.font()
        font0.setPointSize(30)
        font0.setBold(True)

        label0.setFont(font0)

        cancelButton = QPushButton('Cancel')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(cancelButton)
        hbox.addStretch(1)

        h2box = QHBoxLayout()
        h2box.addStretch(1)
        h2box.addWidget(label0)
        h2box.addStretch(1)

        cancelButton.clicked.connect(self.cancel)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(h2box)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.roding.setLayout(vbox)

        self.roding.setWindowTitle('roding')
        self.roding.setWindowModality(Qt.ApplicationModal)
        self.roding.setFixedSize(600, 400)
        self.center()
        self.roding.show()

    def cancel(self):
        self.roding.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())