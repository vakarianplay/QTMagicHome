import sys
import argparse
import configparser
import MagicHome

def conf():
    global ip
    global type
    config = configparser.ConfigParser()
    config.read("settings.ini")
    ip = (config["Settings"]["IP"])
    type = (config["Settings"]["Type"])
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
        print (args.colorArg)
        # self.__connectToHost()

    def __connectToHost(self):
        try:
            print("connected")
            MainClass.magicHome.turn_on()
            MainClass.magicHome.changeColor(int(args.colorArg[0]), int(args.colorArg[1]), int(args.colorArg[2]))
        except :
            print ("Wrong server")

    def statusParce(self):
        stByte = str(MainClass.magicHome.get_status().split()[0]).split('\\x')
#         print (stByte)
        return stByte


if __name__ == "__main__":
    conf()
    args = Argument()
    main = MainClass()
    # sys.exit(app.exec_())
