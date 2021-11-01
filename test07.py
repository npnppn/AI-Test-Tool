# 학습하기 페이지
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.set_style()

    # 스타일 가져오기
    def set_style(self):
        with open("updateStyle", 'r') as f:
            self.setStyleSheet(f.read())

    # 메인페이지
    def initUI(self):
        pretreatmentButton = QPushButton('전처리하기')
        learningButton = QPushButton('학습하기')
        testButton = QPushButton('Test')
        testComButton = QPushButton('Test 비교')

        # 버튼 이벤트
        testButton.clicked.connect(self.testOpen)
        learningButton.clicked.connect(self.learningOpen)

        # 박스 레이아웃
        h2box = QVBoxLayout()
        h2box.addStretch(1)
        h2box.addWidget(pretreatmentButton)
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
        self.learning = QDialog()

        self.setWindowTitle('main')
        # 창 크기 고정
        self.setFixedSize(800, 600)
        # 창 반응형
        # self.setGeometry(550, 100, 800, 600)
        self.center()
        self.testOpen()
        # self.show()

    # 메인페이지 중앙 위치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 학습 페이지
    def learningOpen(self):
        # print(self.learning.width())
        # print(self.learning.height())

        # self.learning = QDialog()
        # 이미지 불러오기
        self.pixmapLearning = QPixmap('./test/img01.jpg')
        self.lbl_imgLearning = QLabel()
        self.lbl_imgLearning.setPixmap(self.pixmapLearning)
        # self.lbl_img.setContentsMargins(10, 10, 10, 10)
        # 사이즈 조정
        self.pixmapLearning = self.pixmapLearning.scaled(700, 700)
        # self.pixmapLearning = self.pixmapLearning.scaled(self.learning.width()/3, self.learning.height()/3)
        # self.lbl_imgLearning = QLabel('Width: ' + str(self.pixmapLearning.width()) + ', Height: ' + str(self.pixmapLearning.height()))   # 원래 사진크기
        self.lbl_imgLearning.setPixmap(self.pixmapLearning)

        # 리스트 불러오기
        path = './test'
        fileList = os.listdir(path)

        # QListWidget 추가
        self.listwidgetLearning = QListWidget(self)

        for f in fileList:
            self.listwidgetLearning.addItem(f)

        # 리스트 클릭 이벤트
        self.listwidgetLearning.itemClicked.connect(self.chkItemClicked2)

        # 폰트 및 글자
        label0 = QLabel('Input \n 파일 리스트', self)
        label0.setAlignment(Qt.AlignCenter)
        font0 = label0.font()
        font0.setPointSize(20)
        font0.setBold(True)
        label3 = QLabel('파라미터', self)
        label3.setAlignment(Qt.AlignCenter)
        font3 = label3.font()
        font3.setPointSize(20)
        font3.setBold(True)
        label10 = QLabel('저장할 모델 이름', self)
        label10.setAlignment(Qt.AlignCenter)
        font10 = label10.font()
        font10.setPointSize(10)
        font10.setBold(True)
        label0.setFont(font0)
        label3.setFont(font3)
        label10.setFont(font10)

        # 박스 레이아웃

        # 이미지 박스
        imgBox = QHBoxLayout()
        imgBox.addWidget(self.lbl_imgLearning)

        # 중간
        vbox = QVBoxLayout()
        # vbox.addWidget(self.lbl_img)
        vbox.addLayout(imgBox)
        vbox.addStretch(2)              # 그래프 넣을 곳

        # 좌측 (리스트)
        listBox = QVBoxLayout()
        listBox.addWidget(label0)
        listBox.addWidget(self.listwidgetLearning)

        # 결과
        label5 = QLabel('Epoch', self)
        label11 = QLabel('learning_rate', self)
        label12 = QLabel('batch_size', self)

        epoch = QLineEdit(self)
        learning_rate = QLineEdit(self)
        batch_size = QLineEdit(self)
        qle = QLineEdit(self)

        # 우측 하단 버튼
        startLearning = QPushButton('학습 하기')
        getModel = QPushButton('모델 추출')
        testButton = QPushButton('Test 하기')

        # 결과값 박스 레이아웃
        resultBox = QVBoxLayout()
        resultBox.addWidget(label3)
        resultBox.addStretch(1)
        resultBox.addWidget(label5)
        resultBox.addWidget(epoch)
        resultBox.addStretch(1)
        resultBox.addWidget(label11)
        resultBox.addWidget(learning_rate)
        resultBox.addStretch(1)
        resultBox.addWidget(label12)
        resultBox.addWidget(batch_size)
        resultBox.addStretch(2)
        resultBox.addWidget(label10)
        resultBox.addWidget(qle)
        resultBox.addStretch(3)
        resultBox.addWidget(startLearning)
        resultBox.addWidget(getModel)
        resultBox.addWidget(testButton)
        resultBox.addStretch(1)

        # 버튼 클릭 이벤트
        testButton.clicked.connect(self.testOpen)

        startLearning.clicked.connect(self.roding)

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

        self.learning.setLayout(hbox)

        self.roding = QDialog()

        # QDialog 세팅
        self.learning.setWindowTitle('learning')
        self.learning.setWindowModality(Qt.NonModal)
        # 반응형
        # self.dialog.setGeometry(350, 100, 1200, 800)
        # 크기 고정
        self.learning.setFixedSize(1200, 800)
        # self.learning.setStyleSheet("background-color: black; color: white;")
        self.learning.show()
        # 메인페이지 종료
        self.hide()

    # 테스트 페이지
    def testOpen(self):

        # self.dialog = QDialog()

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

        self.pixmap3 = QPixmap('./mask/img01.png')
        self.lbl_img3 = QLabel()
        self.lbl_img3.setPixmap(self.pixmap3)
        self.lbl_img3.setContentsMargins(0, 10, 0, 10)
        # 사이즈 조정
        self.pixmap3 = self.pixmap3.scaled(200, 200)
        self.lbl_img3.setPixmap(self.pixmap3)


        # 리스트 불러오기
        path = './test'
        fileList = os.listdir(path)


        # QListWidget 추가
        self.listwidget = QListWidget(self)

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
        # 폰트 적용
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
        subImgBox.addWidget(self.lbl_img3)
        subImgBox.addStretch(1)

        # 이미지 박스
        imgBox = QHBoxLayout()
        imgBox.addWidget(self.lbl_img)
        imgBox.addLayout(subImgBox)

        # 중간
        vbox = QVBoxLayout()
        vbox.addLayout(imgBox)
        vbox.addStretch(2)              # 그래프 넣을 곳

        # 좌측 (리스트)
        listBox = QVBoxLayout()
        listBox.addWidget(label0)
        listBox.addWidget(self.listwidget)

        # 결과
        self.epoch = QLabel("0", self)

        label5 = QLabel('Epoch', self)
        label6 = QLabel('Iteration', self)
        label7 = QLabel('Loss', self)
        label8 = QLabel('Accuracy', self)
        label9 = QLabel('Error Rate', self)
        label11 = QLabel('learning_rate', self)
        label12 = QLabel('batch_size', self)

        path = './test01'
        fileList = os.listdir(path)

        # 모델 선택
        cb = QComboBox(self)
        for f in fileList:
            cb.addItem(f)
        cb.move(50, 50)

        startTest = QPushButton('Test 하기')
        getModel = QPushButton('모델 추출')
        testComButton = QPushButton('Test 비교하기')

        resultBox = QVBoxLayout()
        resultBox.addWidget(label3)
        resultBox.addStretch(1)
        resultBox.addWidget(label5)
        resultBox.addWidget(self.epoch)
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

        startTest.clicked.connect(self.roding2)

        # 가로
        hbox = QHBoxLayout()
        hbox.addLayout(listBox)
        # 비율
        hbox.setStretchFactor(listBox, 2)
        hbox.addLayout(vbox)
        hbox.setStretchFactor(vbox, 6)
        hbox.addLayout(resultBox)
        hbox.setStretchFactor(resultBox, 2)

        # hbox.addWidget(self.lbl_img4)
        # hbox.addStretch(1)              # 결과값 넣을 곳

        self.dialog.setLayout(hbox)

        self.pixmap4 = QPixmap('./mask/img01.png')
        self.lbl_img4 = QLabel(self.dialog)
        self.lbl_img4.setPixmap(self.pixmap4)
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img4)
        opacity_effect.setOpacity(0.2)
        self.lbl_img4.setGraphicsEffect(opacity_effect)
        self.pixmap4 = self.pixmap4.scaled(450, 500)
        self.lbl_img4.setPixmap(self.pixmap4)
        self.lbl_img4.setGeometry(252, 19, 450, 500)

        # self.roding2 = QDialog()

        # QDialog 세팅
        self.dialog.setWindowTitle('Dialog')
        self.dialog.setWindowModality(Qt.NonModal)
        # self.dialog.setGeometry(350,100,1200,800)
        self.dialog.setFixedSize(1200, 800)
        # self.dialog.setStyleSheet("background-color: black; color: white;")
        self.hide()
        self.learning.hide()
        self.dialog.show()

    # 리스트 클릭시 이미지 변경 ( test )
    def chkItemClicked(self):
        # print(self.listwidget.currentItem().text())
        self.pixmap = QPixmap('./test/'+self.listwidget.currentItem().text())

        self.pixmap = self.pixmap.scaled(450,500)
        self.lbl_img.setPixmap(self.pixmap)

        self.pixmap2 = self.pixmap.scaled(200, 200)
        self.lbl_img2.setPixmap(self.pixmap2)

        s = self.listwidget.currentItem().text().split(".")
        print(s[0])
        self.pixmap3 = QPixmap('./mask/' + s[0] + ".png")
        self.pixmap3 = self.pixmap3.scaled(200, 200)
        self.lbl_img3.setPixmap(self.pixmap3)

        self.pixmap4 = QPixmap('./mask/' + s[0] + ".png")
        self.lbl_img4.setPixmap(self.pixmap4)
        self.pixmap4 = self.pixmap4.scaled(450, 500)
        self.lbl_img4.setPixmap(self.pixmap4)
        self.lbl_img4.setGeometry(252, 19, 450, 500)

    # 리스트 클릭시 이미지 변경
    def chkItemClicked2(self):
        print(self.listwidgetLearning.currentItem().text())
        self.pixmapLearning = QPixmap('./test/'+self.listwidgetLearning.currentItem().text())

        self.pixmapLearning = self.pixmapLearning.scaled(700,700)
        self.lbl_imgLearning.setPixmap(self.pixmapLearning)

    def roding(self):
        # 투명 다이로그
        self.learning.setWindowOpacity(0.8);
        label0 = QLabel('학습 중 ...', self)
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
        self.roding.show()

    def roding2(self):
        # self.dialog.hide()
        # self.dialog.setStyleSheet("background:transparent")
        # # self.dialog.setWindowFlag(Qt.FramelessWindowHint)
        # self.dialog.setAttribute(Qt.WA_TranslucentBackground)
        self.dialog.setWindowOpacity(0.8);
        # self.dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        # self.dialog.setAttribute(Qt.WA_TranslucentBackground)

        epoch = 1
        # 결과 값 변경
        self.epoch.setText(str(epoch))

        self.roding2 = QDialog()
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

        cancelButton.clicked.connect(self.cancel2)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(h2box)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.roding2.setLayout(vbox)


        self.roding2.setWindowTitle('roding')
        self.roding2.setWindowModality(Qt.ApplicationModal)
        self.roding2.setFixedSize(600, 400)
        # self.dialog.setStyleSheet("background-color: black;")
        self.roding2.show()

    def cancel(self):
        self.roding.hide()
        self.learning.setWindowOpacity(1);
    def cancel2(self):
        self.roding2.hide()
        self.dialog.setWindowOpacity(1);


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())