import os,sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QGridLayout, QLayout, QLineEdit,QTextEdit,QMenu,QSystemTrayIcon,QFormLayout
from PyQt5.QtWidgets import QLabel,QPushButton,QFileDialog,QSlider,QProgressBar,QMessageBox,QCheckBox
from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QMainWindow
from PyQt5.QtGui import QIcon,QPixmap,QImage
from PyQt5.QtCore import QSize, QTimer,Qt
from consistency_xml import consistency_check
class Second_Win(QWidget):
    def __init__(self,path=None):
        super().__init__()
        self.path = path
        self.validate_message = ""
        self.setWindowTitle("Functions")
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setFixedSize(600, 400)
        self.btn1 = QPushButton("Validate")
        self.btn2 = QPushButton("Fix Error")
        self.btn3 = QPushButton("Format XML")
        self.btn4 = QPushButton("Covert to JSON")
        self.btn5 = QPushButton("Compress")
        self.btn6 = QPushButton("Decompress")

        self.btn1.clicked.connect(self.validate)
        self.btn2.clicked.connect(self.fix_error)
        self.btn3.clicked.connect(self.format)
        self.btn4.clicked.connect(self.to_json)
        self.btn5.clicked.connect(self.compress)
        self.btn6.clicked.connect(self.decompress)

        self.ppar1 = QProgressBar()
        self.ppar2 = QProgressBar()
        self.ppar3 = QProgressBar()
        self.ppar4 = QProgressBar()
        self.ppar5 = QProgressBar()
        self.ppar6 = QProgressBar()



        self.btn1.setParent(self)
        self.btn2.setParent(self)
        self.btn3.setParent(self)
        self.btn4.setParent(self)
        self.btn5.setParent(self)
        self.btn6.setParent(self)




        self.btn1.move(100,50)
        self.btn2.move(100,100)
        self.btn3.move(100,150)
        self.btn4.move(100,200)
        self.btn5.move(100,250)
        self.btn6.move(100,300)


        self.ppar1.setParent(self)
        self.ppar2.setParent(self)
        self.ppar3.setParent(self)
        self.ppar4.setParent(self)
        self.ppar5.setParent(self)
        self.ppar6.setParent(self)

        self.ppar1.move(300,50)
        self.ppar2.move(300,100)
        self.ppar3.move(300,150)
        self.ppar4.move(300,200)
        self.ppar5.move(300,250)
        self.ppar6.move(300,300)
        
        self.ppar1.setMinimumWidth(300)
        self.ppar2.setMinimumWidth(300)
        self.ppar3.setMinimumWidth(300)
        self.ppar4.setMinimumWidth(300)
        self.ppar5.setMinimumWidth(300)
        self.ppar6.setMinimumWidth(300)

        self.btn2.setEnabled(False)
        
    def validate(self):
        path = self.path.text()
        mess,d = consistency_check(path)
        self.validate_message = mess
        if len(mess)!=0:
            self.btn2.setEnabled(True)
            self.ppar1.setValue(80)
            mess_b = QMessageBox()
            mess_b.setText("\n".join(mess))
            mess_b.exec()
    
    def fix_error(self):
        #fix_err(self.validate_message)
        pass
    def convert_to_json(self):
        pass
    def format(self):
        pass
    def to_json(self):
        pass
    def compress(self):
        pass
    def decompress(self):
        pass

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XML Parser")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setFixedSize(600, 400)
        #self.load_layout = QHBoxLayout()
        #self.main_layout.setSpacing(50)
        self.xml_path = ""
        self.path_qlbl = QLabel("")
        self.btn1 = QPushButton("Load")
        self.btn2 = QPushButton("Exit")
        self.btn3 = QPushButton("Next")
        self.path_label = QLineEdit("")
        #self.path_label.setEnabled(False)
        self.path_label.setReadOnly(True)
        self.functions_window = Second_Win(path= self.path_qlbl)


        self.btn1.clicked.connect(self.get_xml_path)
        self.btn2.clicked.connect(sys.exit)
        self.btn3.clicked.connect(self.functions_window.show)
        self.btn1.setParent(self)
        self.btn2.setParent(self)
        self.btn3.setParent(self)
        self.path_label.setParent(self)
        self.btn1.move(500,100)
        self.btn2.move(500,350)
        self.btn3.move(400,350)
        self.path_label.move(10,100)
        self.path_label.setMinimumWidth(450)
        #self.main_layout.addWidget(self.btn1)
        #self.main_layout.addWidget(self.path_label)

        #self.main_layout.addWidget(self.btn2)
        #self.main_layout.addWidget(self.btn3)

        #self.setLayout(self.main_layout)
    def get_xml_path(self):
        self.xml_path = QFileDialog.getOpenFileName(self,"OpenFile")[0]
        self.path_qlbl.setText(self.xml_path)
        self.path_label.setText(self.xml_path.split("/")[-1])
    
if __name__=="__main__":

    myApp = QApplication(sys.argv)
    window = Window()
    window.show()
    #window.resize(600,400)
    #window.repaint()
    
    myApp.exec_()
    sys.exit(0)