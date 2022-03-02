
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import traceback
import cv2
import numpy as np
import datetime

class VideoThread(QtCore.QThread):
    change_pixmap_signal = QtCore.pyqtSignal(np.ndarray)
    
    def run(self):
        # capture from web cam
        
      try:
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,1280)
        self.cap.set(4,720)
        #self.cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS,60)#modify brightness
        while True:
            self.ret, self.frame = self.cap.read()
            
            if self.ret:
                self.change_pixmap_signal.emit(cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE))

      except Exception:
          traceback.print_exc()

    def stop(self):
        self.cap.release()

    def picture(self):
        
         newpath = 'SavedImages' 
         if not os.path.exists(newpath):
          os.makedirs(newpath)
             
         
         img_name = "Image_{}.png".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
         self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
         
         cv2.imwrite(os.path.join(newpath, img_name), self.frame)
         print("{} written!".format(img_name)) # to remove
         try:
          self.showDialog()
          self.stop()
          return 1
         except Exception:
          traceback.print_exc()
    def showDialog(self):
         msg = QtWidgets.QMessageBox()
         msg.setIcon(QtWidgets.QMessageBox.Information)

         msg.setText("Picture has been saved is SavedImages folder")
         msg.setWindowTitle("Done")
         msg.exec_()
         
         

class Ui_Camera_GUI(QtWidgets.QMainWindow):
    def __init__(self,image=""):
         super().__init__()
         self.disply_width = 1280
         self.display_height = 720
         self.image = image
        
         self.thread = VideoThread()

         self.thread.change_pixmap_signal.connect(self.update_image)
         self.thread.start()

    #@QtCore.pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.label_image.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.label_image.width(), self.label_image.height(), QtCore.Qt.KeepAspectRatio)
        return QtGui.QPixmap.fromImage(p)

    
    def setupUi(self, Camera_GUI):
        Camera_GUI.setObjectName("Camera_GUI")
        Camera_GUI.resize(862, 705)
        Camera_GUI.setEnabled(True)
        Camera_GUI.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)
        Camera_GUI.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint)

        #grid layouy
        self.gridCamera = QtWidgets.QGridLayout(Camera_GUI)
        self.gridCamera.setObjectName("gridCamera")
        
        #sizePolicy
        sizePolicy2 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)


        #buttons
        self.btn_Capture2 = QtWidgets.QPushButton(Camera_GUI)
        self.btn_Capture2.setGeometry(QtCore.QRect(30, 20, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_Capture2.setFont(font)
        self.btn_Capture2.setObjectName("btn_Capture")
        self.btn_Capture2.setStyleSheet("background-color: white;")
        self.gridCamera.addWidget(self.btn_Capture2,0,3,1,1)
        self.btn_Capture2.setSizePolicy(sizePolicy2)

        self.btn_Cancel = QtWidgets.QPushButton(Camera_GUI)
        self.btn_Cancel.setGeometry(QtCore.QRect(30, 20, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_Cancel.setFont(font)
        self.btn_Cancel.setObjectName("btn_Cancel")
        self.gridCamera.addWidget(self.btn_Cancel,1,3,1,1)
        self.btn_Cancel.setSizePolicy(sizePolicy2)
        self.btn_Cancel.setStyleSheet("background-color: white;")
        #image label for video

        self.label_image = QtWidgets.QLabel(Camera_GUI)
        self.label_image.resize(self.disply_width, self.display_height)
        self.label_image.setSizePolicy(sizePolicy2)
        self.gridCamera.addWidget(self.label_image, 0,0,2,2)
    
        self.btn_Cancel.clicked.connect(lambda: self.closeIt(Camera_GUI))
        self.btn_Capture2.clicked.connect(lambda: self.captureImage(Camera_GUI))
        self.retranslateUi(Camera_GUI)
        QtCore.QMetaObject.connectSlotsByName(Camera_GUI)

    def retranslateUi(self, Camera_GUI):
        _translate = QtCore.QCoreApplication.translate
        Camera_GUI.setStyleSheet("background-color: gray;")
        Camera_GUI.setWindowTitle(_translate("Camera_GUI", "Camera"))
        self.btn_Capture2.setText(_translate("Camera_GUI", "Capture"))
        self.btn_Cancel.setText(_translate("Camera_GUI", "Cancel"))
    def closeIt(self,Camera_GUI):
        try:
            self.thread.stop()
            Camera_GUI.close()
        except Exception:
            traceback.print_exc()

    def captureImage(self,Camera_GUI):
        self.thread.picture()
        
        Camera_GUI.close()

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    Main = QtWidgets.QDialog()
    ui = Ui_Camera_GUI()
    ui.setupUi(Main)
    Main.showMaximized()
    sys.exit(app.exec_())
