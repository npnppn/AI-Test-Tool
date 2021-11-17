import sys, os, glob
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import webbrowser

from data_read import *
from train import *
from util import *

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    # 메인페이지
    def initUI(self):
        pretreatmentButton = QPushButton('전처리하기')
        pretreatmentButton.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        pretreatmentButton.setToolTip(
            'datasets의 이미지를 변환시킵니다.')

        learningButton = QPushButton('학습하기')
        learningButton.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        learningButton.setToolTip(
            '모델을 학습시킵니다.')

        testButton = QPushButton('Test')
        testButton.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        testButton.setToolTip(
            '학습된 모델을 평가합니다.')

        testComButton = QPushButton('Test 비교')
        testComButton.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        testComButton.setToolTip(
            '서로 다른 모델을 비교합니다.')

        # 버튼 이벤트
        pretreatmentButton.clicked.connect(self.pretreatmentOpen)
        testButton.clicked.connect(self.testOpen)
        QApplication.processEvents()
        learningButton.clicked.connect(self.learningOpen)
        QApplication.processEvents()


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

        self.setWindowTitle('main')
        # 창 크기 고정
        self.setFixedSize(800, 600)
        # 창 반응형
        # self.setGeometry(550, 100, 800, 600)
        self.center()
        # self.testOpen()
        self.setStyleSheet("background-color: #0c4da2; color: white;")
        self.show()

    # 메인페이지 중앙 위치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 데이터 전처리
    def pretreatmentOpen(self):
        self.pretreatmentOpen = QDialog()
        label0 = QLabel('전처리 중 ...', self)
        label0.setAlignment(Qt.AlignCenter)
        font0 = label0.font()
        font0.setPointSize(30)
        font0.setBold(True)
        label0.setFont(font0)

        h2box = QHBoxLayout()
        h2box.addStretch(1)
        h2box.addWidget(label0)
        h2box.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(h2box)
        vbox.addStretch(1)
        vbox.addStretch(1)

        self.pretreatmentOpen.setLayout(vbox)

        self.pretreatmentOpen.setWindowTitle('Loading')
        self.pretreatmentOpen.setWindowModality(Qt.ApplicationModal)
        self.pretreatmentOpen.setFixedSize(600, 400)
        self.pretreatmentOpen.show()
        self.reset()

        data_read()
        self.learningOpen()

        self.cancel_pre()
        self.reset()


    # 학습 페이지
    def learningOpen(self):
        self.learning = QDialog()
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
        #self.lbl_img2.setContentsMargins(0, 10, 0, 10)
        # 사이즈 조정
        self.pixmap2 = self.pixmap.scaled(200, 200)
        self.lbl_img2.setPixmap(self.pixmap2)

        self.pixmap3 = QPixmap('./mask/img01.png')
        self.lbl_img3 = QLabel()
        self.lbl_img3.setPixmap(self.pixmap3)
        #self.lbl_img3.setContentsMargins(0, 10, 0, 10)
        # 사이즈 조정
        self.pixmap3 = self.pixmap3.scaled(200, 200)
        self.lbl_img3.setPixmap(self.pixmap3)

        # 리스트 불러오기
        path = './test'
        fileList = os.listdir(path)

        # QListWidget 추가
        self.listwidgetLearning = QListWidget(self)

        for f in fileList:
            self.listwidgetLearning.addItem(f.split(".")[0])

        # 리스트 클릭 이벤트
        self.listwidgetLearning.itemClicked.connect(self.chkItemClicked)

        # 폰트 및 글자
        label0 = QLabel('이미지 선택', self)
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
        label3 = QLabel('정보 입력', self)
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

        label1.setFont(font1)
        label2.setFont(font2)

        # 박스 레이아웃
        # 이미지 박스 (우측)
        subImgBox = QHBoxLayout()
        subImgBox.addWidget(self.lbl_img2, alignment=Qt.AlignHCenter)
        subImgBox.addWidget(self.lbl_img3, alignment=Qt.AlignHCenter)


        # 이미지 박스
        imgBox = QVBoxLayout()
        imgBox.addWidget(self.lbl_img, alignment=Qt.AlignHCenter)
        imgBox.addWidget(QLabel("\n"))
        imgBox.addLayout(subImgBox)

        imgName = QHBoxLayout()
        imgName.addWidget(label1)
        imgName.addWidget(label2)
        # 중간
        vbox = QVBoxLayout()
        vbox.addLayout(imgBox)
        vbox.addLayout(imgName)

        # 좌측 (리스트)
        listBox = QVBoxLayout()
        btn = QPushButton('뒤로')
        listBox.addWidget(btn)
        listBox.addWidget(label0)
        listBox.addWidget(self.listwidgetLearning)

        # 결과값 화면 보여주는 공간
        result_layout = QVBoxLayout()

        groupbox1 = QGroupBox("학습 정보")
        groupbox1.setAlignment(5)

        groupbox2 = QGroupBox("")
        groupbox2.setAlignment(5)

        # 결과

        resultBox = QFormLayout()  # QFormLayout 생성
        self.learn_widget = QLineEdit()
        self.learn_widget.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        self.learn_widget.setToolTip(
            '한 번의 학습으로 얼마만큼 학습해야 할지를 의미합니다.')

        self.batch_widget = QLineEdit()
        self.batch_widget.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        self.batch_widget.setToolTip(
            '전체 학습 데이터셋에서 몇 개의 데이터를 한 번에 학습할 것인지를 의미합니다.')

        self.model_widget = QLineEdit()
        self.model_widget.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        self.model_widget.setToolTip('저장할 모델의 이름을 입력해주세요.')

        self.epoch_widget = QLineEdit()
        self.epoch_widget.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        self.epoch_widget.setToolTip(
            '1epoch란 전체 데이터셋에 대해 한 번의 학습을 완료한 상태를 의미합니다.')

        space_widget = QLabel("\n")  # 빈 공간 만드는 위젯

        resultBox.addRow(label3)
        resultBox.addRow(space_widget)
        resultBox.addRow("모델 이름 ", self.model_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("Epoch ", self.epoch_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("Learning Rate ", self.learn_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("Batch Size ", self.batch_widget)

        startLearning = QPushButton('학습 시작', self)
        testButton = QPushButton('Test')

        learning_font = startLearning.font()
        test_font = testButton.font()

        learning_font.setPointSize(30)
        startLearning.setFont(learning_font)
        test_font.setPointSize(30)
        testButton.setFont(test_font)

        startLearning.setMaximumHeight(200)
        testButton.setMaximumHeight(200)

        # 버튼 클릭 이벤트
        testButton.clicked.connect(self.testOpen)
        startLearning.clicked.connect(self.loading)

        groupbox1.setLayout(resultBox)
        result_layout.addWidget(groupbox1)
        result_layout.addWidget(startLearning)
        result_layout.addWidget(testButton)
        self.setLayout(result_layout)
        self.show()


        # 가로
        hbox = QHBoxLayout()
        hbox.addLayout(listBox)
        # 비율
        hbox.setStretchFactor(listBox, 2)
        hbox.addLayout(vbox)
        hbox.setStretchFactor(vbox, 6)
        hbox.addLayout(result_layout)

        self.learning.setLayout(hbox)

        self.pixmap4 = QPixmap('./mask/img01.png')
        self.lbl_img4 = QLabel(self.learning)
        self.lbl_img4.setPixmap(self.pixmap4)
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img4)
        opacity_effect.setOpacity(0.2)
        self.lbl_img4.setGraphicsEffect(opacity_effect)
        self.pixmap4 = self.pixmap4.scaled(450, 500)
        self.lbl_img4.setPixmap(self.pixmap4)
        self.lbl_img4.setAlignment(Qt.AlignCenter)
        self.lbl_img4.setGeometry(324, 10, 450, 500)
        self.pixmap5 = QPixmap('./img/dark.png')
        self.lbl_img5 = QLabel(self.learning)
        self.lbl_img5.setPixmap(self.pixmap5)
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img5)
        opacity_effect.setOpacity(0.5)
        self.lbl_img5.setGraphicsEffect(opacity_effect)
        self.pixmap5 = self.pixmap5.scaled(1200, 800)
        self.lbl_img5.setPixmap(self.pixmap5)
        self.lbl_img5.setGeometry(0, 0, 0, 0)

        #self.loading = QDialog()

        # QDialog 세팅
        self.learning.setWindowTitle('Learning')
        self.learning.setWindowModality(Qt.NonModal)
        self.learning.setFixedSize(1200, 800)
        self.learning.setStyleSheet("background-color: #0c4da2; color: white;")
        self.learning.show()

    # 파일 열기 기능. 나중에 이 목록을 가져와서 리스트로 쭈욱 나열하면 될 듯
    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        imagePath = fname[0]
        self.pixmap = QPixmap(imagePath)
        self.pixmap = self.pixmap.scaled(700, 700)
        self.lbl_imgLearning.setPixmap(self.pixmap)

        # 리스트에 파일이름만 저장하려고
        image_name = fname[0]
        self.label.setText(image_name)
        self.listwidgetLearning.addItem(image_name.split("/")[-1])

    # 테스트 페이지
    def testOpen(self):
        self.testOpen_Di = QDialog()
        # 이미지 불러오기
        self.pixmap = QPixmap('./test/img01.jpg')
        self.lbl_img = QLabel()
        self.lbl_img.setPixmap(self.pixmap)
        # self.lbl_img.setContentsMargins(10, 10, 10, 10)
        # 사이즈 조정
        self.pixmap = self.pixmap.scaled(700, 700)
        # self.pixmapLearning = self.pixmapLearning.scaled(self.learning.width()/3, self.learning.height()/3)
        # self.lbl_imgLearning = QLabel('Width: ' + str(self.pixmapLearning.width()) + ', Height: ' + str(self.pixmapLearning.height()))   # 원래 사진크기
        self.lbl_img.setPixmap(self.pixmap)

        # 리스트 불러오기
        path = './result'

        fileList = os.listdir(path)

        # QListWidget 추가
        self.listwidget = QListWidget(self)
        self.listwidget.setSelectionMode(QAbstractItemView.ExtendedSelection)


        # 리스트 클릭 이벤트
        self.listwidget.itemClicked.connect(self.chkItemClicked2)


        # 아웃풋 이미지 주소
        self.test_model_path = ''

        # 폰트 및 글자
        label0 = QLabel('이미지 선택', self)
        label0.setAlignment(Qt.AlignCenter)
        font0 = label0.font()
        font0.setPointSize(20)
        font0.setBold(True)

        label10 = QLabel('\n' + '모델 선택', self)
        label10.setAlignment(Qt.AlignCenter)
        font10 = label10.font()
        font10.setPointSize(20)
        font10.setBold(True)
        label0.setFont(font0)

        label3 = QLabel('------------', self)
        label3.setAlignment(Qt.AlignCenter)
        font3 = label3.font()
        font3.setPointSize(20)
        font3.setBold(True)
        label3.setFont(font3)
        label10.setFont(font10)

        #버튼들
        startTest = QPushButton('Test')
        test_font = startTest.font()
        test_font.setPointSize(30)
        startTest.setFont(test_font)
        startTest.setMaximumHeight(200)

        buttonbox = QHBoxLayout()
        buttonbox.addWidget(startTest)


        #버튼 기능
        startTest.clicked.connect(self.loading2)

        # 이미지 박스
        imgBox = QHBoxLayout()
        imgBox.addWidget(self.lbl_img)

        # 중간
        vbox = QVBoxLayout()
        # vbox.addWidget(self.lbl_img)
        vbox.addLayout(imgBox)
        vbox.addLayout(buttonbox)

        # 모델 선택
        self.cb = QComboBox()
        self.cb.addItem("ㅡㅡㅡㅡ모델을 선택하세요ㅡㅡㅡㅡ")
        self.cb.setPlaceholderText("---모델을 선택하세요---")
        self.cb.setCurrentIndex(0)


        # 모델들 하위 경로 가져오기
        targetPattern = r"./" + "*/**/*.pth"
        cbList = glob.glob(targetPattern)
        self.test_model_arr = ['a.a']
        for f in cbList:
            self.test_model_arr.append(f)
            file = os.path.basename(f)
            self.cb.addItem(file)

        self.cb.move(50, 50)
        self.cb.currentTextChanged.connect(self.combobox_changed and self.selec_model)

        # 좌측 (리스트)
        listBox = QVBoxLayout()
        btn = QPushButton('뒤로')
        btn.clicked.connect(self.clickButton)
        listBox.addWidget(btn)
        listBox.addWidget(label0)
        listBox.addWidget(self.listwidget)

        # 결과값 화면 보여주는 공간
        epoch_value, loss_value, acc_value, iou_value, model_value, batch_value, learn_value = '', '', '', '', '', '', ''

        result_layout = QVBoxLayout()

        groupbox_model = QGroupBox("모델 정보")
        groupbox_model.setAlignment(5)

        groupbox_learn = QGroupBox("학습 정보")
        groupbox_learn.setAlignment(5)
        groupbox_image = QGroupBox("라벨/결과 비교")
        groupbox_image.setAlignment(5)

        self.epoch_widget = QLineEdit()
        self.epoch_widget.setReadOnly(True)
        self.epoch_widget.setText(epoch_value)
        self.epoch_widget.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        self.epoch_widget.setToolTip(
            '1epoch란 전체 데이터셋에 대해 한 번의 학습을 완료한 상태를 의미합니다.')

        self.loss_widget = QLineEdit()
        self.loss_widget.setReadOnly(True)
        self.loss_widget.setPlaceholderText(loss_value)
        self.loss_widget.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        self.loss_widget.setToolTip('정답과 예측한 값 사이의 오차를 의미합니다.')

        self.iou_widget = QLineEdit()
        self.iou_widget.setReadOnly(True)
        self.iou_widget.setPlaceholderText(iou_value)
        self.iou_widget.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        self.iou_widget.setToolTip(
            '실제 값과 예측 값이 얼마나 겹치는 지를 따져 잘 예측했는지 평가하는 지표입니다.')

        self.learning_widget = QLineEdit()
        self.learning_widget.setReadOnly(True)
        self.learning_widget.setPlaceholderText(learn_value)
        self.learning_widget.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        self.learning_widget.setToolTip('한 번의 학습으로 얼마만큼 학습해야 할지를 의미합니다.')

        self.batch_widget = QLineEdit()
        self.batch_widget.setReadOnly(True)
        self.batch_widget.setPlaceholderText(batch_value)
        self.batch_widget.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        self.batch_widget.setToolTip(
            '전체 학습 데이터셋에서 몇 개의 데이터를 한 번에 학습할 것인지를 의미합니다.')

        space_widget = QLabel("\n")  # 빈 공간 만드는 위젯

        resultBox = QFormLayout()
        resultBox.addRow(space_widget)
        resultBox.addRow("Loss Rate ", self.loss_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("IoU ", self.iou_widget)
        resultBox.addRow(space_widget)

        #iou스코어는 학습부분? 모델부분? 결과부분?
        resultBox2 = QFormLayout()
        resultBox2.addRow("Epoch ", self.epoch_widget)
        resultBox2.addRow(space_widget)
        resultBox2.addRow("Learning Rate ", self.learning_widget)
        resultBox2.addRow(space_widget)
        resultBox2.addRow("Batch Size ", self.batch_widget)
        resultBox2.addRow(space_widget)

        resultBox3 = QHBoxLayout()
        btn1 = QPushButton()
        btn1.setText('원본')
        btn2 = QPushButton()
        btn2.setText('결과')
        resultBox3.addWidget(btn1)
        resultBox3.addWidget(btn2)

        groupbox_model.setLayout(resultBox)
        groupbox_learn.setLayout(resultBox2)
        groupbox_image.setLayout(resultBox3)

        result_layout.addWidget(label10)
        result_layout.addWidget(self.cb)

        result_layout.addWidget(QLabel("\n"))
        result_layout.addWidget(groupbox_model)
        result_layout.addWidget(groupbox_learn)
        result_layout.addWidget(label3)
        result_layout.addWidget(groupbox_image)

        self.setLayout(result_layout)
        self.show()

        # 가로
        hbox = QHBoxLayout()
        hbox.addLayout(listBox)
        # 비율
        hbox.setStretchFactor(listBox, 2)
        hbox.addLayout(vbox)
        hbox.setStretchFactor(vbox, 6)
        hbox.addLayout(result_layout)
        hbox.setStretchFactor(result_layout, 2)


        # hbox.addWidget(self.lbl_img4)
        # hbox.addStretch(1)              # 결과값 넣을 곳

        self.testOpen_Di.setLayout(hbox)

        self.pixmap5 = QPixmap('./img/dark.png')
        self.lbl_img5 = QLabel(self.testOpen_Di)
        self.lbl_img5.setPixmap(self.pixmap5)
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img5)
        opacity_effect.setOpacity(0.5)
        self.lbl_img5.setGraphicsEffect(opacity_effect)
        self.pixmap5 = self.pixmap5.scaled(1200, 800)
        self.lbl_img5.setPixmap(self.pixmap5)
        self.lbl_img5.setGeometry(0, 0, 0, 0)

        # QDialog 세팅
        self.testOpen_Di.setWindowTitle('Dialog')
        self.testOpen_Di.setWindowModality(Qt.NonModal)
        # self.dialog.setGeometry(350,100,1200,800)
        self.testOpen_Di.setFixedSize(1200, 800)
        self.testOpen_Di.setStyleSheet("background-color: #0c4da2; color: white;")
        self.testOpen_Di.show()

    # 리스트 클릭시 이미지 변경 (학습부분 )
    def chkItemClicked(self):
        # print(self.listwidget.currentItem().text())
        self.pixmap = QPixmap('./test/' + self.listwidgetLearning.currentItem().text())

        self.pixmap = self.pixmap.scaled(450, 500)
        self.lbl_img.setPixmap(self.pixmap)

        self.pixmap2 = self.pixmap.scaled(200, 200)
        self.lbl_img2.setPixmap(self.pixmap2)

        s = self.listwidgetLearning.currentItem().text().split(".")
        # print(s[0])
        self.pixmap3 = QPixmap('./mask/' + s[0] + ".png")
        self.pixmap3 = self.pixmap3.scaled(200, 200)
        self.lbl_img3.setPixmap(self.pixmap3)

        self.pixmap4 = QPixmap('./mask/' + s[0] + ".png")
        self.lbl_img4.setPixmap(self.pixmap4)
        self.pixmap4 = self.pixmap4.scaled(450, 500)
        self.lbl_img4.setPixmap(self.pixmap4)
        self.lbl_img4.setGeometry(324, 10, 450, 500)

    # 리스트 클릭시 이미지 변경
    def chkItemClicked2(self):
        # print(self.listwidgetLearning.currentItem().text())
        self.pixmap = QPixmap(self.test_model_path + 'input/' + self.listwidget.currentItem().text())

        self.pixmap = self.pixmap.scaled(700, 700)
        self.lbl_img.setPixmap(self.pixmap)


        a = self.test_input_fileList[self.listwidget.currentRow()]
        b = self.test_label_fileList[self.listwidget.currentRow()]
        c = self.test_output_fileList[self.listwidget.currentRow()]

        print(a,b,c)

        ################################################################################3
        # self.pixmap = QPixmap('./test/' + self.listwidgetLearning.currentItem().text())
        #
        # self.pixmap = self.pixmap.scaled(450, 500)
        # self.lbl_img.setPixmap(self.pixmap)
        #
        # self.pixmap2 = self.pixmap.scaled(200, 200)
        # self.lbl_img2.setPixmap(self.pixmap2)
        #
        # s = self.listwidgetLearning.currentItem().text().split(".")
        # # print(s[0])
        # self.pixmap3 = QPixmap('./mask/' + s[0] + ".png")
        # self.pixmap3 = self.pixmap3.scaled(200, 200)
        # self.lbl_img3.setPixmap(self.pixmap3)
        #
        # self.pixmap4 = QPixmap('./mask/' + s[0] + ".png")
        # self.lbl_img4.setPixmap(self.pixmap4)
        # self.pixmap4 = self.pixmap4.scaled(450, 500)
        # self.lbl_img4.setPixmap(self.pixmap4)
        # self.lbl_img4.setGeometry(324, 10, 450, 500)



    def clickButton(self):
        QCoreApplication.instance().quit


    # 모델 콤보 박스 클릭시?
    def combobox_changed(self):
        text = self.cb.currentText()
        return text

    def selec_model(self):
        path = self.test_model_arr[self.cb.currentIndex()]
        res = path.split('\\')[-1]
        res1 = path.split('\\')[2]
        path1 = './checkpoint/' + res1 + '/' + res

        self.test_model_path  = './result/' + res1 + '/png/'

        epoch_value, loss_value, acc_value, iou_value, model_value, batch_value, learn_value = info_load(path1)

        self.epoch_widget.setText(str(epoch_value))
        self.loss_widget.setText(str(loss_value))
        self.iou_widget.setText(str(iou_value))
        self.learning_widget.setText(str(learn_value))
        self.batch_widget.setText(str(batch_value))

        self.test_input_fileList = []
        self.test_label_fileList = []
        self.test_output_fileList = []

        if os.path.exists(self.test_model_path + 'input'):
            input_fileList = os.listdir(self.test_model_path + 'input')
            self.listwidget.clear()
            for f in input_fileList:
                self.listwidget.addItem(f)
                self.test_input_fileList.append(f)

        if os.path.exists(self.test_model_path + 'label'):
            label_fileList = os.listdir(self.test_model_path + 'label')
            for f in label_fileList:
                self.test_label_fileList.append(f)

        if os.path.exists(self.test_model_path + 'output'):
            output_fileList = os.listdir(self.test_model_path + 'output')
            for f in output_fileList:
                self.test_output_fileList.append(f)



        else:
            self.listwidget.clear()
            self.notest = QDialog()

            label0 = QLabel('테스트가 아직 진행되지 않았습니다.', self)
            label0.setAlignment(Qt.AlignCenter)
            font0 = label0.font()
            font0.setPointSize(30)
            font0.setBold(True)
            label0.setFont(font0)

            h2box = QHBoxLayout()
            h2box.addStretch(1)
            h2box.addWidget(label0)
            h2box.addStretch(1)

            vbox = QVBoxLayout()
            vbox.addStretch(1)
            vbox.addLayout(h2box)
            vbox.addStretch(1)
            vbox.addStretch(1)

            self.notest.setLayout(vbox)

            self.notest.setWindowTitle('test')
            self.notest.setWindowModality(Qt.ApplicationModal)
            self.notest.setFixedSize(600, 400)
            self.notest.show()
            self.reset()





    def loading(self):
        self.train = QDialog()

       #train으로 전달할 입력 데이터들 (입력받은 텍스트 값들)
        learn_value = self.learn_widget.text()
        batch_value = self.batch_widget.text()
        epoch_value = self.epoch_widget.text()
        train_value = 'train'
        model_value = self.model_widget.text()

        url = 'http://localhost:6006/'
        webbrowser.open(url)

        label0 = QLabel('학습 중 ...', self)
        label0.setAlignment(Qt.AlignCenter)
        font0 = label0.font()
        font0.setPointSize(30)
        font0.setBold(True)
        label0.setFont(font0)

        h2box = QHBoxLayout()
        h2box.addStretch(1)
        h2box.addWidget(label0)
        h2box.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(h2box)
        vbox.addStretch(1)
        vbox.addStretch(1)

        self.train.setLayout(vbox)

        self.train.setWindowTitle('train')
        self.train.setWindowModality(Qt.ApplicationModal)
        self.train.setFixedSize(600, 400)
        self.train.show()
        self.reset()

        train(learn_value, batch_value, epoch_value, train_value, model_value)

        self.cancel()
        self.reset()
       

    def loading2(self):
        self.test = QDialog()
        path = self.test_model_arr[self.cb.currentIndex()]
        res = path.split('\\')[-1]
        res1 = path.split('\\')[2]
        path1 = './checkpoint/' + res1 + '/' + res
        epoch_value, loss_value, acc_value, iou_value, model_value, batch_value, learn_value, = info_load(path1)

        label0 = QLabel('테스트 중 ...', self)
        label0.setAlignment(Qt.AlignCenter)
        font0 = label0.font()
        font0.setPointSize(30)
        font0.setBold(True)
        label0.setFont(font0)

        h2box = QHBoxLayout()
        h2box.addStretch(1)
        h2box.addWidget(label0)
        h2box.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(h2box)
        vbox.addStretch(1)
        vbox.addStretch(1)

        self.test.setLayout(vbox)

        self.test.setWindowTitle('test')
        self.test.setWindowModality(Qt.ApplicationModal)
        self.test.setFixedSize(600, 400)
        self.test.show()
        self.reset()

        train(learn_value, batch_value, epoch_value, 'test', model_value, path)

        self.cancel2()
        self.reset()
        

    def cancel(self):
        self.train.hide()
        
    def cancel2(self):
        self.test.hide()


    def cancel_pre(self):
        self.pretreatmentOpen.hide()

    def reset(self):
        loop = QEventLoop()
        QTimer.singleShot(100, loop.quit)  # msec
        loop.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()

    sys.exit(app.exec_())
