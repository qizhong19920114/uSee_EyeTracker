# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uSeeDemoUI.ui'
#
# Created: Sat Oct 31 23:06:38 2015
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

import cv
import sys
from PyQt4.QtCore import QPoint, QTimer
from PyQt4.QtGui import QApplication, QImage, QPainter, QWidget


class IplQImage(QImage):
    """
    http://matthewshotton.wordpress.com/2011/03/31/python-opencv-iplimage-to-pyqt-qimage/
    A class for converting iplimages to qimages
    """

    def __init__(self,iplimage):
        # Rough-n-ready but it works dammit
        alpha = cv.CreateMat(iplimage.height,iplimage.width, cv.CV_8UC1)
        cv.Rectangle(alpha, (0, 0), (iplimage.width,iplimage.height), cv.ScalarAll(255) ,-1)
        rgba = cv.CreateMat(iplimage.height, iplimage.width, cv.CV_8UC4)
        cv.Set(rgba, (1, 2, 3, 4))
        cv.MixChannels([iplimage, alpha],[rgba], [
        (0, 0), # rgba[0] -> bgr[2]
        (1, 1), # rgba[1] -> bgr[1]
        (2, 2), # rgba[2] -> bgr[0]
        (3, 3)  # rgba[3] -> alpha[0]
        ])
        self.__imagedata = rgba.tostring()
        super(IplQImage,self).__init__(self.__imagedata, iplimage.width, iplimage.height, QImage.Format_RGB32)


