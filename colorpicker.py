from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QTextEdit, QPushButton, QSlider
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
from pyqt_color_picker import ColorPickerWidget
import sys
import qdarktheme
import configparser
import MagicHome
import threading


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
        self.__initUi()

    def __initUi(self):
        button2 = QPushButton("    Fade    ", self)
        button3 = QPushButton("    Pulse    ", self)
        buttonOnOff.setText("Off")
        buttonOnOff.clicked.connect(MainClass.onOffButton)
        button2.clicked.connect(MainClass.fadeEffect)
        button3.clicked.connect(MainClass.pulseEffect)
        # button2.clicked.connect(MainClass.changeColor)

        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.valueChanged.connect(MainClass.brightlight)
        slider.setRange(0, 255)

        lay = QVBoxLayout()
        layH = QHBoxLayout()
        layH.addWidget(button2)
        layH.addWidget(button3)
        lay.addStretch(1)
        lay.addWidget(buttonOnOff)
        lay.addLayout(layH)
        lay.addWidget(te)

        if type == "RGB":
            lay.addWidget(colorPicker)
        if type == "White":
            slider.setValue(int(bright))
            lay.addWidget(slider)


        mainWidget = QWidget()
        mainWidget.setLayout(lay)
        self.setCentralWidget(mainWidget)

    def closeEvent(self, e):
        MainClass.rgbFade.stop()
        MainClass.rgbPulse.stop()


class MainClass:

    MagicHome.ip = conf()
    magicHome = MagicHome.Controller()
    stBtn = True

    def __init__(self):
        print("Test main class")
        self.__connectToHost()

    def textWidget(self):
        te.setPlainText("RED: " + str(colorPicker.getCurrentColor().getRgb()[0]) +
        "\nGREEN: " + str(colorPicker.getCurrentColor().getRgb()[1])
        + "\nBLUE: "+ str(colorPicker.getCurrentColor().getRgb()[2]) +
        "\n" + ip)
        self.__changeColor()

    def __connectToHost(self):
        try:
            print("connected")
            MainClass.magicHome.turn_on()
        except :
            print ("Wrong server")


    def onOffButton(self):
        if MainClass.stBtn:
            buttonOnOff.setText("On")
            MainClass.magicHome.turn_off()
            MainClass.stBtn = False
        else:
            buttonOnOff.setText("Off")
            MainClass.magicHome.turn_on()
            MainClass.stBtn = True


    def __changeColor(self):
        MainClass.magicHome.stopRgbFade()
        MainClass.magicHome.stopRgbPulse()
        MainClass.magicHome.changeColor(int(colorPicker.getCurrentColor().getRgb()[0]),
        int(colorPicker.getCurrentColor().getRgb()[1]),
        int(colorPicker.getCurrentColor().getRgb()[2]))

    def brightlight(value):
        MainClass.magicHome.changeColor(int(value), 0, 0)

    def fadeEffect(self):
        rgbFade = threading.Thread(name='rgbfade', target=MainClass.magicHome.rgbfade)
        rgbFade.start()

    def pulseEffect(self):
        rgbPulse = threading.Thread(name='rgbpulse', target=MainClass.magicHome.rgbPulse)
        rgbPulse.start()


if __name__ == "__main__":
    conf()
    main = MainClass()
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    colorPicker = ColorPickerWidget(color=QColor(R, G, B), orientation='vertical')
    colorPicker.colorChanged.connect(main.textWidget)
    buttonOnOff = QPushButton()
    te = QTextEdit()
    ex = Window()
    ex.setWindowTitle("Picker.")
    ex.show()
    sys.exit(app.exec_())
