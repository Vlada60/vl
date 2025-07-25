from PyQt6.QtWidgets import QFileDialog, QMainWindow, QApplication
from PyQt6.uic import loadUi
import sys
import valueLine
import google
import api
from vlTypes import Price, Quallity

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        loadUi("gui.ui", self)

        self.actionExtract_Data.triggered.connect(self.extractClickHandler)
        self.actionAdd_Files.triggered.connect(self.openFile)
        self.actionUpload_to_sheets.triggered.connect(self.uploadToSheetsClickHandler)
        self.actionLog_In.triggered.connect(self.logInClickHandler)

    quality: Quallity
    price: Price

    def logInClickHandler(self):
        api.authenticate()

    def uploadToSheetsClickHandler(self):
        self.quality.q2 = self.q2LineEdit.text()
        self.quality.q3 = self.q3LineEdit.text()
        self.quality.q4a = self.q4aLineEdit.text()
        self.quality.q4b = self.q4bLineEdit.text()
        self.quality.q5 = self.q5LineEdit.text()
        self.quality.q6a = self.q6aLineEdit.text()
        self.quality.q6b = self.q6bLineEdit.text()
        self.quality.q6c = self.q6cLineEdit.text()
        self.quality.q6d = self.q6dLineEdit.text()
        self.quality.q6e = self.q6eLineEdit.text()
        self.quality.q6f = self.q6fLineEdit.text()
        self.quality.q6g = self.q6gLineEdit.text()
        self.quality.q7a = self.q7LineEdit.text()
        self.quality.q7 = [self.q7TextEdit.toPlainText(),self.q7TextEdit_analysis.toPlainText()]
        self.quality.q8 = self.q8LineEdit.text()

        self.price.p2a=self.p2aLineEdit.text()
        self.price.p2b=self.p2bLineEdit.text()
        self.price.p3a=self.p3LineEdit.text()
        self.price.p5a[0] = self.p5aLineEdit_y1.text()
        self.price.p5a[1] = self.p5aLineEdit_y2.text()
        self.price.p5a[2] = self.p5aLineEdit_y3.text()
        self.price.p5a[3] = self.p5aLineEdit_y4.text()
        self.price.p5a[4] = self.p5aLineEdit_y5.text()
        self.price.p5b = self.p5bLineEdit.text()
        self.price.p6a[0][0] = self.p6aLineEdit_y1.text()
        self.price.p6a[0][1] = self.p6aLineEdit_y2.text()
        self.price.p6a[0][2] = self.p6aLineEdit_y3.text()
        self.price.p6a[0][3] = self.p6aLineEdit_y4.text()
        self.price.p6a[0][4] = self.p6aLineEdit_y5.text()
        self.price.p6a[1][0] = self.p6aLineEdit_y1_low.text()
        self.price.p6a[1][1] = self.p6aLineEdit_y2_low.text()
        self.price.p6a[1][2] = self.p6aLineEdit_y3_low.text()
        self.price.p6a[1][3] = self.p6aLineEdit_y4_low.text()
        self.price.p6a[1][4] = self.p6aLineEdit_y5_low.text()
        self.price.p6b[0] = self.p6bLineEdit_y1.text()
        self.price.p6b[1] = self.p6bLineEdit_y2.text()
        self.price.p6b[2] = self.p6bLineEdit_y3.text()
        self.price.p6b[3] = self.p6bLineEdit_y4.text()
        self.price.p6b[4] = self.p6bLineEdit_y5.text()
        self.price.p6c = self.p6cLineEdit.text()

        try:
            api.insert_to_sheets(self.quality, self.price)
        except google.auth.exceptions.RefreshError:
            print("You are not authentificated")

    path = []
    def openFile(self):
        file_filter = 'Pdf Files (*.pdf)'
        self.path.append(QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file',
            filter=file_filter,
            initialFilter=file_filter
        )[0]
    )

    def extractClickHandler(self):
        (self.quality, self.price) = valueLine.extract_with_path(self.path[0])

        self.q2LineEdit.setText(self.quality.q2)
        if(self.q2LineEdit.text() == "error"):
            self.q2LineEdit.setStyleSheet("border: 1px solid red; border-radius:4px");
        self.q3LineEdit.setText(self.quality.q3)
        if(self.q3LineEdit.text() == "error"):
            self.q3LineEdit.setStyleSheet("border: 1px solid red; border-radius:4px");
        self.q4aLineEdit.setText(str(self.quality.q4a))
        if(self.q4aLineEdit.text() == "-1"):
            self.q4aLineEdit.setStyleSheet("border: 1px solid red; border-radius:4px");
        self.q4bLineEdit.setText(str(self.quality.q4b))
        if(self.q4bLineEdit.text() == "-1"):
            self.q4bLineEdit.setStyleSheet("border: 1px solid red; border-radius:4px");
        self.q5LineEdit.setText(self.quality.q5)
        self.q6aLineEdit.setText(self.quality.q6a)
        self.q6bLineEdit.setText(str(self.quality.q6b))
        self.q6cLineEdit.setText(self.quality.q6c)
        self.q6dLineEdit.setText(str(self.quality.q6d))
        self.q6eLineEdit.setText(self.quality.q6e)
        self.q6fLineEdit.setText(self.quality.q6f)
        self.q6gLineEdit.setText(self.quality.q6g)
        self.q7LineEdit.setText(str(self.quality.q7a))
        self.q7TextEdit.setText(self.quality.q7[0])
        self.q7TextEdit_analysis.setText(self.quality.q7[1])
        self.q8LineEdit.setText(self.quality.q8)

        self.p2aLineEdit.setText(self.price.p2a)
        self.p2bLineEdit.setText(str(self.price.p2b))
        self.p3LineEdit.setText(self.price.p3a)
        self.p5aLineEdit_y1.setText(self.price.p5a[0])
        self.p5aLineEdit_y2.setText(self.price.p5a[1])
        self.p5aLineEdit_y3.setText(self.price.p5a[2])
        self.p5aLineEdit_y4.setText(self.price.p5a[3])
        self.p5aLineEdit_y5.setText(self.price.p5a[4])
        self.p5bLineEdit.setText(self.price.p5b)
        self.p6aLineEdit_y1.setText(self.price.p6a[0][0])
        self.p6aLineEdit_y2.setText(self.price.p6a[0][1])
        self.p6aLineEdit_y3.setText(self.price.p6a[0][2])
        self.p6aLineEdit_y4.setText(self.price.p6a[0][3])
        self.p6aLineEdit_y5.setText(self.price.p6a[0][4])
        self.p6aLineEdit_y1_low.setText(self.price.p6a[1][0])
        self.p6aLineEdit_y2_low.setText(self.price.p6a[1][1])
        self.p6aLineEdit_y3_low.setText(self.price.p6a[1][2])
        self.p6aLineEdit_y4_low.setText(self.price.p6a[1][3])
        self.p6aLineEdit_y5_low.setText(self.price.p6a[1][4])
        self.p6bLineEdit_y1.setText(self.price.p6b[0])
        self.p6bLineEdit_y2.setText(self.price.p6b[1])
        self.p6bLineEdit_y3.setText(self.price.p6b[2])
        self.p6bLineEdit_y4.setText(self.price.p6b[3])
        self.p6bLineEdit_y5.setText(self.price.p6b[4])
        self.p6cLineEdit.setText(self.price.p6c)

app = QApplication(sys.argv)
ui = MainUI()
ui.show()
app.exec()
