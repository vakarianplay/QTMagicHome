from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QTextEdit, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen
from pyqt_color_picker import ColorPickerWidget
import sys
import qdarktheme
import configparser
import MagicHome


def conf():
    global ip
    global type
    global R
    global G
    global B
    config = configparser.ConfigParser()
    config.read("settings.ini")
    ip = (config["Settings"]["IP"])
    type = (config["Settings"]["Type"])
    StartColor = (config["Settings"]["StartColor"]).replace(",", "").split()
    R = int(StartColor[0])
    G = int(StartColor[1])
    B = int(StartColor[2])
    return ip


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

    MagicHome.ip = conf()
    magicHome = MagicHome.Controller()

    def __init__(self):
        print("Test main class")
        self.connectToHost()

    def textWidget(self):
        te.setPlainText("RED: " + str(colorPicker.getCurrentColor().getRgb()[0]) +
        "\nGREEN: " + str(colorPicker.getCurrentColor().getRgb()[1])
        + "\nBLUE: "+ str(colorPicker.getCurrentColor().getRgb()[2]) +
        "\n" + ip)
        # print((colorPicker.getCurrentColor().getRgb()[0]))
        # print((colorPicker.getCurrentColor().getRgb()[1]))
        # print((colorPicker.getCurrentColor().getRgb()[2]))

    def connectToHost(self):
        try:
            magicHome.turn_off()
        except :
            print ("No connection")


if __name__ == "__main__":
    conf()
    main = MainClass()
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    colorPicker = ColorPickerWidget(color=QColor(R, G, B), orientation='vertical')
    colorPicker.colorChanged.connect(main.textWidget)
    te = QTextEdit()
    ex = Window()
    ex.setWindowTitle("Picker.")
    ex.show()
    sys.exit(app.exec_())
