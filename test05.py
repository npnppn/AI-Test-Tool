# 학습하기 페이지
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    #   self.set_style()

    # 스타일 가져오기
    # def set_style(self):
    #    with open("updateStyle", 'r') as f:
    #        self.setStyleSheet(f.read())

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
        self.gray = QDialog()

        self.setWindowTitle('main')
        # 창 크기 고정
        self.setFixedSize(800, 600)
        # 창 반응형
        # self.setGeometry(550, 100, 800, 600)
        self.center()
        # self.testOpen()
        self.show()

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
        resultBox = QFormLayout()  # QFormLayout 생성
        self.epoch_widget = QLineEdit()
        self.learn_widget = QLineEdit()
        self.batch_widget = QLineEdit()
        self.model_widget = QLineEdit()

        space_widget = QLabel("\n")  # 빈 공간 만드는 위젯

        label5 = QLabel('Epoch', self)
        label11 = QLabel('learning_rate', self)
        label12 = QLabel('batch_size', self)

        #epoch = QLineEdit(self)
        #learning_rate = QLineEdit(self)
        #batch_size = QLineEdit(self)
        #qle = QLineEdit(self)

        resultBox.addRow(label3)
        resultBox.addRow(space_widget)
        resultBox.addRow("Epoch ", self.epoch_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("Iteration ", self.learn_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("Loss ", self.batch_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow(label10)
        resultBox.addRow(self.model_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow(space_widget)

        # 우측 하단 버튼
        startLearning = QPushButton('학습 하기')
        getModel = QPushButton('모델 추출')
        testButton = QPushButton('Test 하기')

        # 결과값 박스 레이아웃

        resultBox.addRow(startLearning)
        resultBox.addRow(getModel)
        resultBox.addRow(testButton)


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

        self.pixmap5 = QPixmap('./img/dark.png')
        self.lbl_img5 = QLabel(self.learning)
        self.lbl_img5.setPixmap(self.pixmap5)
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img5)
        opacity_effect.setOpacity(0.5)
        self.lbl_img5.setGraphicsEffect(opacity_effect)
        self.pixmap5 = self.pixmap5.scaled(1200, 800)
        self.lbl_img5.setPixmap(self.pixmap5)
        self.lbl_img5.setGeometry(0, 0, 0, 0)

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
        font4.setPointSize(12)
        font4.setBold(True)
        label10 = QLabel('모델 선택', self)
        label10.setAlignment(Qt.AlignCenter)
        font10 = label10.font()
        font10.setPointSize(12)
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

        # 결과값 화면 보여주는 공간 배치

        # 변수받는 공간
        resultBox = QFormLayout()  # QFormLayout 생성
        self.epoch_widget = QLabel("3")
        self.iter_widget = QLabel("20")
        self.loss_widget = QLabel("0.02")
        self.accuracy_widget = QLabel("99.7%")
        self.error_widget = QLabel("0.3%")
        self.learning_widget = QLabel("2")
        self.batch_widget = QLabel("1")
        space_widget = QLabel("\n") #빈 공간 만드는 위젯

        # 행 추가하는 공간
        resultBox.addRow(label3) #결과값
        resultBox.addRow("Epoch ", self.epoch_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("Iteration ", self.iter_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("Loss ", self.loss_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("Accuracy ", self.accuracy_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("Error Rate ", self.error_widget)
        resultBox.addRow(space_widget)

        resultBox.addRow(label4) #적용된 패러미터
        resultBox.addRow("Learning_Rate ", self.learning_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("Batch_Size ", self.batch_widget)
        resultBox.addRow(space_widget)

        resultBox.addRow(label10) #모델 선택
        resultBox.addRow(cb)
        resultBox.addRow(space_widget)
        resultBox.addRow(space_widget)

        resultBox.addRow(startTest)
        resultBox.addRow(getModel)
        resultBox.addRow(testComButton)

        #색깔 변경은 어떻게 할까?
        self.setStyleSheet('color: blue; background:rgb(255,0,0)')

        self.setLayout(resultBox)
        self.show()

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


        self.pixmap5 = QPixmap('./img/dark.png')
        self.lbl_img5 = QLabel(self.dialog)
        self.lbl_img5.setPixmap(self.pixmap5)
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img5)
        opacity_effect.setOpacity(0.5)
        self.lbl_img5.setGraphicsEffect(opacity_effect)
        self.pixmap5 = self.pixmap5.scaled(1200, 800)
        self.lbl_img5.setPixmap(self.pixmap5)
        self.lbl_img5.setGeometry(0, 0, 0, 0)


        # self.roding2 = QDialog()

        # QDialog 세팅
        self.dialog.setWindowTitle('Dialog')
        self.dialog.setWindowModality(Qt.NonModal)
        # self.dialog.setGeometry(350,100,1200,800)
        self.dialog.setFixedSize(1200, 800)
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
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img5)
        opacity_effect.setOpacity(0.5)
        self.lbl_img5.setGraphicsEffect(opacity_effect)
        self.lbl_img5.setGeometry(0, 0, 1200, 800)

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
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img5)
        opacity_effect.setOpacity(0.5)
        self.lbl_img5.setGraphicsEffect(opacity_effect)
        self.lbl_img5.setGeometry(0, 0, 1200, 800)

        epoch = 1
        # 결과 값 변경
        self.epoch_widget.setText(str(epoch))

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
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img5)
        opacity_effect.setOpacity(0.5)
        self.lbl_img5.setGraphicsEffect(opacity_effect)
        self.lbl_img5.setGeometry(0, 0, 0, 0)

    def cancel2(self):
        self.roding2.hide()

        opacity_effect = QGraphicsOpacityEffect(self.lbl_img5)
        opacity_effect.setOpacity(0.5)
        self.lbl_img5.setGraphicsEffect(opacity_effect)
        self.lbl_img5.setGeometry(0, 0, 0, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
