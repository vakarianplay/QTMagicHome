import sys
import argparse
import configparser
import MagicHome

def conf():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    ip = (config["Settings"]["IP"])
    return ip

class Argument:
    def __init__(self):
        parser = argparse.ArgumentParser(description='MagicHome CLI')
        parser.add_argument('--color', type=str, help="Color in RGB (R,G,B)")
        args = parser.parse_args()
        self.colorArg = (args.color).split(',')

class MainClass:

    MagicHome.ip = conf()
    magicHome = MagicHome.Controller()

    def __init__(self):
        if int(args.colorArg[0]) == 0 and int(args.colorArg[1]) == 0 and int(args.colorArg[2]) == 0:
            self.__turnOff()
        else:
            self.__connectToHost()

    def __connectToHost(self):
        try:
            print("connected")
            MainClass.magicHome.turn_on()
            MainClass.magicHome.changeColor(int(args.colorArg[0]), int(args.colorArg[1]), int(args.colorArg[2]))
        except :
            print ("Wrong server")

    def __turnOff(self):
        MainClass.magicHome.turn_off()

    def statusParce(self):
        stByte = str(MainClass.magicHome.get_status().split()[0]).split('\\x')
#         print (stByte)
        return stByte

if __name__ == "__main__":
    conf()
    args = Argument()
    main = MainClass()
