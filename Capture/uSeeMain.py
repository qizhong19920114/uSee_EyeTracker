#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      ZhongQi
#
# Created:     31/10/2015
# Copyright:   (c) ZhongQi 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
from uSeeDemoUI import Ui_MainWindow
from PyQt4 import QtCore, QtGui
import cv2
import numpy as np


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

def test():
    while(1):
        _,img = c.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        #cv2.imshow('img',img)
        if cv2.waitKey(5)==27:
            break

def getFrame():
    _,img = c.read()



    height, width, byteValue = img.shape
    byteValue = byteValue * width

    cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)

    QI= QtGui.QImage(img, width, height, byteValue, QtGui.QImage.Format_RGB888)
    ui.label_EyeCam.setPixmap(QtGui.QPixmap.fromImage(QI))

if __name__ == "__main__":
    c = cv2.VideoCapture(0)

    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #ui.label_EyeCam

    getFrame()

    MainWindow.show()



sys.exit(app.exec_())

cv2.destroyAllWindows()
