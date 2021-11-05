import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from PyQt5.QtGui import QIcon

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

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
        self.setGeometry(800, 800, 800, 600)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def testOpen(self):
        # qPixmapVar = QPixmap()

        path = './test'
        fileList = os.listdir(path)
        # view = QListView(self)
        # view = QListWidget(self)

        # QListWidget 추가
        self.listwidget = QListWidget(self)
        # model = QStandardItemModel()


        for f in fileList:
            self.listwidget.addItem(f)

        # for f in model:
        #     self.listwidget.insertItem(f)
        # self.listwidget.insertItem(model)
        self.listwidget.itemClicked.connect(self.chkItemClicked)

        hbox = QHBoxLayout()
        # hbox.addStretch(1)
        hbox.addWidget(self.listwidget)
        hbox.addStretch(1)

        self.dialog.setLayout(hbox)


        # QDialog 세팅
        self.dialog.setWindowTitle('Dialog')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(800,600)
        self.center()
        self.dialog.show()
        self.hide()



    def chkItemClicked(self):
        print(self.listwidget.currentItem().text())

        # 상대경로 이용
        # self.dialog.qPixmapVar.load("./"+self.listwidget.currentItem().text())
        # print(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())