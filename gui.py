from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUi
import sys
import valueLine

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        loadUi("gui.ui", self)

        self.actionExtract_Data.triggered.connect(self.extractClickHandler)

    def extractClickHandler(self):
        (quality, price) = valueLine.extract_with_path("./tests/blank.pdf")
        print("test")

        self.q2LineEdit.setText(quality.q2)
        if(self.q2LineEdit.text() == "error"):
            self.q2LineEdit.setStyleSheet("border: 1px solid red; border-radius:4px");
        self.q3LineEdit.setText(quality.q3)
        if(self.q3LineEdit.text() == "error"):
            self.q3LineEdit.setStyleSheet("border: 1px solid red; border-radius:4px");
        self.q4aLineEdit.setText(str(quality.q4a))
        if(self.q4aLineEdit.text() == "-1"):
            self.q4aLineEdit.setStyleSheet("border: 1px solid red; border-radius:4px");
        self.q4bLineEdit.setText(str(quality.q4b))
        if(self.q4bLineEdit.text() == "-1"):
            self.q4bLineEdit.setStyleSheet("border: 1px solid red; border-radius:4px");
        self.q5LineEdit.setText(quality.q5)
        self.q6aLineEdit.setText(quality.q6a)
        self.q6bLineEdit.setText(str(quality.q6b))
        self.q6cLineEdit.setText(quality.q6c)
        self.q6dLineEdit.setText(str(quality.q6d))
        self.q6eLineEdit.setText(quality.q6e)
        self.q6fLineEdit.setText(quality.q6f)
        self.q6gLineEdit.setText(quality.q6g)
        self.q7LineEdit.setText(str(quality.q7a))
        self.q8LineEdit.setText(quality.q8)

        self.p2aLineEdit.setText(price.p2a)
        self.p2bLineEdit.setText(str(price.p2b))
        self.p3LineEdit.setText(price.p3a)
        self.p5aLineEdit_y1.setText(price.p5a[0])
        self.p5aLineEdit_y2.setText(price.p5a[1])
        self.p5aLineEdit_y3.setText(price.p5a[2])
        self.p5aLineEdit_y4.setText(price.p5a[3])
        self.p5aLineEdit_y5.setText(price.p5a[4])
        self.p5bLineEdit.setText(price.p5b)
        self.p6aLineEdit_y1.setText(price.p6a[0][0])
        self.p6aLineEdit_y2.setText(price.p6a[0][1])
        self.p6aLineEdit_y3.setText(price.p6a[0][2])
        self.p6aLineEdit_y4.setText(price.p6a[0][3])
        self.p6aLineEdit_y5.setText(price.p6a[0][4])
        self.p6aLineEdit_y1_low.setText(price.p6a[1][0])
        self.p6aLineEdit_y2_low.setText(price.p6a[1][1])
        self.p6aLineEdit_y3_low.setText(price.p6a[1][2])
        self.p6aLineEdit_y4_low.setText(price.p6a[1][3])
        self.p6aLineEdit_y5_low.setText(price.p6a[1][4])
        self.p6bLineEdit_y1.setText(price.p6b[0])
        self.p6bLineEdit_y2.setText(price.p6b[1])
        self.p6bLineEdit_y3.setText(price.p6b[2])
        self.p6bLineEdit_y4.setText(price.p6b[3])
        self.p6bLineEdit_y5.setText(price.p6b[4])
        self.p6cLineEdit.setText(price.p6c)

app = QApplication(sys.argv)
ui = MainUI()
ui.show()
app.exec()
