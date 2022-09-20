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
        buttonFade = QPushButton("    Fade    ", self)
        buttonPulse = QPushButton("    Pulse    ", self)
        buttonPolice = QPushButton("    Police    ", self)
        buttonRandom = QPushButton("    Random    ", self)
        buttonOnOff.setText("Off")
        buttonOnOff.clicked.connect(MainClass.onOffButton)
        buttonFade.clicked.connect(MainClass.fadeEffect)
        buttonPulse.clicked.connect(MainClass.pulseEffect)
        buttonPolice.clicked.connect(MainClass.policeEffect)
        buttonRandom.clicked.connect(MainClass.randomEffect)

        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.valueChanged.connect(MainClass.brightlight)
        slider.setRange(0, 255)

        lay = QVBoxLayout()
        layH = QHBoxLayout()
        layH.addWidget(buttonFade)
        layH.addWidget(buttonPulse)
        layH.addWidget(buttonPolice)
        layH.addWidget(buttonRandom)
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
        MainClass.policeEf.stop()
        MainClass.randomEf.stop()


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
            # self.statusParce()
        except :
            print ("Wrong server")

    def statusParce(self):
        stByte = str(MainClass.magicHome.get_status().split()[0]).split('\\x')
#         print (stByte)
        return stByte

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

    def policeEffect(self):
        policeEf = threading.Thread(name='policeEf', target=MainClass.magicHome.police)
        policeEf.start()

    def randomEffect(self):
        randomEf = threading.Thread(name='randomEf', target=MainClass.magicHome.Random)
        randomEf.start()


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
    ex.setWindowTitle("QTMagicHome")
    ex.show()
    sys.exit(app.exec_())
