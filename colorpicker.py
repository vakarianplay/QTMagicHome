from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QTextEdit, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen
from pyqt_color_picker import ColorPickerWidget
import sys
import qdarktheme


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        button = QPushButton("    Click    ", self)
        button2 = QPushButton("    Click2    ", self)
        button3 = QPushButton("    Click3    ", self)
        # button.move(50, 50)
        button.clicked.connect(self.color)
        lay = QVBoxLayout()
        layH = QHBoxLayout()
        layH.addWidget(button2)
        layH.addWidget(button3)
        lay.addStretch(1)
        lay.addWidget(button)
        lay.addLayout(layH)
        lay.addWidget(te)
        lay.addWidget(colorPicker)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)
        self.setCentralWidget(mainWidget)


    def color(self):
        print(colorPicker.getCurrentColor().getRgb())
        # return current

class MainClass:
    def __init__(self):
        # self.test()
        print("Test main class")

    def test(self):
        te.setPlainText("RED: " + str(colorPicker.getCurrentColor().getRgb()[0]) + "\nGREEN: " + str(colorPicker.getCurrentColor().getRgb()[1])
        + "\nBLUE: "+ str(colorPicker.getCurrentColor().getRgb()[2]))
        # print((colorPicker.getCurrentColor().getRgb()[0]))
        # print((colorPicker.getCurrentColor().getRgb()[1]))
        # print((colorPicker.getCurrentColor().getRgb()[2]))

if __name__ == "__main__":
    main = MainClass()
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    colorPicker = ColorPickerWidget(color=QColor(65, 80, 100), orientation='vertical')
    colorPicker.colorChanged.connect(main.test)
    te = QTextEdit()
    ex = Window()
    ex.setWindowTitle("Picker.")
    ex.show()
    sys.exit(app.exec_())
