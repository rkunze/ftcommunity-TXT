# TxtStyle application
#
# Initially meant to implement a TXT Qt style. Now also includes
# additional functionality to communicate with the app launcher and
# the like

import struct, os, platform, socket
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# TXT values
INPUT_EVENT_DEVICE = "/dev/input/event1"
INPUT_EVENT_CODE = 116

INPUT_EVENT_FORMAT = 'llHHI'
INPUT_EVENT_SIZE = struct.calcsize(INPUT_EVENT_FORMAT)

STYLE_NAME = "themes/default/style.qss"

# background thread to monitor power button event device
class ButtonThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()
 
    def run(self):
        in_file = open(INPUT_EVENT_DEVICE, "rb")
        event = in_file.read(INPUT_EVENT_SIZE)
        while event:
            (tv_sec, tv_usec, type, code, value) = struct.unpack(INPUT_EVENT_FORMAT, event)
            print((type, code, value))
            if type == 1 and code == INPUT_EVENT_CODE and value == 0:
                self.emit( SIGNAL('power_button_released()'))   
            event = in_file.read(INPUT_EVENT_SIZE)
        return

def TxtSetStyle(self):
    # try to find style sheet and load it
    base = os.path.dirname(os.path.realpath(__file__)) + "/"
    if os.path.isfile(base + STYLE_NAME):
        self.setStyleSheet( "file:///" + base + STYLE_NAME)
    elif os.path.isfile("/opt/ftc/" + STYLE_NAME):
        self.setStyleSheet( "file:///" + "/opt/ftc/" + STYLE_NAME)

class TxtMenu(QMenu):
    def __init__(self, parent=None):
        super(TxtMenu, self).__init__(parent)

    def on_button_clicked(self):
        pos = self.parent().mapToGlobal(QPoint(0,0))
        self.popup(pos)

# The TXTs window title bar
class TxtTitle(QLabel):
    def __init__(self,str,parent=None):
        super(TxtTitle, self).__init__(str, parent)
        self.setObjectName("titlebar")
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.close = QPushButton(self)
        self.close.setObjectName("closebut")
        self.close.clicked.connect(parent.close)
        self.close.move(200,6)

    def addMenu(self):
        self.menubut = QPushButton(self)
        self.menubut.setObjectName("menubut")
        self.menubut.move(8,6)
        self.menu = TxtMenu(self.menubut)
        self.menubut.clicked.connect(self.menu.on_button_clicked)
        return self.menu
        
# The TXT does not use windows. Instead we just paint custom 
# toplevel windows fullscreen. This widget is closed when the 
# pwoer button is being pressed
class TxtBaseWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setFixedSize(240, 320)
        self.setObjectName("centralwidget")
        self.subdialogs = []

        # on arm (TXT) start thread to monitor power button
        if platform.machine() == "armv7l":
            self.buttonThread = ButtonThread()
            self.connect( self.buttonThread, SIGNAL("power_button_released()"), self.close )
            self.buttonThread.start()

            
        # TXT windows are always fullscreen on arm (txt itself)
        # and windowed else (e.g. on PC)
    def show(self):
        if platform.machine() == "armv7l":
            QWidget.showFullScreen(self)
        else:
            QWidget.show(self)
            
        # send a message to the launcher once the main widget has been 
        # drawn for the first time
        self.notify_launcher()

    def notify_launcher(self):
        # send a signal so launcher knows that the app
        # is up and can stop the busy animation
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server and send data
            sock.connect(("localhost", 9000))
            sock.sendall(bytes("app-running {}\n".format(os.getpid()), "UTF-8"))
        except socket.error as msg:
            print(("Unable to connect to launcher:", msg))
        finally:
            sock.close()

    def unregister(self,child):
        self.subdialogs.remove(child)

    def register(self,child):
        self.subdialogs.append(child)
        
    def close(self):
        for i in self.subdialogs: i.close()
        super(TxtBaseWidget, self).close()

class TxtWindow(TxtBaseWidget):
    def __init__(self,str):
        TxtBaseWidget.__init__(self)

        # create a vertical layout and put all widgets inside
        self.layout = QVBoxLayout()
        self.titlebar = TxtTitle(str, self)
        self.layout.addWidget(self.titlebar)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        # add an empty widget as the centralWidget
        self.centralWidget = QWidget()
        self.layout.addWidget(self.centralWidget)

        self.setLayout(self.layout)        

    def setCentralWidget(self,w):
        # remove the old central widget and add a new one
        self.centralWidget.deleteLater()
        self.centralWidget = w
        self.layout.addWidget(self.centralWidget)

    def addMenu(self):
        return self.titlebar.addMenu()

class TxtDialog(QDialog):
    def __init__(self,title,parent):
        QDialog.__init__(self,parent)

        # for some odd reason the childern are not registered
        # as child windows on the txt
        self.parent = parent
        parent.register(self)
        
        # the setFixedSize is only needed for testing on a desktop pc
        # the centralwidget name makes sure the themes background 
        # gradient is being used
        self.setParent(parent)
        self.setFixedSize(240, 320)
        self.setObjectName("centralwidget")

        # create a vertical layout and put all widgets inside
        self.layout = QVBoxLayout()
        self.layout.addWidget(TxtTitle(title, self))
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        # add an empty widget as the centralWidget
        self.centralWidget = QWidget()
        self.layout.addWidget(self.centralWidget)

        self.setLayout(self.layout)        

    def setCentralWidget(self,w):
        # remove the old central widget and add a new one
        self.centralWidget.deleteLater()
        self.centralWidget = w
        self.layout.addWidget(self.centralWidget)

    def close(self):
        self.parent.unregister(self)
        super(TxtDialog, self).close()
        
        # TXT windows are always fullscreen
    def exec_(self):
        QDialog.showFullScreen(self)
        QDialog.exec_(self)

class TxtApplication(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)
        TxtSetStyle(self)

