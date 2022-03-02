
import cv2
import matplotlib.pyplot as plt
import sys
import os
import cameraGUI
import timeit
from pathlib import Path
from YOLO import *
from PyQt5 import QtCore, QtGui, QtWidgets
path=os.path.dirname(__file__)

class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main, parent=None):
        ######GUI formatting######
        Main.setObjectName("Main")
        Main.resize(1076, 761)
        Main.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)
        Main.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint)
        #MainGrid
        self.gridMain = QtWidgets.QGridLayout(Main)
        self.gridMain.setObjectName("gridMain")

        #sizePolicy
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
           
        #frame
        self.frame = QtWidgets.QFrame(Main)
        self.frame.setGeometry(QtCore.QRect(10, 220, 191, 311))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(1)
        self.frame.setMidLineWidth(1)
        self.frame.setObjectName("frame")
        self.gridMain.addWidget(self.frame,0,0,1,1)
        

        #frameGrid
        self.gridFrame= QtWidgets.QGridLayout(self.frame)
        self.gridFrame.setObjectName("gridFrame")

        #frame in Grid
        self.frameGrid1 = QtWidgets.QFrame(self.frame)
        self.frameGrid2 = QtWidgets.QFrame(self.frame)

        self.gridFrame.addWidget(self.frameGrid1,0,0,1,1)
        self.gridFrame.addWidget(self.frameGrid2,5,1,1,1)
        
        #frame elements
        self.btn_Capture = QtWidgets.QPushButton(self.frame)
        self.btn_Capture.setGeometry(QtCore.QRect(30, 20, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_Capture.setFont(font)
        self.btn_Capture.setObjectName("btn_Capture")
        self.gridFrame.addWidget(self.btn_Capture,1,0,1,2)
        self.btn_Capture.setSizePolicy(sizePolicy)
        
        self.btn_Save = QtWidgets.QPushButton(self.frame)
        self.btn_Save.setGeometry(QtCore.QRect(30, 160, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_Save.setFont(font)
        self.btn_Save.setObjectName("btn_Save")
        self.gridFrame.addWidget(self.btn_Save,3,0,1,2)
        self.btn_Save.setSizePolicy(sizePolicy)
        
        self.btn_Reset = QtWidgets.QPushButton(self.frame)
        self.btn_Reset.setGeometry(QtCore.QRect(30, 230, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_Reset.setFont(font)
        self.btn_Reset.setObjectName("btn_Reset")
        self.gridFrame.addWidget(self.btn_Reset,4,0,1,2)
        self.btn_Reset.setSizePolicy(sizePolicy)

        
        self.btn_File = QtWidgets.QPushButton(self.frame)
        self.btn_File.setGeometry(QtCore.QRect(30, 90, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_File.setFont(font)
        self.btn_File.setObjectName("btn_File")
        self.gridFrame.addWidget(self.btn_File,2,0,1,2)
        self.btn_File.setSizePolicy(sizePolicy)
    
        #Frame2
        self.frame2 = QtWidgets.QFrame(Main)
        self.frame2.setGeometry(QtCore.QRect(230, 20, 821, 721))
        self.frame2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame2.setLineWidth(1)
        self.frame2.setMidLineWidth(1)
        self.frame2.setObjectName("frame2")
        self.gridMain.addWidget(self.frame2,0,1,1,5)

        #frame2 grid
        self.gridFrame2= QtWidgets.QGridLayout(self.frame2)
        self.gridFrame2.setObjectName("gridFrame2")

        #frame in Grid2
        self.frame2Grid1 = QtWidgets.QFrame(self.frame2)
        self.frame2Grid2 = QtWidgets.QFrame(self.frame2)
        self.frame2Grid3 = QtWidgets.QFrame(self.frame2)

        self.gridFrame2.addWidget(self.frame2Grid1,0,2,1,1)
        self.gridFrame2.addWidget(self.frame2Grid2,1,2,1,1)
        self.gridFrame2.addWidget(self.frame2Grid3,0,3,1,1)

        
        #frame2 elements
        self.view_Input = QtWidgets.QGraphicsView(self.frame2)
        self.view_Input.setGeometry(QtCore.QRect(20, 170, 381, 521))
        self.view_Input.setObjectName("view_Input")
        self.gridFrame2.addWidget(self.view_Input,2,0,8,2)
        
        
        self.view_Output = QtWidgets.QGraphicsView(self.frame2)
        self.view_Output.setGeometry(QtCore.QRect(420, 170, 381, 521))
        self.view_Output.setObjectName("view_Output")
        self.gridFrame2.addWidget(self.view_Output,2,2,8,2)
        
        self.labelCobb = QtWidgets.QLabel(self.frame2)
        self.labelCobb.setGeometry(QtCore.QRect(30, 20, 291, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.labelCobb.setFont(font)
        self.labelCobb.setObjectName("labelCobb")
        self.gridFrame2.addWidget(self.labelCobb,0,0,1,2)
        
        self.labelClass = QtWidgets.QLabel(self.frame2)
        self.labelClass.setGeometry(QtCore.QRect(30, 90, 361, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.labelClass.setFont(font)
        self.labelClass.setObjectName("labelClass")
        self.gridFrame2.addWidget(self.labelClass,1,0,1,2)
        
        
        self.labelInput = QtWidgets.QLabel(self.frame2)
        self.labelInput.setGeometry(QtCore.QRect(20, 170, 381, 521))
        self.labelInput.setScaledContents(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.labelInput.setFont(font)
        self.labelInput.setObjectName("labelInput")
        self.labelInput.setAlignment(QtCore.Qt.AlignCenter)
        self.gridFrame2.addWidget(self.labelInput,2,0,8,2)
      
        
        self.labelOutput = QtWidgets.QLabel(self.frame2)
        self.labelOutput.setGeometry(QtCore.QRect(420, 170, 381, 521))
        self.labelOutput.setScaledContents(True)
        self.labelOutput.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.labelOutput.setFont(font)
        self.labelOutput.setObjectName("labelOutput")
        self.gridFrame2.addWidget(self.labelOutput,2,2,8,2)
        
        self.btn_Calculate = QtWidgets.QPushButton(self.frame2)
        self.btn_Calculate.setGeometry(QtCore.QRect(640, 70, 161, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_Calculate.setFont(font)
        self.btn_Calculate.setObjectName("btn_Calculate")
        self.gridFrame2.addWidget(self.btn_Calculate,1,3,1,1)
        self.btn_Calculate.setSizePolicy(sizePolicy)
        
        self.frame2.raise_()
        self.frame.raise_()
        self.image =" "
        self.imagePath  = ""
        self.cobbAngle = ""
        self.classification = ""
        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)
        ######GUI formatting######

        
        self.btn_File.clicked.connect(self.on_btn_File_clicked)
        self.btn_Calculate.clicked.connect(self.on_btn_Calculate_clicked)
        self.btn_Reset.clicked.connect(self.on_btn_Reset_clicked)
        self.btn_Save.clicked.connect(self.on_btn_Save_clicked)
        self.btn_Capture.clicked.connect(self.on_btn_Capture_clicked)
    def truncate(self,n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "Scoliosis Detection"))
        self.btn_Capture.setText(_translate("Main", "Capture"))
        self.btn_Save.setText(_translate("Main", "Save"))
        self.btn_Reset.setText(_translate("Main", "Reset"))
        self.btn_File.setText(_translate("Main", "File"))
        self.labelCobb.setText(_translate("Main", "Cobb angle: Value"))
        self.labelClass.setText(_translate("Main", "Classification: Value"))
        self.labelInput.setText(_translate("Main", "Input Image"))
        self.labelOutput.setText(_translate("Main", "Output Image"))
        self.btn_Calculate.setText(_translate("Main", "Calculate"))

    def on_btn_Capture_clicked(self):
        try:
         self.capture = QtWidgets.QDialog()
         self.camera = cameraGUI.Ui_Camera_GUI(self.image)
         self.camera.setupUi(self.capture)
         self.dialog = self.capture
         self.dialog.showMaximized()
        except Exception:
         traceback.print_exc()
            
        
    def on_btn_File_clicked(self):
        plt.close(None)
        imagePath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
           path,"Image files (*.jpg *.png)")
        if imagePath != ('',''):
         self.image = cv2.imread(imagePath[0])
         self.imagePath = imagePath[0]
         height, width, channel = self.image.shape
         bytesPerLine = 3 * width
         self.image2 = QtGui.QImage(self.image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
         imagePixmap = QtGui.QPixmap.fromImage(self.image2)
         imagePixmap = imagePixmap.scaled(self.view_Input.width(),self.view_Input.height(),QtCore.Qt.KeepAspectRatio)
         self.labelInput.setPixmap(imagePixmap)

    def on_btn_Calculate_clicked(self):
        start = timeit.default_timer()
        plt.close(None)
        #Check if the used has chosen an image
        if self.image != " ":
            self.cobbUp, self.cobbLow, self.imgCobb, self.result = computeCobb(self.image)

            #check to see if there is no vertebrae detected in the image
            if (self.cobbUp or self.cobbLow)==None:
                print("No vertebrae detected or wrong image")
                return
            
            #gets the values of the image so that it can placed into the gui
            height, width, channel = self.imgCobb.shape
            bytesPerLine = 3 * width
            self.imgCobb2 = QtGui.QImage(self.imgCobb.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
            imagePixmap = QtGui.QPixmap.fromImage(self.imgCobb2)
            imagePixmap = imagePixmap.scaled(self.view_Input.width(),self.view_Input.height(),QtCore.Qt.KeepAspectRatio)
            self.labelOutput.setPixmap(imagePixmap)

            #check which angle is larger
            if abs(self.cobbUp) > abs(self.cobbLow):
            #convert the angle into string
                self.cobbAngle =  str(self.truncate(abs(self.cobbUp),2))
                text = "Cobb angle: " + self.cobbAngle
                self.labelCobb.setText(text)
            else:
                self.cobbAngle = str(self.truncate(abs(self.cobbLow),2))
                text = "Cobb angle: " + self.cobbAngle
                self.labelCobb.setText(text)

            
            
            #set the classification text
            self.labelClass.setText("Classification: " + self.result)
            self.classification = self.result
        stop = timeit.default_timer()

        print('Time: ', stop - start) 
            
            
    def on_btn_Reset_clicked(self):
        plt.close(None)
        self.labelInput.setText("Input Image")
        self.labelOutput.setText("Output Image")
        self.labelCobb.setText("Cobb angle: Value")
        self.labelClass.setText("Classification: Value")

    def on_btn_Save_clicked(self):
     try:
        newpath = 'SavedResults' 
        if not os.path.exists(newpath):
          os.makedirs(newpath)
        split = self.imagePath.split('/')
        imageName = split[len(split)-1]
        imageName = imageName.split('.')
        print(imageName)
        plt.savefig(newpath + '/' + imageName[0]+'.png')
        plt.close(None)
        textfile = Path('SavedResults/result.txt')
        if textfile.is_file() :
            file = open(textfile,'a')
            file.writelines(imageName[0] + '    /   ' + self.cobbAngle + '   /   ' + self.classification + '\n')
            file.close()
        else :
            file = open(textfile, 'w' )
            file.writelines("Name    /   Cobb Angle  /   Classification \n")
            file.writelines(imageName[0] + '    /   ' + self.cobbAngle + '   /   ' + self.classification + '\n')
            file.close()
        plt.show()
     except Exception:
         traceback.print_exc()
            
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    Main = QtWidgets.QDialog()
    ui = Ui_Main()
    ui.setupUi(Main)
    Main.showMaximized()
    sys.exit(app.exec_())

