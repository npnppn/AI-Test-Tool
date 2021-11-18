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
        pretreatmentButton = QPushButton('  전처리  ')
        pretreatmentButton.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        pretreatmentButton.setToolTip(
            'datasets의 이미지를 변환시킵니다.')

        learningButton = QPushButton(' 학습 ')
        learningButton.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        learningButton.setToolTip(
            '모델을 학습시킵니다.')

        testButton = QPushButton(' Test ')
        testButton.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        testButton.setToolTip(
            '학습된 모델을 평가합니다.')

        testComButton = QPushButton(' 모델 비교 ')
        testComButton.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
        testComButton.setToolTip(
            '서로 다른 모델을 비교합니다.')

        # 글씨체 파트
        pretreatment_font = pretreatmentButton.font()
        pretreatment_font.setPointSize(35)
        pretreatmentButton.setFont(pretreatment_font)
        pretreatmentButton.setMaximumHeight(500)

        learning_font = learningButton.font()
        learning_font.setPointSize(35)
        learningButton.setFont(learning_font)
        learningButton.setMaximumHeight(500)

        test_font = testButton.font()
        test_font.setPointSize(35)
        testButton.setFont(test_font)
        testButton.setMaximumHeight(500)

        testcom_font = testComButton.font()
        testcom_font.setPointSize(35)
        testComButton.setFont(testcom_font)
        testComButton.setMaximumHeight(500)

        # 버튼 이벤트
        pretreatmentButton.clicked.connect(self.pretreatmentOpen)
        testButton.clicked.connect(self.testOpen)
        QApplication.processEvents()
        learningButton.clicked.connect(self.learningOpen)
        QApplication.processEvents()
        testComButton.clicked.connect(self.test_Compare)
        QApplication.processEvents()

        space_widget = QLabel("\n")  # 빈 공간 만드는 위젯
        title = QLabel()
        title_image = QPixmap('./img/samsung.jpg')
        title_image = title_image.scaled(230,110)
        title.setPixmap(title_image)
        title.setAlignment(Qt.AlignCenter)


        # 박스 레이아웃
        h2box = QVBoxLayout()
        h2box.addStretch(1)
        h2box.addWidget(title)
        #h2box.addWidget(space_widget)
        #h2box.addWidget(space_widget)
        h2box.addWidget(pretreatmentButton)
        h2box.addWidget(space_widget)
        h2box.addWidget(learningButton)
        h2box.addWidget(space_widget)
        h2box.addWidget(testButton)
        h2box.addWidget(space_widget)
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

        self.setWindowTitle('AI 도우미')
        self.setFixedSize(800, 600)
        self.center()
        self.setStyleSheet("background-color: #0c4da2; color: white;")
        self.show()

    # 메인페이지 중앙 위치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def pre_dataset_alert(self):
        self.noimage = QDialog()

        label0 = QLabel('datasets 폴더를 확인해주세요.', self)
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

        self.noimage.setLayout(vbox)

        self.noimage.setWindowTitle('train')
        self.noimage.setWindowModality(Qt.ApplicationModal)
        self.noimage.setFixedSize(600, 400)
        self.noimage.show()
        self.reset()

    # 데이터 전처리
    def pretreatmentOpen(self):
        path1 = './datasets/Imgs/'
        path2 = './datasets/labels/'

        if not os.path.exists(path1):
            return self.pre_dataset_alert()
        if not os.path.exists(path2):
            return self.pre_dataset_alert()

        if len(os.listdir(path1)) == 0:
            return self.pre_dataset_alert()
        if len(os.listdir(path2)) == 0:
            return self.pre_dataset_alert()

        if len(os.listdir(path1)) != len(os.listdir(path2)):
            return self.pre_dataset_alert()

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
        # imgs 폴더 맨 처음 이미지 불러오기 (그래야 첫 화면에서 그림이 나오니까!)
        file_list = os.listdir('datasets/Imgs')
        learning_list = []
        for i in file_list:
            learning_list.append(i)
        first_image_path = r"./datasets/Imgs/" + learning_list[0]

        # 중간에 큰 그림 나타내는 부분
        self.pixmap = QPixmap(first_image_path)
        self.lbl_img = QLabel()
        self.lbl_img.setPixmap(self.pixmap)
        self.pixmap = self.pixmap.scaled(450, 500)
        self.lbl_img.setPixmap(self.pixmap)

        self.lbl_img2 = QLabel()
        self.lbl_img2.setPixmap(self.pixmap)
        self.pixmap2 = self.pixmap.scaled(200, 200)
        self.lbl_img2.setPixmap(self.pixmap2)

        # 마스킹 맨 처음 이미지 보여주기 (그래야 화면에 바로 나오니까)
        mask_list = os.listdir('datasets/labels')
        self.msk_list = []
        for i in mask_list:
            self.msk_list.append(i)
        first_msk_path = r"./datasets/labels/" + self.msk_list[0]

        # 마스킹 사진
        self.pixmap3 = QPixmap(first_msk_path)
        self.lbl_img3 = QLabel()
        self.lbl_img3.setPixmap(self.pixmap3)
        self.pixmap3 = self.pixmap3.scaled(200, 200)
        self.lbl_img3.setPixmap(self.pixmap3)

        # 투명도 주는 부분(겹치게 하기)
        # self.pixmap4 = QPixmap(first_msk_path)
        # self.lbl_img4 = QLabel(self.learning)
        # self.lbl_img4.setPixmap(self.pixmap4)
        # opacity_effect = QGraphicsOpacityEffect(self.lbl_img4)
        # opacity_effect.setOpacity(0.5)
        # self.lbl_img4.setGraphicsEffect(opacity_effect)
        # self.pixmap4 = self.pixmap4.scaled(450, 500)
        # self.lbl_img4.setPixmap(self.pixmap4)
        # self.lbl_img4.setAlignment(Qt.AlignCenter)
        # self.lbl_img4.setGeometry(324, 10, 450, 500)

        # 이미지 리스트 불러오기
        path = './datasets/Imgs'
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

        # 맨 초기상태
        self.pixmap4 = QPixmap(first_msk_path)
        self.lbl_img4 = QLabel(self.learning)
        self.lbl_img4.setPixmap(self.pixmap4)
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img4)
        opacity_effect.setOpacity(0.2)
        self.lbl_img4.setGraphicsEffect(opacity_effect)
        self.pixmap4 = self.pixmap4.scaled(450, 500)
        self.lbl_img4.setPixmap(self.pixmap4)
        self.lbl_img4.setAlignment(Qt.AlignCenter)
        self.lbl_img4.setGeometry(324, 10, 450, 500)
        # self.pixmap5 = QPixmap('./img/dark.png')
        # self.lbl_img5 = QLabel(self.learning)
        # self.lbl_img5.setPixmap(self.pixmap5)
        # #opacity_effect = QGraphicsOpacityEffect(self.lbl_img5)
        # #opacity_effect.setOpacity(0.5)
        # #self.lbl_img5.setGraphicsEffect(opacity_effect)
        # self.pixmap5 = self.pixmap5.scaled(1200, 800)
        # self.lbl_img5.setPixmap(self.pixmap5)
        # self.lbl_img5.setGeometry(0, 0, 0, 0)

        # self.loading = QDialog()

        # QDialog 세팅
        self.learning.setWindowTitle('Learning')
        self.learning.setWindowModality(Qt.NonModal)
        self.learning.setFixedSize(1200, 800)
        self.learning.setStyleSheet("background-color: #0c4da2; color: white;")
        self.learning.show()

    # 테스트 페이지
    def testOpen(self):
        self.testOpen_Di = QDialog()
        # 맨 처음 이미지 불러오기
        self.pixmap11 = QPixmap('./img/test.png')
        self.lbl_img11 = QLabel()
        self.lbl_img11.setPixmap(self.pixmap11)
        self.pixmap11 = self.pixmap11.scaled(700, 700)

        self.pixmap22 = QPixmap('./img/test.png')
        self.lbl_img22 = QLabel()
        self.lbl_img22.setPixmap(self.pixmap22)
        self.pixmap22 = self.pixmap22.scaled(700, 700)
        self.lbl_img22.setPixmap(self.pixmap22)

        self.pixmap33 = QPixmap('./img/test.png')
        self.lbl_img33 = QLabel()
        self.lbl_img33.setPixmap(self.pixmap33)
        self.pixmap33 = self.pixmap33.scaled(700, 700)
        self.lbl_img33.setPixmap(self.pixmap33)

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

        # 버튼들
        startTest = QPushButton('Test')
        test_font = startTest.font()
        test_font.setPointSize(20)
        startTest.setFont(test_font)
        startTest.setMaximumHeight(200)

        logCheck = QPushButton('로그 확인')
        check_font = logCheck.font()
        check_font.setPointSize(20)
        logCheck.setFont(check_font)
        logCheck.setMaximumHeight(200)

        # 버튼 기능
        startTest.clicked.connect(self.loading2)
        logCheck.clicked.connect(self.open_log)

        # 이미지 박스
        imgBox = QHBoxLayout()
        imgBox.addWidget(self.lbl_img11)
        imgBox.addWidget(self.lbl_img22)
        imgBox.addWidget(self.lbl_img33)

        # 중간
        vbox = QVBoxLayout()
        # vbox.addWidget(self.lbl_img)
        vbox.addLayout(imgBox)


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
        listBox.addWidget(label0)
        listBox.addWidget(self.listwidget)

        # 결과값 화면 보여주는 공간
        epoch_value, loss_value, acc_value, iou_value, model_value, batch_value, learn_value = '', '', '', '', '', '', ''

        result_layout = QVBoxLayout()

        groupbox_model = QGroupBox("모델 정보")
        groupbox_model.setAlignment(5)

        groupbox_learn = QGroupBox("학습 정보")
        groupbox_learn.setAlignment(5)

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

        # iou스코어는 학습부분? 모델부분? 결과부분?
        resultBox2 = QFormLayout()
        resultBox2.addRow("Epoch ", self.epoch_widget)
        resultBox2.addRow(space_widget)
        resultBox2.addRow("Learning Rate ", self.learning_widget)
        resultBox2.addRow(space_widget)
        resultBox2.addRow("Batch Size ", self.batch_widget)
        resultBox2.addRow(space_widget)

        groupbox_model.setLayout(resultBox)
        groupbox_learn.setLayout(resultBox2)


        result_layout.addWidget(label10)
        result_layout.addWidget(self.cb)

        result_layout.addWidget(QLabel("\n"))
        result_layout.addWidget(groupbox_model)
        result_layout.addWidget(groupbox_learn)
        result_layout.addWidget(label3)
        result_layout.addWidget(startTest)
        result_layout.addWidget(logCheck)

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

        self.pixmap55 = QPixmap('./img/dark.png')
        self.lbl_img55 = QLabel(self.testOpen_Di)
        self.lbl_img55.setPixmap(self.pixmap55)
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img55)
        opacity_effect.setOpacity(0.5)
        self.lbl_img55.setGraphicsEffect(opacity_effect)
        self.pixmap55 = self.pixmap55.scaled(1200, 800)
        self.lbl_img55.setPixmap(self.pixmap55)
        self.lbl_img55.setGeometry(0, 0, 0, 0)

        # QDialog 세팅
        self.testOpen_Di.setWindowTitle('Test')
        self.testOpen_Di.setWindowModality(Qt.NonModal)
        # self.dialog.setGeometry(350,100,1200,800)
        self.testOpen_Di.setFixedSize(1200, 800)
        self.testOpen_Di.setStyleSheet("background-color: #0c4da2; color: white;")
        self.testOpen_Di.show()

    def open_log(self):
        if self.cb.currentIndex() == 0:
            return
        path = self.test_model_arr[self.cb.currentIndex()]
        res = path.split('\\')[2]
        path1 = './log/' + res
        print(res)
        print(path1)
        os.system("start cmd /c tensorboard --logdir={}".format(path1))

        url = 'http://localhost:6006/'
        webbrowser.open(url)

    # 리스트 클릭시 이미지 변경 (학습부분 )
    def chkItemClicked(self):
        # print(self.listwidget.currentItem().text())
        self.pixmap = QPixmap('./datasets/Imgs/' + self.listwidgetLearning.currentItem().text())

        self.pixmap = self.pixmap.scaled(450, 500)
        self.lbl_img.setPixmap(self.pixmap)

        self.pixmap2 = self.pixmap.scaled(200, 200)
        self.lbl_img2.setPixmap(self.pixmap2)

        s = self.listwidgetLearning.currentItem().text().split(".")
        # print(s[0])
        self.pixmap3 = QPixmap('./datasets/labels/' + self.msk_list[self.listwidgetLearning.currentRow()])
        self.pixmap3 = self.pixmap3.scaled(200, 200)
        self.lbl_img3.setPixmap(self.pixmap3)

        self.pixmap4 = self.pixmap3
        self.lbl_img4.setPixmap(self.pixmap4)
        self.pixmap4 = self.pixmap4.scaled(450, 500)
        self.lbl_img4.setPixmap(self.pixmap4)
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img4)
        opacity_effect.setOpacity(0.5)
        self.lbl_img4.setGraphicsEffect(opacity_effect)

        self.lbl_img4.setGeometry(324, 10, 450, 500)

    # 리스트 클릭시 이미지 변경 (테스트)
    def chkItemClicked2(self):
        # print(self.listwidgetLearning.currentItem().text())
        self.pixmap11 = QPixmap(self.test_model_path + 'input/' + self.listwidget.currentItem().text())

        self.pixmap11 = self.pixmap11.scaled(700, 700)
        self.lbl_img11.setPixmap(self.pixmap11)

        a = self.test_input_fileList[self.listwidget.currentRow()]
        b = self.test_label_fileList[self.listwidget.currentRow()]
        c = self.test_output_fileList[self.listwidget.currentRow()]

        # 원본
        self.pixmap11 = QPixmap(self.test_model_path + 'input/' + a)
        self.pixmap11 = self.pixmap11.scaled(700, 700)
        self.lbl_img11.setPixmap(self.pixmap11)
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img11)
        opacity_effect.setOpacity(0.9)
        self.lbl_img11.setGraphicsEffect(opacity_effect)
        self.lbl_img11.setPixmap(self.pixmap11)

        # 라벨
        # print(self.test_model_path + 'label/' + b)
        self.pixmap22 = QPixmap(self.test_model_path + 'label/' + b)
        self.pixmap22 = self.pixmap22.scaled(700, 700)
        self.lbl_img22.setPixmap(self.pixmap22)
        self.lbl_img22.setStyleSheet('color: red; background: red')


        # 아웃풋
        # print(self.test_model_path + 'output/' + c)
        self.pixmap33 = QPixmap(self.test_model_path + 'output/' + c)
        self.pixmap33 = self.pixmap33.scaled(700, 700)
        self.lbl_img33.setPixmap(self.pixmap33)

        self.lbl_img11.setAlignment(Qt.AlignCenter)
        self.lbl_img22.setAlignment(Qt.AlignCenter)
        self.lbl_img33.setAlignment(Qt.AlignCenter)
        self.lbl_img11.setGeometry(324, 10, 700, 700)
        self.lbl_img22.setGeometry(324, 10, 700, 700)
        self.lbl_img33.setGeometry(324, 10, 700, 700)

        #검은색 부분
        self.pixmap55 = QPixmap(self.test_model_path + 'label/' + b)
        self.pixmap55 = self.pixmap55.scaled(700, 700)
        self.lbl_img55.setPixmap(self.pixmap55)

    def chkItemClicked3(self):
        # print(self.listwidgetLearning.currentItem().text())
        self.pixmap111 = QPixmap(self.compare_model_path + 'input/' + self.compare_listwidget.currentItem().text())
        self.pixmap111 = self.pixmap111.scaled(700, 700)
        self.lbl_img111.setPixmap(self.pixmap111)

        a = self.compare_input_fileList[self.compare_listwidget.currentRow()]
        b = self.compare_label_fileList[self.compare_listwidget.currentRow()]
        c = self.compare_output1_fileList[self.compare_listwidget.currentRow()]
        d = self.compare_output2_fileList[self.compare_listwidget.currentRow()]

        # 원본
        self.pixmap111 = QPixmap(self.compare_model_path + 'input/' + a)
        self.pixmap111 = self.pixmap111.scaled(700, 700)
        self.lbl_img111.setPixmap(self.pixmap111)

        # 라벨
        # print(self.test_model_path + 'label/' + b)
        self.pixmap222 = QPixmap(self.compare_model_path + 'label/' + b)
        self.pixmap222 = self.pixmap222.scaled(700, 700)
        self.lbl_img222.setPixmap(self.pixmap222)

        # 아웃풋1
        # print(self.test_model_path + 'output/' + c)
        self.pixmap333 = QPixmap(self.compare_model_path + 'output/' + c)
        self.pixmap333 = self.pixmap333.scaled(700, 700)
        self.lbl_img333.setPixmap(self.pixmap333)

        # 아웃풋2
        # print(self.test_model_path + 'output/' + d)
        self.pixmap444 = QPixmap(self.compare_model_path + 'output/' + d)
        self.pixmap444 = self.pixmap444.scaled(700, 700)
        self.lbl_img444.setPixmap(self.pixmap444)

        self.lbl_img111.setAlignment(Qt.AlignCenter)
        self.lbl_img222.setAlignment(Qt.AlignCenter)
        self.lbl_img333.setAlignment(Qt.AlignCenter)
        self.lbl_img444.setAlignment(Qt.AlignCenter)
        self.lbl_img111.setGeometry(324, 10, 700, 700)
        self.lbl_img222.setGeometry(324, 10, 700, 700)
        self.lbl_img333.setGeometry(324, 10, 700, 700)
        self.lbl_img444.setGeometry(324, 10, 700, 700)

        #검은색 부분
        self.pixmap555 = QPixmap(self.compare_model_path + 'label/' + b)
        self.pixmap555 = self.pixmap555.scaled(700, 700)
        self.lbl_img555.setPixmap(self.pixmap555)

    def clickButton(self):
        QCoreApplication.instance().quit

    # 모델 콤보 박스 클릭시?
    def combobox_changed(self):
        text = self.cb.currentText()
        return text

    def compare_combobox_changed1(self):
        text = self.compare_cb1.currentText()
        return text

    def compare_combobox_changed2(self):
        text = self.compare_cb2.currentText()
        return text

    def selec_model(self):
        if self.cb.currentIndex() == 0:
            return

        path = self.test_model_arr[self.cb.currentIndex()]
        res = path.split('\\')[-1]
        res1 = path.split('\\')[2]
        path1 = './checkpoint/' + res1 + '/' + res
        test_model_path_res1 = os.path.basename(path).replace(".pth", "")
        self.test_model_path = './result/' + test_model_path_res1 + '/png/'
        #print(self.test_model_path)
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

    def compare_selec_model1(self):
        if self.compare_cb1.currentIndex() == 0:
            return

        path1 = self.test_model_arr[self.compare_cb1.currentIndex()]
        res = path1.split('\\')[-1]
        res1 = path1.split('\\')[2]
        path1 = './checkpoint/' + res1 + '/' + res
        test_model_path_res1 = os.path.basename(path1).replace(".pth", "")
        epoch_value, loss_value, acc_value, iou_value, model_value, batch_value, learn_value = info_load(path1)
        self.loss_widget1.setText(str(loss_value))
        self.iou_widget1.setText(str(iou_value))

        if self.compare_cb2.currentIndex() == 0:
            return
        path2 = self.test_model_arr[self.compare_cb2.currentIndex()]
        res = path2.split('\\')[-1]
        res1 = path2.split('\\')[2]
        path2 = './checkpoint/' + res1 + '/' + res
        test_model_path_res2 = os.path.basename(path2).replace(".pth", "")
        self.compare_model_path = './compare/' + test_model_path_res1 + '&' + test_model_path_res2 + '/png/'

        self.compare_input_fileList = []
        self.compare_label_fileList = []
        self.compare_output1_fileList = []
        self.compare_output2_fileList = []

        if os.path.exists(self.compare_model_path + 'input'):
            input_fileList = os.listdir(self.compare_model_path + 'input')
            self.compare_listwidget.clear()
            for f in input_fileList:
                self.compare_listwidget.addItem(f)
                self.compare_input_fileList.append(f)

        if os.path.exists(self.compare_model_path + 'label'):
            label_fileList = os.listdir(self.compare_model_path + 'label')
            for f in label_fileList:
                self.compare_label_fileList.append(f)

        if os.path.exists(self.compare_model_path + 'output1'):
            output_fileList = os.listdir(self.compare_model_path + 'output1')
            for f in output_fileList:
                self.compare_output1_fileList.append(f)

        if os.path.exists(self.compare_model_path + 'output2'):
            output_fileList = os.listdir(self.compare_model_path + 'output2')
            for f in output_fileList:
                self.compare_output2_fileList.append(f)

        else:
            self.compare_listwidget.clear()
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



    def compare_selec_model2(self):
        if self.compare_cb2.currentIndex() == 0:
            return

        path2 = self.test_model_arr[self.compare_cb2.currentIndex()]
        res = path2.split('\\')[-1]
        res1 = path2.split('\\')[2]
        path2 = './checkpoint/' + res1 + '/' + res
        test_model_path_res2 = os.path.basename(path2).replace(".pth", "")
        epoch_value, loss_value, acc_value, iou_value, model_value, batch_value, learn_value = info_load(path2)
        self.loss_widget2.setText(str(loss_value))
        self.iou_widget2.setText(str(iou_value))

        if self.compare_cb2.currentIndex() == 0:
            return

        path1 = self.test_model_arr[self.compare_cb1.currentIndex()]
        res = path1.split('\\')[-1]
        res1 = path1.split('\\')[2]
        path1 = './checkpoint/' + res1 + '/' + res
        test_model_path_res1 = os.path.basename(path1).replace(".pth", "")
        self.compare_model_path = './compare/' + test_model_path_res1 + '&' + test_model_path_res2 + '/png/'
        print(self.compare_model_path)

        self.compare_input_fileList = []
        self.compare_label_fileList = []
        self.compare_output1_fileList = []
        self.compare_output2_fileList = []

        if os.path.exists(self.compare_model_path + 'input'):
            input_fileList = os.listdir(self.compare_model_path + 'input')
            self.compare_listwidget.clear()
            for f in input_fileList:
                self.compare_listwidget.addItem(f)
                self.compare_input_fileList.append(f)

        if os.path.exists(self.compare_model_path + 'label'):
            label_fileList = os.listdir(self.compare_model_path + 'label')
            for f in label_fileList:
                self.compare_label_fileList.append(f)

        if os.path.exists(self.compare_model_path + 'output1'):
            output_fileList = os.listdir(self.compare_model_path + 'output1')
            for f in output_fileList:
                self.compare_output1_fileList.append(f)

        if os.path.exists(self.compare_model_path + 'output2'):
            output_fileList = os.listdir(self.compare_model_path + 'output2')
            for f in output_fileList:
                self.compare_output2_fileList.append(f)

        else:
            self.compare_listwidget.clear()
            self.notest = QDialog()

            label0 = QLabel('테스트가 아직 진행 X.', self)
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


    def dataset_alert(self):
        self.nodatasets = QDialog()

        label0 = QLabel('전처리를 먼저 진행해 주세요.', self)
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

        self.nodatasets.setLayout(vbox)

        self.nodatasets.setWindowTitle('train')
        self.nodatasets.setWindowModality(Qt.ApplicationModal)
        self.nodatasets.setFixedSize(600, 400)
        self.nodatasets.show()
        self.reset()

    def train_alert(self):
        self.novalue = QDialog()

        label0 = QLabel('모든 값을 입력해주세요.', self)
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

        self.novalue.setLayout(vbox)

        self.novalue.setWindowTitle('train')
        self.novalue.setWindowModality(Qt.ApplicationModal)
        self.novalue.setFixedSize(600, 400)
        self.novalue.show()
        self.reset()

    def loading(self):
        path = './datasets/train/'
        if not os.path.exists(path):
            return self.dataset_alert()
        if len(os.listdir(path)) == 0:
            return self.dataset_alert()

        # train으로 전달할 입력 데이터들 (입력받은 텍스트 값들)
        learn_value = self.learn_widget.text()
        batch_value = self.batch_widget.text()
        epoch_value = self.epoch_widget.text()
        train_value = 'train'
        model_value = self.model_widget.text()

        if learn_value == '' or batch_value == '' or epoch_value == '' or model_value == '':
            return self.train_alert()

        self.train = QDialog()
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
        epoch_value, loss_value, acc_value, iou_value, model_value, batch_value, learn_value, = info_load(path)

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

    def loading3(self):
        self.compare_test = QDialog()
        path1 = self.test_model_arr[self.compare_cb1.currentIndex()]
        res = path1.split('\\')[-1]
        res1 = path1.split('\\')[2]
        path1 = './checkpoint/' + res1 + '/' + res

        path2 = self.test_model_arr[self.compare_cb2.currentIndex()]
        res = path2.split('\\')[-1]
        res1 = path2.split('\\')[2]
        path2 = './checkpoint/' + res1 + '/' + res

        # ################################
        # path = self.test_model_arr[self.cb.currentIndex()]
        # res = path.split('\\')[-1]
        # res1 = path.split('\\')[2]
        # path1 = './checkpoint/' + res1 + '/' + res

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

        self.compare_test.setLayout(vbox)

        self.compare_test.setWindowTitle('compare')
        self.compare_test.setWindowModality(Qt.ApplicationModal)
        self.compare_test.setFixedSize(600, 400)
        self.compare_test.show()
        self.reset()

        # compare batch_size,mode='compare',model1 = 해당 모델 경로, model2 = 해당 모델 경로
        train(learn_value, batch_value, epoch_value, 'compare', model_value, path1, path2)

        self.cancel3()
        self.reset()

    # 데이터 전처리
    def test_Compare(self):
        if not os.path.exists('./compare'):
            os.makedirs('./compare')

        self.testCompare = QDialog()
        # 맨 처음 이미지 불러오기
        self.pixmap111 = QPixmap('./img/compare.jpg')
        self.lbl_img111 = QLabel()
        self.lbl_img111.setPixmap(self.pixmap111)
        self.pixmap111 = self.pixmap111.scaled(700, 700)
        self.lbl_img111.setPixmap(self.pixmap111)

        self.pixmap222 = QPixmap('./img/compare.jpg')
        self.lbl_img222 = QLabel()
        self.lbl_img222.setPixmap(self.pixmap222)
        self.pixmap222 = self.pixmap222.scaled(700, 700)
        self.lbl_img222.setPixmap(self.pixmap222)

        self.pixmap333 = QPixmap('./img/compare.jpg')
        self.lbl_img333 = QLabel()
        self.lbl_img333.setPixmap(self.pixmap333)
        self.pixmap333 = self.pixmap333.scaled(700, 700)
        self.lbl_img333.setPixmap(self.pixmap333)

        self.pixmap444 = QPixmap('./img/compare.jpg')
        self.lbl_img444 = QLabel()
        self.lbl_img444.setPixmap(self.pixmap444)
        self.pixmap444 = self.pixmap444.scaled(700, 700)
        self.lbl_img444.setPixmap(self.pixmap444)

        self.lbl_img111.setGeometry(324, 10, 450, 500)
        self.lbl_img222.setGeometry(324, 10, 450, 500)
        self.lbl_img333.setGeometry(324, 10, 450, 500)
        self.lbl_img444.setGeometry(324, 10, 450, 500)

        # QListWidget 추가
        self.compare_listwidget = QListWidget(self)
        self.compare_listwidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # 리스트 클릭 이벤트
        self.compare_listwidget.itemClicked.connect(self.chkItemClicked3)

        # 아웃풋 이미지 주소
        self.compare_model_path = ''

        # 폰트 및 글자
        label0 = QLabel('이미지 선택', self)
        label0.setAlignment(Qt.AlignCenter)
        font0 = label0.font()
        font0.setPointSize(20)
        font0.setBold(True)

        label10 = QLabel('\n' + '첫 번째 모델 선택', self)
        label10.setAlignment(Qt.AlignCenter)
        font10 = label10.font()
        font10.setPointSize(20)
        font10.setBold(True)
        label0.setFont(font0)

        label11 = QLabel('\n' + '두 번째 모델 선택', self)
        label11.setAlignment(Qt.AlignCenter)
        font11 = label11.font()
        font11.setPointSize(20)
        font11.setBold(True)
        label11.setFont(font11)

        label3 = QLabel('------------', self)
        label3.setAlignment(Qt.AlignCenter)
        font3 = label3.font()
        font3.setPointSize(20)
        font3.setBold(True)
        label3.setFont(font3)
        label10.setFont(font10)

        # 버튼들
        startTest = QPushButton('모델 비교')
        # startTest.setStyleSheet("""QPushButton {
        #                                    color: white;
        #                                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.857143, y2:0.857955,
        #                                    stop:0 rgba(10, 242, 251, 255), stop:1 rgba(224, 6, 159, 255));
        #                                    border-radius: 20px;
        #                                    }""")
        test_font = startTest.font()
        test_font.setPointSize(30)
        startTest.setFont(test_font)
        startTest.setMaximumHeight(200)

        buttonbox = QHBoxLayout()
        buttonbox.addWidget(startTest)

        # 버튼 기능
        startTest.clicked.connect(self.loading3)

        # 이미지 박스
        imgBox = QHBoxLayout()
        imgBox.addWidget(self.lbl_img111)

        # 중간
        vbox = QVBoxLayout()
        # vbox.addWidget(self.lbl_img)
        vbox.addLayout(imgBox)
        vbox.addLayout(buttonbox)

        # 모델 선택
        self.compare_cb1 = QComboBox()
        self.compare_cb1.addItem("ㅡㅡㅡㅡ모델을 선택하세요ㅡㅡㅡㅡ")
        self.compare_cb1.setPlaceholderText("---모델을 선택하세요---")
        self.compare_cb1.setCurrentIndex(0)

        # 모델들 하위 경로 가져오기
        targetPattern = r"./" + "*/**/*.pth"
        cbList = glob.glob(targetPattern)
        self.test_model_arr = ['a.a']
        for f in cbList:
            self.test_model_arr.append(f)
            file = os.path.basename(f)
            self.compare_cb1.addItem(file)

        self.compare_cb1.move(50, 50)
        self.compare_cb1.currentTextChanged.connect(self.compare_combobox_changed1 and self.compare_selec_model1)

        # 좌측 (리스트)
        listBox = QVBoxLayout()
        # btn = QPushButton('뒤로')
        # btn.clicked.connect(self.clickButton)
        # listBox.addWidget(btn)
        listBox.addWidget(label0)
        listBox.addWidget(self.compare_listwidget)

        # 모델 선택
        self.compare_cb2 = QComboBox()
        self.compare_cb2.addItem("ㅡㅡㅡㅡ모델을 선택하세요ㅡㅡㅡㅡ")
        self.compare_cb2.setPlaceholderText("---모델을 선택하세요---")
        self.compare_cb2.setCurrentIndex(0)

        # 모델들 하위 경로 가져오기
        targetPattern2 = r"./" + "*/**/*.pth"
        cbList2 = glob.glob(targetPattern2)
        self.test_model_arr2 = ['a.a']
        for f in cbList2:
            self.test_model_arr2.append(f)
            file = os.path.basename(f)
            self.compare_cb2.addItem(file)

        self.compare_cb2.move(50, 50)
        self.compare_cb2.currentTextChanged.connect(self.compare_combobox_changed2 and self.compare_selec_model2)

        # 결과값 화면 보여주는 공간
        epoch_value, loss_value, acc_value, iou_value, model_value, batch_value, learn_value = '', '', '', '', '', '', ''

        result_layout = QVBoxLayout()

        groupbox_model = QGroupBox("첫 번째 모델 정보")
        groupbox_model.setAlignment(5)
        groupbox_model2 = QGroupBox("두 번째 모델 정보")
        groupbox_model2.setAlignment(5)

        # 첫 번째 모델 데이터들
        self.loss_widget1 = QLineEdit()
        self.loss_widget1.setReadOnly(True)
        self.loss_widget1.setPlaceholderText(loss_value)
        self.loss_widget1.setStyleSheet("""QToolTip { 
                                   background-color: black; 
                                   color: white; 
                                   border: black solid 1px
                                   }""")
        self.loss_widget1.setToolTip('정답과 예측한 값 사이의 오차를 의미합니다.')
        self.iou_widget1 = QLineEdit()
        self.iou_widget1.setReadOnly(True)
        self.iou_widget1.setPlaceholderText(iou_value)
        self.iou_widget1.setStyleSheet("""QToolTip { 
                                   background-color: black; 
                                   color: white; 
                                   border: black solid 1px
                                   }""")
        self.iou_widget1.setToolTip(
            '실제 값과 예측 값이 얼마나 겹치는 지를 따져 잘 예측했는지 평가하는 지표입니다.')

        # 두 번째 모델 데이터들
        self.loss_widget2 = QLineEdit()
        self.loss_widget2.setReadOnly(True)
        self.loss_widget2.setPlaceholderText(loss_value)
        self.loss_widget2.setStyleSheet("""QToolTip { 
                                   background-color: black; 
                                   color: white; 
                                   border: black solid 1px
                                   }""")
        self.loss_widget2.setToolTip('정답과 예측한 값 사이의 오차를 의미합니다.')

        self.iou_widget2 = QLineEdit()
        self.iou_widget2.setReadOnly(True)
        self.iou_widget2.setPlaceholderText(iou_value)
        self.iou_widget2.setStyleSheet("""QToolTip { 
                                   background-color: black; 
                                   color: white; 
                                   border: black solid 1px
                                   }""")
        self.iou_widget2.setToolTip(
            '실제 값과 예측 값이 얼마나 겹치는 지를 따져 잘 예측했는지 평가하는 지표입니다.')

        space_widget = QLabel("\n")  # 빈 공간 만드는 위젯

        resultBox = QFormLayout()
        resultBox.addRow(space_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("Loss Rate ", self.loss_widget1)
        resultBox.addRow(space_widget)
        resultBox.addRow("IoU ", self.iou_widget1)
        resultBox.addRow(space_widget)

        resultBox2 = QFormLayout()
        resultBox2.addRow(space_widget)
        resultBox2.addRow("Loss Rate ", self.loss_widget2)
        resultBox2.addRow(space_widget)
        resultBox2.addRow("IoU ", self.iou_widget2)
        resultBox2.addRow(space_widget)

        groupbox_model.setLayout(resultBox)
        groupbox_model2.setLayout(resultBox2)

        result_layout.addWidget(label10)
        result_layout.addWidget(self.compare_cb1)
        result_layout.addWidget(QLabel("\n"))
        result_layout.addWidget(groupbox_model)

        result_layout.addWidget(label11)
        result_layout.addWidget(self.compare_cb2)
        result_layout.addWidget(QLabel("\n"))
        result_layout.addWidget(groupbox_model2)

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

        self.testCompare.setLayout(hbox)

        self.pixmap555 = QPixmap('./img/dark.png')
        self.lbl_img555 = QLabel(self.testCompare)
        self.lbl_img555.setPixmap(self.pixmap555)
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img555)
        opacity_effect.setOpacity(0.5)
        self.lbl_img555.setGraphicsEffect(opacity_effect)
        self.pixmap555 = self.pixmap555.scaled(1200, 800)
        self.lbl_img555.setPixmap(self.pixmap555)
        self.lbl_img555.setGeometry(0, 0, 0, 0)

        # QDialog 세팅
        self.testCompare.setWindowTitle('TestCompare')
        self.testCompare.setWindowModality(Qt.NonModal)
        # self.dialog.setGeometry(350,100,1200,800)
        self.testCompare.setFixedSize(1200, 800)
        self.testCompare.setStyleSheet("background-color: #0c4da2; color: white;")
        self.testCompare.show()

    def cancel(self):
        self.train.hide()

    def cancel2(self):
        self.test.hide()

    def cancel3(self):
        self.compare_test.hide()

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
