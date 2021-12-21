import sys
from PyQt5.QtWidgets import QApplication, QLineEdit,QTextEdit
from PyQt5.QtWidgets import QLabel,QPushButton,QFileDialog,QProgressBar,QMessageBox,QSizePolicy
from PyQt5.QtWidgets import QWidget,QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from XML import XML
from consistency_xml import consistency_check
#build command pyinstaller XML_Parser.py -i icon.ico
class MyMessageBox(QMessageBox):
    def __init__(self):
        QMessageBox.__init__(self)
        self.setSizeGripEnabled(True)

    def event(self, e):
        result = QMessageBox.event(self, e)

        self.setMinimumHeight(0)
        self.setMaximumHeight(16777215)
        self.setMinimumWidth(0)
        self.setMaximumWidth(16777215)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        textEdit = self.findChild(QTextEdit)
        if textEdit != None :
            textEdit.setMinimumHeight(0)
            textEdit.setMaximumHeight(16777215)
            textEdit.setMinimumWidth(0)
            textEdit.setMaximumWidth(16777215)
            textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        return result
class Second_Win(QWidget):
    def __init__(self,path=None):
        super().__init__()
        self.path_widget = path
        self.path = ""
        self.path_text = ""
        self.validate_message = ""
        self.xml_obj = None
        self.setWindowTitle("XML Parser")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setFixedSize(600, 400)
        self.btn1 = QPushButton("Validate")
        #self.btn2 = QPushButton("Fix Error")
        self.btn3 = QPushButton("Fix and Format XML")
        self.btn4 = QPushButton("Covert to JSON")
        self.btn5 = QPushButton("Compress / Decompress")
        #self.btn6 = QPushButton("Decompress")

        self.btn1.clicked.connect(self.validate)
        #self.btn2.clicked.connect(self.fix_error)
        self.btn3.clicked.connect(self.format)
        self.btn4.clicked.connect(self.to_json)
        self.btn5.clicked.connect(self.de_compress)
        #self.btn6.clicked.connect(self.decompress)

        self.ppar1 = QProgressBar()
        self.ppar2 = QProgressBar()
        self.ppar3 = QProgressBar()
        self.ppar4 = QProgressBar()
        self.ppar5 = QProgressBar()
        #self.ppar6 = QProgressBar()



        self.btn1.setParent(self)
        #self.btn2.setParent(self)
        self.btn3.setParent(self)
        self.btn4.setParent(self)
        self.btn5.setParent(self)
        #self.btn6.setParent(self)




        self.btn1.move(100,100)
        #self.btn2.move(100,100)
        self.btn3.move(100,160)
        self.btn4.move(100,220)
        self.btn5.move(100,280)
        #self.btn6.move(100,290)


        self.ppar1.setParent(self)
        #self.ppar2.setParent(self)
        self.ppar3.setParent(self)
        self.ppar4.setParent(self)
        self.ppar5.setParent(self)
        #self.ppar6.setParent(self)

        self.ppar1.move(300,100)
        #self.ppar2.move(300,100)
        self.ppar3.move(300,160)
        self.ppar4.move(300,220)
        self.ppar5.move(300,280)
        #self.ppar6.move(300,290)
        
        self.ppar1.setMinimumWidth(300)
        #self.ppar2.setMinimumWidth(300)
        self.ppar3.setMinimumWidth(300)
        self.ppar4.setMinimumWidth(300)
        self.ppar5.setMinimumWidth(300)
        #self.ppar6.setMinimumWidth(300)

        #self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)
        self.btn4.setEnabled(False)
        self.btn5.setEnabled(False)
        #self.btn6.setEnabled(False)

        
    def validate(self):
        path = self.path_widget.text()
        self.path = path
        self.xml_obj = XML(path)
        self.xml_obj.validate_()
        mess,err = consistency_check(path)
        if not isinstance(mess,str):
            mess = "\n".join(mess)
        self.validate_message = mess
        #self.xml_obj.validate_()
        if len(mess)!=0:
            #self.btn2.setEnabled(True)
            self.btn3.setEnabled(True)
            self.btn4.setEnabled(True)
            self.btn5.setEnabled(True)
            #self.btn6.setEnabled(True)
            self.ppar1.setValue(100)
            mess_b = QMessageBox()
            mess_b.setWindowIcon(QIcon('icon.ico'))
            mess_b.setText(mess)
            mess_b.setWindowTitle("Validation")
            mess_b.exec()
    
    def fix_error(self):
        #fix_err(self.validate_message)
        self.xml_obj.fix()


    def format(self):
        frm = self.xml_obj.format_xml()
        self.ppar3.setValue(100)
        mess_b = MyMessageBox()
        mess_b.setWindowIcon(QIcon('icon.ico'))
        mess_b.setText("FORMATED OUTPUT: [Show Details]")
        print(frm)
        mess_b.setDetailedText(frm)
        mess_b.setWindowTitle("Formating and Fixing")
        mess_b.exec()

    def to_json(self):
        j = self.xml_obj.to_json()
        self.ppar4.setValue(100)
        mess_b = MyMessageBox()
        mess_b.setWindowIcon(QIcon('icon.ico'))
        mess_b.setText("JSON OUTPUT: [Show Details]")
        mess_b.setDetailedText(j)
        mess_b.setWindowTitle("Convert to JSON")
        mess_b.exec()

    def de_compress(self):
        mess_b = MyMessageBox()
        mess_b.setWindowIcon(QIcon('icon.ico'))
        
        if self.path[-4:] == ".xml":
            print("Encode")
            s = self.xml_obj.encode()
            mess_b.setText("COMPRESSED OUTPUT: [Show Details]")
        elif self.path[-4:] == ".enc":
            print("Decode")
            s = self.xml_obj.decode()
            mess_b.setText("DECOMPRESSED OUTPUT: [Show Details]")
        
        mess_b.setDetailedText(s)
        mess_b.setWindowTitle("Compress / Decompress")
        self.ppar5.setValue(100)
        mess_b.exec()
     

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XML Parser Main Window")
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
        self.show_window = QTextEdit("")
        #self.path_label.setEnabled(False)
        self.path_label.setReadOnly(True)
        self.show_window.setReadOnly(True)
        self.functions_window = Second_Win(path= self.path_qlbl)


        self.btn1.clicked.connect(self.get_xml_path)
        self.btn2.clicked.connect(sys.exit)
        self.btn3.clicked.connect(self.functions_window.show)
        self.btn1.setParent(self)
        self.btn2.setParent(self)
        self.btn3.setParent(self)
        self.path_label.setParent(self)
        self.show_window.setParent(self)

        self.btn1.move(500,100)
        self.btn2.move(500,350)
        self.btn3.move(400,350)
        self.path_label.move(10,100)
        self.show_window.move(10,150)
        self.path_label.setMinimumWidth(450)
        self.show_window.setMinimumWidth(450)
        self.show_window.setMinimumHeight(150)
        #self.main_layout.addWidget(self.btn1)
        #self.main_layout.addWidget(self.path_label)

        #self.main_layout.addWidget(self.btn2)
        #self.main_layout.addWidget(self.btn3)

        #self.setLayout(self.main_layout)
    def get_xml_path(self):
        self.xml_path = QFileDialog.getOpenFileName(self,"OpenFile")[0]
        self.path_qlbl.setText(self.xml_path)
        self.path_label.setText(self.xml_path.split("/")[-1])
        with open(self.xml_path,'r') as f:
            data = f.read()
        self.show_window.setText(data)
        self.functions_window.btn3.setEnabled(False)
        self.functions_window.btn4.setEnabled(False)
        self.functions_window.btn5.setEnabled(False)
        self.functions_window.ppar1.setValue(0)
        self.functions_window.ppar3.setValue(0)
        self.functions_window.ppar4.setValue(0)
        self.functions_window.ppar5.setValue(0)
if __name__=="__main__":

    myApp = QApplication(sys.argv)
    window = Window()
    window.show()
    #window.resize(600,400)
    #window.repaint()
    
    myApp.exec_()
    sys.exit(0)