class VideoWidget(QWidget):
    """ A class for rendering video coming from OpenCV """

    def __init__(self, cameraIndex,parent=None):
        QWidget.__init__(self)
        self._capture = cv.CreateCameraCapture(cameraIndex)
        # Take one frame to query height
        frame = cv.QueryFrame(self._capture)
        self.setMinimumSize(frame.width, frame.height)
        self.setMaximumSize(self.minimumSize())
        self._frame = None
        self._image = self._build_image(frame)
        # Paint every 50 ms
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.queryFrame)
        self._timer.start(50)

    def _build_image(self, frame):
        if not self._frame:
            self._frame = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, frame.nChannels)
        if frame.origin == cv.IPL_ORIGIN_TL:
            cv.Copy(frame, self._frame)
        else:
            cv.Flip(frame, self._frame, 0)
        return IplQImage(self._frame)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(QPoint(0, 0), self._image)

    def queryFrame(self):
        frame = cv.QueryFrame(self._capture)
        self._image = self._build_image(frame)
        self.update()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(938, 661)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.quickBtn_Create = QtGui.QPushButton(self.centralwidget)
        self.quickBtn_Create.setGeometry(QtCore.QRect(10, 10, 51, 71))
        self.quickBtn_Create.setObjectName(_fromUtf8("quickBtn_Create"))
        self.quickBtn_Save = QtGui.QPushButton(self.centralwidget)
        self.quickBtn_Save.setGeometry(QtCore.QRect(70, 10, 51, 71))
        self.quickBtn_Save.setObjectName(_fromUtf8("quickBtn_Save"))
        self.quickBtn_StartRecord = QtGui.QPushButton(self.centralwidget)
        self.quickBtn_StartRecord.setGeometry(QtCore.QRect(130, 10, 51, 71))
        self.quickBtn_StartRecord.setObjectName(_fromUtf8("quickBtn_StartRecord"))
        self.quickBtn_Pause = QtGui.QPushButton(self.centralwidget)
        self.quickBtn_Pause.setGeometry(QtCore.QRect(190, 10, 51, 71))
        self.quickBtn_Pause.setObjectName(_fromUtf8("quickBtn_Pause"))
        self.quickBtn_Stop = QtGui.QPushButton(self.centralwidget)
        self.quickBtn_Stop.setGeometry(QtCore.QRect(250, 10, 51, 71))
        self.quickBtn_Stop.setObjectName(_fromUtf8("quickBtn_Stop"))
        self.quickBtn_CfgCamera = QtGui.QPushButton(self.centralwidget)
        self.quickBtn_CfgCamera.setGeometry(QtCore.QRect(390, 10, 51, 71))
        self.quickBtn_CfgCamera.setObjectName(_fromUtf8("quickBtn_CfgCamera"))
        self.quickBtn_VerifyCamera = QtGui.QPushButton(self.centralwidget)
        self.quickBtn_VerifyCamera.setGeometry(QtCore.QRect(450, 10, 51, 71))
        self.quickBtn_VerifyCamera.setObjectName(_fromUtf8("quickBtn_VerifyCamera"))
        self.quick_Btn_CfgRoi = QtGui.QPushButton(self.centralwidget)
        self.quick_Btn_CfgRoi.setGeometry(QtCore.QRect(330, 10, 51, 71))
        self.quick_Btn_CfgRoi.setObjectName(_fromUtf8("quick_Btn_CfgRoi"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(293, 0, 51, 91))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 110, 241, 21))
        self.label.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label.setFrameShadow(QtGui.QFrame.Plain)
        self.label.setObjectName(_fromUtf8("label"))
        self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(10, 160, 241, 121))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 130, 61, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(70, 130, 61, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(130, 130, 61, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(190, 130, 61, 23))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(130, 320, 61, 23))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 320, 61, 23))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_7 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(190, 320, 61, 23))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 300, 241, 21))
        self.label_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_2.setFrameShadow(QtGui.QFrame.Plain)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton_8 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(70, 320, 61, 23))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.tableView = QtGui.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 340, 241, 192))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(260, 120, 451, 421))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.graphicsView = QtGui.QGraphicsView(self.tab)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 421, 301))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(0, 300, 441, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.line_2 = QtGui.QFrame(self.tab)
        self.line_2.setGeometry(QtCore.QRect(0, 310, 451, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(0, 320, 451, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.line_3 = QtGui.QFrame(self.tab)
        self.line_3.setGeometry(QtCore.QRect(0, 340, 451, 16))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.scrollArea = QtGui.QScrollArea(self.tab)
        self.scrollArea.setGeometry(QtCore.QRect(0, 350, 451, 51))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 449, 49))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalScrollBar_2 = QtGui.QScrollBar(self.scrollAreaWidgetContents)
        self.verticalScrollBar_2.setGeometry(QtCore.QRect(430, 0, 20, 51))
        self.verticalScrollBar_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar_2.setObjectName(_fromUtf8("verticalScrollBar_2"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

##        self.label_EyeCam = QtGui.QLabel(self.tab)
##        self.label_EyeCam.setGeometry(QtCore.QRect(0, 0, 441, 301))
##        self.label_EyeCam.setText(_fromUtf8(""))
##        self.label_EyeCam.setPixmap(QtGui.QPixmap(_fromUtf8("../Downloads/eyeDemo.bmp")))
##        self.label_EyeCam.setObjectName(_fromUtf8("label_EyeCam"))
        #by HJB
        self.label_EyeCam = VideoWidget(0)
        self.tab.setObjectName(_fromUtf8("tab_1"))
        self.tabWidget.addTab(self.label_EyeCam, _fromUtf8(""))

        self.tab_2 = VideoWidget(1)
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5"))
        self.tabWidget.addTab(self.tab_5, _fromUtf8(""))
        self.horizontalScrollBar = QtGui.QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(10, 260, 221, 20))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName(_fromUtf8("horizontalScrollBar"))
        self.verticalScrollBar = QtGui.QScrollBar(self.centralwidget)
        self.verticalScrollBar.setGeometry(QtCore.QRect(230, 160, 20, 101))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName(_fromUtf8("verticalScrollBar"))
        self.line_4 = QtGui.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(10, 80, 711, 16))
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.line_5 = QtGui.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(710, 0, 16, 541))
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 938, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        self.menuIP_Port = QtGui.QMenu(self.menuAbout)
        self.menuIP_Port.setObjectName(_fromUtf8("menuIP_Port"))
        self.menuData = QtGui.QMenu(self.menuAbout)
        self.menuData.setObjectName(_fromUtf8("menuData"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menu_H = QtGui.QMenu(self.menubar)
        self.menu_H.setObjectName(_fromUtf8("menu_H"))
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionImport = QtGui.QAction(MainWindow)
        self.actionImport.setObjectName(_fromUtf8("actionImport"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionSetting = QtGui.QAction(MainWindow)
        self.actionSetting.setObjectName(_fromUtf8("actionSetting"))
        self.actionRecording_mode = QtGui.QAction(MainWindow)
        self.actionRecording_mode.setObjectName(_fromUtf8("actionRecording_mode"))
        self.actionClient = QtGui.QAction(MainWindow)
        self.actionClient.setObjectName(_fromUtf8("actionClient"))
        self.actionServer = QtGui.QAction(MainWindow)
        self.actionServer.setObjectName(_fromUtf8("actionServer"))
        self.actionEye_Data = QtGui.QAction(MainWindow)
        self.actionEye_Data.setObjectName(_fromUtf8("actionEye_Data"))
        self.actionScene_Data = QtGui.QAction(MainWindow)
        self.actionScene_Data.setObjectName(_fromUtf8("actionScene_Data"))
        self.actionAudio_Data = QtGui.QAction(MainWindow)
        self.actionAudio_Data.setObjectName(_fromUtf8("actionAudio_Data"))
        self.actionSocket_out_data = QtGui.QAction(MainWindow)
        self.actionSocket_out_data.setObjectName(_fromUtf8("actionSocket_out_data"))
        self.actionPC_event = QtGui.QAction(MainWindow)
        self.actionPC_event.setObjectName(_fromUtf8("actionPC_event"))
        self.actionAbout_us = QtGui.QAction(MainWindow)
        self.actionAbout_us.setObjectName(_fromUtf8("actionAbout_us"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionClose)
        self.menuIP_Port.addAction(self.actionClient)
        self.menuIP_Port.addAction(self.actionServer)
        self.menuData.addAction(self.actionEye_Data)
        self.menuData.addAction(self.actionScene_Data)
        self.menuData.addAction(self.actionAudio_Data)
        self.menuData.addAction(self.actionSocket_out_data)
        self.menuData.addAction(self.actionPC_event)
        self.menuAbout.addAction(self.actionSetting)
        self.menuAbout.addAction(self.actionRecording_mode)
        self.menuAbout.addAction(self.menuIP_Port.menuAction())
        self.menuAbout.addAction(self.menuData.menuAction())
        self.menuHelp.addAction(self.actionAbout_us)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menu_H.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "优视眼动科技 - 数据采集工具 v2.1 : 授权给 UESEO LLC ", None))
        self.quickBtn_Create.setText(_translate("MainWindow", "新建", None))
        self.quickBtn_Save.setText(_translate("MainWindow", "保存", None))
        self.quickBtn_StartRecord.setText(_translate("MainWindow", "开始记录", None))
        self.quickBtn_Pause.setText(_translate("MainWindow", "暂停", None))
        self.quickBtn_Stop.setText(_translate("MainWindow", "停止", None))
        self.quickBtn_CfgCamera.setText(_translate("MainWindow", "标定\n"
"摄像头", None))
        self.quickBtn_VerifyCamera.setText(_translate("MainWindow", "验证\n"
"摄像头", None))
        self.quick_Btn_CfgRoi.setText(_translate("MainWindow", "设置瞳孔\n"
"区域", None))
        self.label.setText(_translate("MainWindow", "                               项目记录", None))
        self.pushButton.setText(_translate("MainWindow", "收起", None))
        self.pushButton_2.setText(_translate("MainWindow", "展开", None))
        self.pushButton_3.setText(_translate("MainWindow", "增加", None))
        self.pushButton_4.setText(_translate("MainWindow", "删除", None))
        self.pushButton_5.setText(_translate("MainWindow", "增加", None))
        self.pushButton_6.setText(_translate("MainWindow", "收起", None))
        self.pushButton_7.setText(_translate("MainWindow", "删除", None))
        self.label_2.setText(_translate("MainWindow", "                               任务定义", None))
        self.pushButton_8.setText(_translate("MainWindow", "展开", None))
        self.label_3.setText(_translate("MainWindow", "提示： 设置的瞳孔区域需要覆盖瞳孔的所有可能位置", None))
        self.label_4.setText(_translate("MainWindow", "                                                                   实时消息", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "眼睛摄像头", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "场景摄像头", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "麦克风", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "网络数据", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "键盘鼠标与软件事件", None))
        self.menuFile.setTitle(_translate("MainWindow", "文件 (E)", None))
        self.menuAbout.setTitle(_translate("MainWindow", "设置 (S)", None))
        self.menuIP_Port.setTitle(_translate("MainWindow", "IP/Port", None))
        self.menuData.setTitle(_translate("MainWindow", "Data", None))
        self.menuHelp.setTitle(_translate("MainWindow", "设备 (D)", None))
        self.menu_H.setTitle(_translate("MainWindow", "帮助 (H)", None))
        self.actionOpen.setText(_translate("MainWindow", "Create New", None))
        self.actionImport.setText(_translate("MainWindow", "Open Existing ", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionSetting.setText(_translate("MainWindow", "Resolution", None))
        self.actionRecording_mode.setText(_translate("MainWindow", "Recording mode", None))
        self.actionClient.setText(_translate("MainWindow", "Client", None))
        self.actionServer.setText(_translate("MainWindow", "Server", None))
        self.actionEye_Data.setText(_translate("MainWindow", "Eye data", None))
        self.actionScene_Data.setText(_translate("MainWindow", "Scene video", None))
        self.actionAudio_Data.setText(_translate("MainWindow", "Audio ", None))
        self.actionSocket_out_data.setText(_translate("MainWindow", "Socket out data", None))
        self.actionPC_event.setText(_translate("MainWindow", "PC events", None))
        self.actionAbout_us.setText(_translate("MainWindow", "About us", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

