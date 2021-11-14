# 학습하기 페이지
import sys, os, glob
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# import webview
import webbrowser

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
        path = os.getcwd()
        os.chdir("./AI/model3/pytorch-unet-master")
        self.reset()
        os.system("python data_read.py")
        os.chdir(path)
        self.learningOpen()

    # 학습 페이지
    def learningOpen(self):

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
        btn.clicked.connect(self.clickButton)
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
        self.batch_widget = QLineEdit()
        self.epoch_widget = QLineEdit()
        self.model_widget = QLineEdit()
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
        #resultBox.addRow(space_widget)

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

        self.loading = QDialog()

        # QDialog 세팅
        self.learning.setWindowTitle('Learning')
        self.learning.setWindowModality(Qt.NonModal)
        self.learning.setFixedSize(1200, 800)
        self.hide()
        self.dialog.hide()
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
        # self.dialog = QDialog()
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
        path = './test'
        fileList = os.listdir(path)

        # QListWidget 추가
        self.listwidget = QListWidget(self)
        self.listwidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # 확장자명 제거해서 리스트에 추가
        for f in fileList:
            self.listwidget.addItem(f.split(".")[0])

        # 리스트 클릭 이벤트
        self.listwidget.itemClicked.connect(self.chkItemClicked2)

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

        #getModel = QPushButton('모델 추출')
        #testComButton = QPushButton('Test 비교')
        buttonbox = QHBoxLayout()
        buttonbox.addWidget(startTest)
        #buttonbox.addWidget(getModel)
        #buttonbox.addWidget(testComButton)

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


        # 테스트 모델 경로
        path = './AI/model3/pytorch-unet-master/checkpoint'
        fileList2 = os.listdir(path)

        # 모델 선택
        cb = QComboBox(self)
        cb.addItem("ㅡㅡㅡㅡ모델을 선택하세요ㅡㅡㅡㅡ")
        cb.setPlaceholderText("---모델을 선택하세요---")
        cb.setCurrentIndex(0)

        # 모델들 하위 경로 가져오기
        targetPattern = r"./AI/model3/pytorch-unet-master/" + "**/**/*.pth"
        cbList = glob.glob(targetPattern)
        arr = []
        for f in cbList:
            file = os.path.basename(f)
            cb.addItem(file)

        cb.move(50, 50)


        with open('./AI/model3/pytorch-unet-master/test_file_path.txt', 'w', encoding='UTF-8') as f:
            for name in fileList2:
                f.write(name + '\n')

        cb.currentTextChanged.connect(self.combobox_changed)

        # 좌측 (리스트)
        listBox = QVBoxLayout()
        btn = QPushButton('뒤로')
        btn.clicked.connect(self.clickButton)
        listBox.addWidget(btn)
        listBox.addWidget(label0)
        listBox.addWidget(self.listwidget)

        # 결과값 화면 보여주는 공간
        result_layout = QVBoxLayout()

        groupbox_model = QGroupBox("모델 정보")
        groupbox_model.setAlignment(5)

        groupbox_learn = QGroupBox("학습 정보")
        groupbox_learn.setAlignment(5)
        groupbox_image = QGroupBox("라벨/결과 비교")
        groupbox_image.setAlignment(5)

        self.epoch_widget = QLineEdit()
        self.epoch_widget.setPlaceholderText("epoch")
        self.loss_widget = QLineEdit()
        self.loss_widget.setPlaceholderText("loss")
        self.accuracy_widget = QLineEdit()
        self.accuracy_widget.setPlaceholderText("accuracy")
        self.learning_widget = QLineEdit()
        self.learning_widget.setPlaceholderText("learning")
        self.batch_widget = QLineEdit()
        self.batch_widget.setPlaceholderText("batch")
        space_widget = QLabel("\n")  # 빈 공간 만드는 위젯

        resultBox = QFormLayout()
        resultBox.addRow(space_widget)
        resultBox.addRow("Loss Rate ", self.loss_widget)
        resultBox.addRow(space_widget)
        resultBox.addRow("Accuracy ", self.accuracy_widget)
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
        result_layout.addWidget(cb)

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

        self.dialog.setLayout(hbox)

        self.pixmap5 = QPixmap('./img/dark.png')
        self.lbl_img5 = QLabel(self.dialog)
        self.lbl_img5.setPixmap(self.pixmap5)
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img5)
        opacity_effect.setOpacity(0.5)
        self.lbl_img5.setGraphicsEffect(opacity_effect)
        self.pixmap5 = self.pixmap5.scaled(1200, 800)
        self.lbl_img5.setPixmap(self.pixmap5)
        self.lbl_img5.setGeometry(0, 0, 0, 0)

        # QDialog 세팅
        self.dialog.setWindowTitle('Dialog')
        self.dialog.setWindowModality(Qt.NonModal)
        # self.dialog.setGeometry(350,100,1200,800)
        self.dialog.setFixedSize(1200, 800)
        self.hide()
        self.learning.hide()
        self.dialog.setStyleSheet("background-color: #0c4da2; color: white;")
        self.dialog.show()

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
        self.pixmap = QPixmap('./test/' + self.listwidget.currentItem().text())

        self.pixmap = self.pixmap.scaled(700, 700)
        self.lbl_img.setPixmap(self.pixmap)

    def clickButton(self):
        self.initUI()

    # 모델 콤보 박스 클릭시?
    def combobox_changed(self):
        readFile = open('./AI/model3/pytorch-unet-master/learn_input_file.txt', 'r')
        reads = readFile.readlines()
        readList = []
        for read in reads:
            readList.append(read)

        print(readList)
        self.epoch_widget.setText(readList[0])
        self.learning_widget.setText(readList[1])
        self.batch_widget.setText(readList[2])
        #print("ㅇㅇ콤보박스 이벤트")

    def loading(self):
       #train으로 전달할 입력 데이터들 (입력받은 텍스트 값들)
        learn_value = self.learn_widget.text()
        batch_value = self.batch_widget.text()
        epoch_value = self.epoch_widget.text()
        train_value = 'train'
        model_value = self.model_widget.text()

        url = 'http://localhost:6006/'
        webbrowser.open(url)

        #로딩화면 꾸미는 부분
        self.label0 = QLabel()
        label1 = QLabel('로딩 중 ...', self)
        label1.setAlignment(Qt.AlignCenter)
        font1 = label1.font()
        font1.setPointSize(30)
        font1.setBold(True)
        label1.setFont(font1)
        self.label0.setAlignment(Qt.AlignCenter)
        #print(os.getcwd())
        self.movie = QMovie('loading.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.label0.setMovie(self.movie)
        self.movie.start()
        # 윈도우 해더 숨기기
        self.setWindowFlags(Qt.FramelessWindowHint)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label0)
        vbox.addWidget(label1)

        self.loading.setLayout(vbox)
        self.loading.setWindowTitle('Loading')
        self.loading.setWindowModality(Qt.ApplicationModal)
        self.loading.setFixedSize(600, 400)
        self.loading.show()
        self.reset()

        # 경로 변경해서 ai모델 있는 경로에 txt파일로 입력받은 값들을 저장하자
        path = os.getcwd()
        os.chdir("./AI/model3/pytorch-unet-master")
        inputFile = open('learn_input_file.txt', 'w')
        inputFile.write(learn_value + '\n' + batch_value + '\n' + epoch_value  + '\n' + train_value + '\n' + model_value)
        inputFile.close()

        self.reset()
        os.system("python train.py")
        self.cancel()
        os.chdir(path)

    def loading2(self):
        # TEST
        # 로딩화면 꾸미는 부분
        self.label0 = QLabel()
        label1 = QLabel('로딩 중 ...', self)
        label1.setAlignment(Qt.AlignCenter)
        font1 = label1.font()
        font1.setPointSize(30)
        font1.setBold(True)
        label1.setFont(font1)
        self.label0.setAlignment(Qt.AlignCenter)
        print(os.getcwd())
        self.movie = QMovie('loading.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.label0.setMovie(self.movie)
        self.movie.start()
        # 윈도우 해더 숨기기
        self.setWindowFlags(Qt.FramelessWindowHint)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label0)
        vbox.addWidget(label1)

        self.loading.setLayout(vbox)
        self.loading.setWindowTitle('Loading')
        self.loading.setWindowModality(Qt.ApplicationModal)
        self.loading.setFixedSize(600, 400)
        self.loading.show()
        self.reset()
        #self.epoch_widget.setText(str(epoch))



        # 경로 변경해서 ai모델 있는 경로에 txt파일로 입력받은 값들을 저장하자
        # train으로 전달할 입력 데이터들 (입력받은 텍스트 값들)
        train_file = open('./AI/model3/pytorch-unet-master/learn_input_file.txt', 'r')
        lines = train_file.readlines()
        linesList = []
        for line in lines:
            linesList.append(line)

        #lineList에는 입력받은 데이터인 epoch_value / learn_value / batch_value / train_value / model_value 이렇게 들어가있음!
        print(linesList)
        with open('./AI/model3/pytorch-unet-master/learn_input_file.txt', 'w', encoding='UTF-8') as f:
            for name in linesList:
                if name == 'train\n':
                    f.write('test\n')
                else:
                    f.write(name)

        os.chdir("./AI/model3/pytorch-unet-master")
        print(os.getcwd())
        self.reset()
        os.system("python train.py")
        self.cancel()

    def cancel(self):
        self.loading.hide()
        opacity_effect = QGraphicsOpacityEffect(self.lbl_img5)
        opacity_effect.setOpacity(0.5)
        self.lbl_img5.setGraphicsEffect(opacity_effect)
        self.lbl_img5.setGeometry(0, 0, 0, 0)

    def cancel2(self):
        self.loading2.hide()

        opacity_effect = QGraphicsOpacityEffect(self.lbl_img5)
        opacity_effect.setOpacity(0.5)
        self.lbl_img5.setGraphicsEffect(opacity_effect)
        self.lbl_img5.setGeometry(0, 0, 0, 0)

    def reset(self):
        loop = QEventLoop()
        QTimer.singleShot(100, loop.quit)  # msec
        loop.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()

    sys.exit(app.exec_())
