from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QTextEdit, QPushButton, QSlider
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
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
    global bright
    config = configparser.ConfigParser()
    config.read("settings.ini")
    ip = (config["Settings"]["IP"])
    type = (config["Settings"]["Type"])
    StartColor = (config["Settings"]["StartColor"]).replace(",", "").split()
    bright = (config["Settings"]["StartBright"])
    R = int(StartColor[0])
    G = int(StartColor[1])
    B = int(StartColor[2])
    return ip


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        button = QPushButton("    Батон1    ", self)
        button2 = QPushButton("    Батон2    ", self)
        button3 = QPushButton("    Батон3    ", self)
        button.clicked.connect(self.color)
        button2.clicked.connect(MainClass.connectToHost)

        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.valueChanged.connect(MainClass.brightlight)
        slider.setRange(0, 255)
        slider.setValue(int(bright))

        lay = QVBoxLayout()
        layH = QHBoxLayout()
        layH.addWidget(button2)
        layH.addWidget(button3)
        lay.addStretch(1)
        lay.addWidget(button)
        lay.addLayout(layH)
        lay.addWidget(te)

        if type == "RGB":
            lay.addWidget(colorPicker)
        if type == "White":
            lay.addWidget(slider)

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
        self.changeColor()
        # print((colorPicker.getCurrentColor().getRgb()[0]))
        # print((colorPicker.getCurrentColor().getRgb()[1]))
        # print((colorPicker.getCurrentColor().getRgb()[2]))

    def connectToHost(self):
        try:
            print("connected")
            MainClass.magicHome.get_status()
            MainClass.magicHome.turn_on()
        except :
            print ("Wrong server")

    def changeColor(self):
        MainClass.magicHome.changeColor(int(colorPicker.getCurrentColor().getRgb()[0]),
        int(colorPicker.getCurrentColor().getRgb()[1]),
        int(colorPicker.getCurrentColor().getRgb()[2]))

    def brightlight(value):
        MainClass.magicHome.changeColor(int(value), 0, 0)


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
