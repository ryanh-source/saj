# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'index.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStackedWidget, QTableWidget, QTableWidgetItem,
    QTextBrowser, QTextEdit, QWidget)

from saj.ui.widgets import CircularProgressButton
from . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(780, 670)
        MainWindow.setMinimumSize(QSize(780, 670))
        MainWindow.setMaximumSize(QSize(780, 670))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.sidebar_2 = QWidget(self.centralwidget)
        self.sidebar_2.setObjectName(u"sidebar_2")
        self.sidebar_2.setGeometry(QRect(0, 0, 1071, 791))
        font = QFont()
        font.setFamilies([u"Manrope"])
        self.sidebar_2.setFont(font)
        self.sidebar_2.setStyleSheet(u"background-color: rgb(15, 15, 16);")
        self.stackedWidget = QStackedWidget(self.sidebar_2)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(-10, 10, 800, 671))
        self.stackedWidget.setMinimumSize(QSize(800, 631))
        self.stackedWidget.setFont(font)
        self.stackedWidget.setStyleSheet(u"background-color: transparent;")
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        self.home_page.setStyleSheet(u"background-color: #0f0f10;")
        self.consoleLog = QTextEdit(self.home_page)
        self.consoleLog.setObjectName(u"consoleLog")
        self.consoleLog.setGeometry(QRect(30, 320, 341, 291))
        font1 = QFont()
        font1.setFamilies([u"Consolas,Monaco,Courier New,monospace"])
        font1.setPointSize(8)
        self.consoleLog.setFont(font1)
        self.consoleLog.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ArrowCursor))
        self.consoleLog.setStyleSheet(u"QTextEdit, QPlainTextEdit {\n"
"    background-color: #1c1c1e;\n"
"    border: 1px solid #2c2c2e; \n"
"    \n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 16px;\n"
"    border-bottom-right-radius: 16px;\n"
"\n"
"    padding: 10px;\n"
"    color: #c8c8c8;\n"
"    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;\n"
"    font-size: 8pt;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: #0f0f12;\n"
"    width: 14px;\n"
"    margin: 15px 4px 15px 4px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: #2A2A30;\n"
"    min-height: 30px;\n"
"    border-radius: 3px;\n"
"}\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #3f3f46;\n"
"}\n"
"QScrollBar::add-line:vertical, \n"
"QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"}\n"
"QScrollBar::add-page:vertical, \n"
"QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"")
        self.consoleLog.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.consoleLog.setReadOnly(True)
        self.frame_3 = QFrame(self.home_page)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(30, 280, 341, 41))
        self.frame_3.setFont(font)
        self.frame_3.setStyleSheet(u"background-color: rgb(28, 28, 30);\n"
"border: 1px solid #2c2c2e;\n"
"\n"
"/* Curve only the top */\n"
"border-top-left-radius: 10px;\n"
"border-top-right-radius: 10px;\n"
"\n"
"/* Bottom stays straight */\n"
"border-bottom-left-radius: 0;\n"
"border-bottom-right-radius: 0;\n"
"")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.logo_text_9 = QLabel(self.frame_3)
        self.logo_text_9.setObjectName(u"logo_text_9")
        self.logo_text_9.setGeometry(QRect(51, 3, 111, 31))
        font2 = QFont()
        font2.setFamilies([u"Manrope"])
        font2.setPointSize(8)
        font2.setBold(True)
        self.logo_text_9.setFont(font2)
        self.logo_text_9.setStyleSheet(u"background-color: transparent;\n"
"color: #9CA3AF;\n"
"outline: none;\n"
"border: none;")
        self.mp3_icon_2 = QLabel(self.frame_3)
        self.mp3_icon_2.setObjectName(u"mp3_icon_2")
        self.mp3_icon_2.setGeometry(QRect(20, 9, 19, 19))
        font3 = QFont()
        font3.setFamilies([u"Manrope"])
        font3.setPointSize(12)
        self.mp3_icon_2.setFont(font3)
        self.mp3_icon_2.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.mp3_icon_2.setPixmap(QPixmap(u":/images/images/terminal.png"))
        self.mp3_icon_2.setScaledContents(True)
        self.format_qual_frame = QFrame(self.home_page)
        self.format_qual_frame.setObjectName(u"format_qual_frame")
        self.format_qual_frame.setGeometry(QRect(390, 10, 381, 271))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.format_qual_frame.sizePolicy().hasHeightForWidth())
        self.format_qual_frame.setSizePolicy(sizePolicy)
        self.format_qual_frame.setMinimumSize(QSize(318, 179))
        self.format_qual_frame.setFont(font)
        self.format_qual_frame.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame.setFrameShadow(QFrame.Raised)
        self.logo_text_3 = QLabel(self.format_qual_frame)
        self.logo_text_3.setObjectName(u"logo_text_3")
        self.logo_text_3.setGeometry(QRect(20, 40, 101, 31))
        font4 = QFont()
        font4.setFamilies([u"Manrope"])
        font4.setPointSize(9)
        self.logo_text_3.setFont(font4)
        self.logo_text_3.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.logo_text_10 = QLabel(self.format_qual_frame)
        self.logo_text_10.setObjectName(u"logo_text_10")
        self.logo_text_10.setGeometry(QRect(50, 13, 231, 21))
        font5 = QFont()
        font5.setFamilies([u"Manrope"])
        font5.setPointSize(11)
        self.logo_text_10.setFont(font5)
        self.logo_text_10.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"outline: none;\n"
"border: none;")
        self.mp4_icon_3 = QLabel(self.format_qual_frame)
        self.mp4_icon_3.setObjectName(u"mp4_icon_3")
        self.mp4_icon_3.setGeometry(QRect(20, 13, 21, 21))
        self.mp4_icon_3.setFont(font3)
        self.mp4_icon_3.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.mp4_icon_3.setPixmap(QPixmap(u":/images/images/sliders-solid.png"))
        self.mp4_icon_3.setScaledContents(True)
        self.logo_text_6 = QLabel(self.format_qual_frame)
        self.logo_text_6.setObjectName(u"logo_text_6")
        self.logo_text_6.setGeometry(QRect(20, 170, 171, 31))
        font6 = QFont()
        font6.setFamilies([u"Manrope"])
        font6.setPointSize(10)
        self.logo_text_6.setFont(font6)
        self.logo_text_6.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.logo_text_7 = QLabel(self.format_qual_frame)
        self.logo_text_7.setObjectName(u"logo_text_7")
        self.logo_text_7.setGeometry(QRect(20, 244, 341, 31))
        font7 = QFont()
        font7.setFamilies([u"Manrope"])
        font7.setPointSize(8)
        self.logo_text_7.setFont(font7)
        self.logo_text_7.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"outline: none;")
        self.time = QLineEdit(self.format_qual_frame)
        self.time.setObjectName(u"time")
        self.time.setGeometry(QRect(20, 200, 341, 51))
        self.time.setFont(font6)
        self.time.setStyleSheet(u"color: white;\n"
"background-color: rgb(15, 15, 18);\n"
"border-radius: 12px;\n"
"border: 1px solid #2c2c2e;")
        self.time.setAlignment(Qt.AlignCenter)
        self.join_order_frame = QFrame(self.format_qual_frame)
        self.join_order_frame.setObjectName(u"join_order_frame")
        self.join_order_frame.setGeometry(QRect(20, 70, 341, 101))
        self.join_order_frame.setFrameShape(QFrame.StyledPanel)
        self.join_order_frame.setFrameShadow(QFrame.Raised)
        self.format_qual_frame_2 = QFrame(self.home_page)
        self.format_qual_frame_2.setObjectName(u"format_qual_frame_2")
        self.format_qual_frame_2.setGeometry(QRect(390, 300, 381, 141))
        sizePolicy.setHeightForWidth(self.format_qual_frame_2.sizePolicy().hasHeightForWidth())
        self.format_qual_frame_2.setSizePolicy(sizePolicy)
        self.format_qual_frame_2.setMinimumSize(QSize(0, 0))
        self.format_qual_frame_2.setFont(font)
        self.format_qual_frame_2.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame_2.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame_2.setFrameShadow(QFrame.Raised)
        self.logo_text_11 = QLabel(self.format_qual_frame_2)
        self.logo_text_11.setObjectName(u"logo_text_11")
        self.logo_text_11.setGeometry(QRect(50, 13, 161, 21))
        font8 = QFont()
        font8.setFamilies([u"Manrope"])
        font8.setPointSize(11)
        font8.setBold(True)
        self.logo_text_11.setFont(font8)
        self.logo_text_11.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"outline: none;\n"
"border: none;")
        self.mp4_icon_4 = QLabel(self.format_qual_frame_2)
        self.mp4_icon_4.setObjectName(u"mp4_icon_4")
        self.mp4_icon_4.setGeometry(QRect(20, 13, 21, 21))
        self.mp4_icon_4.setFont(font3)
        self.mp4_icon_4.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.mp4_icon_4.setPixmap(QPixmap(u":/images/images/map-location-dot-solid.png"))
        self.mp4_icon_4.setScaledContents(True)
        self.calibrate_position = QPushButton(self.format_qual_frame_2)
        self.calibrate_position.setObjectName(u"calibrate_position")
        self.calibrate_position.setGeometry(QRect(20, 60, 341, 61))
        font9 = QFont()
        font9.setBold(True)
        self.calibrate_position.setFont(font9)
        self.calibrate_position.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.calibrate_position.setStyleSheet(u"QPushButton {\n"
"    background-color: #1a2238;\n"
"    border: 1px solid #2563eb;\n"
"    border-radius: 8px;\n"
"    padding: 14px;\n"
"    color: #ffffff;\n"
"    font-size: 13px;\n"
"    font-weight: 600;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #1f2a45;\n"
"    border: 1px solid #3b82f6;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #16203a;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/images/images/map-pin-solid.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.calibrate_position.setIcon(icon)
        self.calibrate_position.setIconSize(QSize(25, 25))
        self.calibrate_position.setCheckable(True)
        self.calibrated = QPushButton(self.format_qual_frame_2)
        self.calibrated.setObjectName(u"calibrated")
        self.calibrated.setGeometry(QRect(249, 13, 112, 31))
        self.calibrated.setFont(font9)
        self.calibrated.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.calibrated.setStyleSheet(u"QPushButton {\n"
"    background-color: rgba(239, 68, 68, 25);\n"
"    border: 1px solid rgba(239, 68, 68, 80);\n"
"    border-radius: 10px;\n"
"    padding: 2px 10px;\n"
"    color: #ef4444;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    letter-spacing: 0.5px;\n"
"    text-align: center;\n"
"}\n"
"QPushButton:hover, QPushButton:pressed, QPushButton:disabled {\n"
"    background-color: rgba(239, 68, 68, 25);\n"
"    border: 1px solid rgba(239, 68, 68, 80);\n"
"    color: #ef4444;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/images/images/circle-inactive.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.calibrated.setIcon(icon1)
        self.calibrated.setIconSize(QSize(14, 14))
        self.calibrated.setCheckable(False)
        self.format_qual_frame_3 = QFrame(self.home_page)
        self.format_qual_frame_3.setObjectName(u"format_qual_frame_3")
        self.format_qual_frame_3.setGeometry(QRect(30, 10, 341, 251))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.format_qual_frame_3.sizePolicy().hasHeightForWidth())
        self.format_qual_frame_3.setSizePolicy(sizePolicy1)
        self.format_qual_frame_3.setMinimumSize(QSize(0, 0))
        self.format_qual_frame_3.setFont(font)
        self.format_qual_frame_3.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame_3.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame_3.setFrameShadow(QFrame.Raised)
        self.logo_text_14 = QLabel(self.format_qual_frame_3)
        self.logo_text_14.setObjectName(u"logo_text_14")
        self.logo_text_14.setGeometry(QRect(50, 13, 231, 21))
        self.logo_text_14.setFont(font8)
        self.logo_text_14.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"outline: none;\n"
"border: none;")
        self.mp4_icon_5 = QLabel(self.format_qual_frame_3)
        self.mp4_icon_5.setObjectName(u"mp4_icon_5")
        self.mp4_icon_5.setGeometry(QRect(20, 13, 21, 21))
        self.mp4_icon_5.setFont(font3)
        self.mp4_icon_5.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.mp4_icon_5.setPixmap(QPixmap(u":/images/images/rocket.png"))
        self.mp4_icon_5.setScaledContents(True)
        self.status = QPushButton(self.format_qual_frame_3)
        self.status.setObjectName(u"status")
        self.status.setGeometry(QRect(19, 60, 301, 41))
        self.status.setFont(font9)
        self.status.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.status.setStyleSheet(u"QPushButton {\n"
"    background-color: #1f1f25;\n"
"    border: 1px solid #2c2c2e;\n"
"    border-radius: 20px;\n"
"    padding: 6px 18px;\n"
"    color: #9ca3af;\n"
"    font-size: 15px;\n"
"    font-weight: 600;\n"
"    letter-spacing: 1.5px;\n"
"    text-align: center;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/images/images/circle-idle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.status.setIcon(icon2)
        self.status.setIconSize(QSize(14, 14))
        self.status.setCheckable(False)
        self.format_qual_frame_10 = QFrame(self.format_qual_frame_3)
        self.format_qual_frame_10.setObjectName(u"format_qual_frame_10")
        self.format_qual_frame_10.setGeometry(QRect(20, 140, 141, 81))
        sizePolicy1.setHeightForWidth(self.format_qual_frame_10.sizePolicy().hasHeightForWidth())
        self.format_qual_frame_10.setSizePolicy(sizePolicy1)
        self.format_qual_frame_10.setMinimumSize(QSize(0, 0))
        self.format_qual_frame_10.setFont(font)
        self.format_qual_frame_10.setStyleSheet(u"background-color: #0f0f12;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame_10.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame_10.setFrameShadow(QFrame.Raised)
        self.logo_text_15 = QLabel(self.format_qual_frame_10)
        self.logo_text_15.setObjectName(u"logo_text_15")
        self.logo_text_15.setGeometry(QRect(10, 0, 111, 38))
        font10 = QFont()
        font10.setFamilies([u"Manrope"])
        font10.setPointSize(7)
        self.logo_text_15.setFont(font10)
        self.logo_text_15.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"outline: none;")
        self.current_slot = QLabel(self.format_qual_frame_10)
        self.current_slot.setObjectName(u"current_slot")
        self.current_slot.setGeometry(QRect(10, 30, 111, 38))
        self.current_slot.setFont(font6)
        self.current_slot.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.format_qual_frame_11 = QFrame(self.format_qual_frame_3)
        self.format_qual_frame_11.setObjectName(u"format_qual_frame_11")
        self.format_qual_frame_11.setGeometry(QRect(180, 140, 141, 81))
        sizePolicy1.setHeightForWidth(self.format_qual_frame_11.sizePolicy().hasHeightForWidth())
        self.format_qual_frame_11.setSizePolicy(sizePolicy1)
        self.format_qual_frame_11.setMinimumSize(QSize(0, 0))
        self.format_qual_frame_11.setFont(font)
        self.format_qual_frame_11.setStyleSheet(u"background-color: #0f0f12;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame_11.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame_11.setFrameShadow(QFrame.Raised)
        self.logo_text_32 = QLabel(self.format_qual_frame_11)
        self.logo_text_32.setObjectName(u"logo_text_32")
        self.logo_text_32.setGeometry(QRect(10, 0, 111, 38))
        self.logo_text_32.setFont(font10)
        self.logo_text_32.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"outline: none;")
        self.attempts = QLabel(self.format_qual_frame_11)
        self.attempts.setObjectName(u"attempts")
        self.attempts.setGeometry(QRect(10, 30, 111, 38))
        self.attempts.setFont(font6)
        self.attempts.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.format_qual_frame_12 = QFrame(self.home_page)
        self.format_qual_frame_12.setObjectName(u"format_qual_frame_12")
        self.format_qual_frame_12.setGeometry(QRect(390, 460, 381, 151))
        sizePolicy.setHeightForWidth(self.format_qual_frame_12.sizePolicy().hasHeightForWidth())
        self.format_qual_frame_12.setSizePolicy(sizePolicy)
        self.format_qual_frame_12.setMinimumSize(QSize(0, 0))
        self.format_qual_frame_12.setFont(font)
        self.format_qual_frame_12.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame_12.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame_12.setFrameShadow(QFrame.Raised)
        self.logo_text_34 = QLabel(self.format_qual_frame_12)
        self.logo_text_34.setObjectName(u"logo_text_34")
        self.logo_text_34.setGeometry(QRect(50, 13, 161, 21))
        self.logo_text_34.setFont(font8)
        self.logo_text_34.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"outline: none;\n"
"border: none;")
        self.mp4_icon_6 = QLabel(self.format_qual_frame_12)
        self.mp4_icon_6.setObjectName(u"mp4_icon_6")
        self.mp4_icon_6.setGeometry(QRect(20, 13, 21, 21))
        self.mp4_icon_6.setFont(font3)
        self.mp4_icon_6.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.mp4_icon_6.setPixmap(QPixmap(u":/images/images/play-solid.png"))
        self.mp4_icon_6.setScaledContents(True)
        self.stop = QPushButton(self.format_qual_frame_12)
        self.stop.setObjectName(u"stop")
        self.stop.setGeometry(QRect(200, 65, 171, 51))
        self.stop.setFont(font9)
        self.stop.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.stop.setStyleSheet(u"QPushButton {\n"
"    background-color: #2a0d0d;\n"
"    border: 1px solid #dc2626;\n"
"    border-radius: 8px;\n"
"    padding: 14px;\n"
"    color: #ef4444;\n"
"    font-size: 14px;\n"
"    font-weight: 700;\n"
"    letter-spacing: 1px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #321111;\n"
"    border: 1px solid #ef4444;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #200a0a;\n"
"}\n"
"QPushButton:disabled {\n"
"    background-color: #16161a;\n"
"    border: 1px solid #2c2c2e;\n"
"    color: #4b5563;\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/images/images/stop-solid-full.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.stop.setIcon(icon3)
        self.stop.setIconSize(QSize(20, 20))
        self.stop.setCheckable(True)
        self.start = QPushButton(self.format_qual_frame_12)
        self.start.setObjectName(u"start")
        self.start.setGeometry(QRect(10, 65, 171, 51))
        self.start.setFont(font9)
        self.start.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.start.setStyleSheet(u"QPushButton {\n"
"    background-color: #0d2818;\n"
"    border: 1px solid #16a34a;\n"
"    border-radius: 8px;\n"
"    padding: 14px;\n"
"    color: #22c55e;\n"
"    font-size: 14px;\n"
"    font-weight: 700;\n"
"    letter-spacing: 1px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #11321e;\n"
"    border: 1px solid #22c55e;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #0a2014;\n"
"}\n"
"QPushButton:disabled {\n"
"    background-color: #16161a;\n"
"    border: 1px solid #2c2c2e;\n"
"    color: #4b5563;\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/images/images/play-solid-full.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.start.setIcon(icon4)
        self.start.setIconSize(QSize(20, 20))
        self.start.setCheckable(True)
        self.stackedWidget.addWidget(self.home_page)
        self.settings_page = QWidget()
        self.settings_page.setObjectName(u"settings_page")
        self.format_qual_frame_4 = QFrame(self.settings_page)
        self.format_qual_frame_4.setObjectName(u"format_qual_frame_4")
        self.format_qual_frame_4.setGeometry(QRect(30, 10, 341, 221))
        sizePolicy.setHeightForWidth(self.format_qual_frame_4.sizePolicy().hasHeightForWidth())
        self.format_qual_frame_4.setSizePolicy(sizePolicy)
        self.format_qual_frame_4.setMinimumSize(QSize(318, 179))
        self.format_qual_frame_4.setFont(font)
        self.format_qual_frame_4.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame_4.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame_4.setFrameShadow(QFrame.Raised)
        self.logo_text_12 = QLabel(self.format_qual_frame_4)
        self.logo_text_12.setObjectName(u"logo_text_12")
        self.logo_text_12.setGeometry(QRect(50, 13, 231, 21))
        self.logo_text_12.setFont(font4)
        self.logo_text_12.setStyleSheet(u"background-color: transparent;\n"
"color: #9CA3AF;\n"
"outline: none;\n"
"border: none;")
        self.system_icon = QLabel(self.format_qual_frame_4)
        self.system_icon.setObjectName(u"system_icon")
        self.system_icon.setGeometry(QRect(20, 13, 21, 21))
        self.system_icon.setFont(font3)
        self.system_icon.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.system_icon.setPixmap(QPixmap(u":/images/images/terminal-solid.png"))
        self.system_icon.setScaledContents(True)
        self.logo_text_21 = QLabel(self.format_qual_frame_4)
        self.logo_text_21.setObjectName(u"logo_text_21")
        self.logo_text_21.setGeometry(QRect(20, 40, 211, 38))
        self.logo_text_21.setFont(font4)
        self.logo_text_21.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.system_tray = QPushButton(self.format_qual_frame_4)
        self.system_tray.setObjectName(u"system_tray")
        self.system_tray.setGeometry(QRect(283, 56, 41, 28))
        self.system_tray.setFont(font)
        self.system_tray.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.system_tray.setCheckable(True)
        self.logo_text_22 = QLabel(self.format_qual_frame_4)
        self.logo_text_22.setObjectName(u"logo_text_22")
        self.logo_text_22.setGeometry(QRect(20, 104, 211, 38))
        self.logo_text_22.setFont(font4)
        self.logo_text_22.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.auto_launch = QPushButton(self.format_qual_frame_4)
        self.auto_launch.setObjectName(u"auto_launch")
        self.auto_launch.setGeometry(QRect(283, 116, 41, 28))
        self.auto_launch.setFont(font)
        self.auto_launch.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.auto_launch.setCheckable(True)
        self.line = QFrame(self.format_qual_frame_4)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(20, 102, 300, 1))
        self.line.setFont(font)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.logo_text_35 = QLabel(self.format_qual_frame_4)
        self.logo_text_35.setObjectName(u"logo_text_35")
        self.logo_text_35.setGeometry(QRect(20, 130, 241, 31))
        self.logo_text_35.setFont(font10)
        self.logo_text_35.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"outline: none;")
        self.logo_text_36 = QLabel(self.format_qual_frame_4)
        self.logo_text_36.setObjectName(u"logo_text_36")
        self.logo_text_36.setGeometry(QRect(20, 66, 241, 31))
        self.logo_text_36.setFont(font10)
        self.logo_text_36.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"outline: none;")
        self.logo_text_41 = QLabel(self.format_qual_frame_4)
        self.logo_text_41.setObjectName(u"logo_text_41")
        self.logo_text_41.setGeometry(QRect(20, 164, 211, 38))
        self.logo_text_41.setFont(font4)
        self.logo_text_41.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.logo_text_42 = QLabel(self.format_qual_frame_4)
        self.logo_text_42.setObjectName(u"logo_text_42")
        self.logo_text_42.setGeometry(QRect(20, 190, 241, 31))
        self.logo_text_42.setFont(font10)
        self.logo_text_42.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"outline: none;")
        self.line_7 = QFrame(self.format_qual_frame_4)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setGeometry(QRect(20, 164, 300, 1))
        self.line_7.setFont(font)
        self.line_7.setFrameShape(QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)
        self.open_startup = QPushButton(self.format_qual_frame_4)
        self.open_startup.setObjectName(u"open_startup")
        self.open_startup.setGeometry(QRect(283, 180, 41, 28))
        self.open_startup.setFont(font)
        self.open_startup.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.open_startup.setCheckable(True)
        self.format_qual_frame_5 = QFrame(self.settings_page)
        self.format_qual_frame_5.setObjectName(u"format_qual_frame_5")
        self.format_qual_frame_5.setGeometry(QRect(30, 250, 341, 141))
        sizePolicy.setHeightForWidth(self.format_qual_frame_5.sizePolicy().hasHeightForWidth())
        self.format_qual_frame_5.setSizePolicy(sizePolicy)
        self.format_qual_frame_5.setMinimumSize(QSize(0, 0))
        self.format_qual_frame_5.setFont(font)
        self.format_qual_frame_5.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame_5.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame_5.setFrameShadow(QFrame.Raised)
        self.logo_text_16 = QLabel(self.format_qual_frame_5)
        self.logo_text_16.setObjectName(u"logo_text_16")
        self.logo_text_16.setGeometry(QRect(50, 13, 231, 21))
        self.logo_text_16.setFont(font4)
        self.logo_text_16.setStyleSheet(u"background-color: transparent;\n"
"color: #9CA3AF;\n"
"outline: none;\n"
"border: none;")
        self.hotkey_icon = QLabel(self.format_qual_frame_5)
        self.hotkey_icon.setObjectName(u"hotkey_icon")
        self.hotkey_icon.setGeometry(QRect(20, 13, 21, 21))
        self.hotkey_icon.setFont(font3)
        self.hotkey_icon.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.hotkey_icon.setPixmap(QPixmap(u":/images/images/keyboard-regular.png"))
        self.hotkey_icon.setScaledContents(True)
        self.line_2 = QFrame(self.format_qual_frame_5)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(20, 83, 300, 1))
        self.line_2.setFont(font)
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.logo_text_24 = QLabel(self.format_qual_frame_5)
        self.logo_text_24.setObjectName(u"logo_text_24")
        self.logo_text_24.setGeometry(QRect(20, 90, 211, 38))
        self.logo_text_24.setFont(font4)
        self.logo_text_24.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.logo_text_23 = QLabel(self.format_qual_frame_5)
        self.logo_text_23.setObjectName(u"logo_text_23")
        self.logo_text_23.setGeometry(QRect(20, 40, 211, 38))
        self.logo_text_23.setFont(font4)
        self.logo_text_23.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.start_seq = QLabel(self.format_qual_frame_5)
        self.start_seq.setObjectName(u"start_seq")
        self.start_seq.setGeometry(QRect(280, 39, 42, 32))
        font11 = QFont()
        font11.setFamilies([u"Consolas,Courier New,monospace"])
        font11.setBold(True)
        self.start_seq.setFont(font11)
        self.start_seq.setStyleSheet(u"QLabel {\n"
"    background-color: #0f0f12;\n"
"    border: 1px solid #2c2c2e;\n"
"    border-radius: 6px;\n"
"    padding: 4px 12px;\n"
"    color: #3b82f6;\n"
"    font-family: \"Consolas\", \"Courier New\", monospace;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"    min-width: 16px;\n"
"    max-height: 22px;\n"
"}")
        self.start_seq.setAlignment(Qt.AlignCenter)
        self.stop_seq = QLabel(self.format_qual_frame_5)
        self.stop_seq.setObjectName(u"stop_seq")
        self.stop_seq.setGeometry(QRect(280, 95, 42, 32))
        self.stop_seq.setFont(font11)
        self.stop_seq.setStyleSheet(u"QLabel {\n"
"    background-color: #0f0f12;\n"
"    border: 1px solid #2c2c2e;\n"
"    border-radius: 6px;\n"
"    padding: 4px 12px;\n"
"    color: #3b82f6;\n"
"    font-family: \"Consolas\", \"Courier New\", monospace;\n"
"    font-size: 12px;\n"
"    font-weight: bold;\n"
"    min-width: 16px;\n"
"    max-height: 22px;\n"
"}")
        self.stop_seq.setAlignment(Qt.AlignCenter)
        self.format_qual_frame_6 = QFrame(self.settings_page)
        self.format_qual_frame_6.setObjectName(u"format_qual_frame_6")
        self.format_qual_frame_6.setGeometry(QRect(30, 408, 341, 203))
        sizePolicy.setHeightForWidth(self.format_qual_frame_6.sizePolicy().hasHeightForWidth())
        self.format_qual_frame_6.setSizePolicy(sizePolicy)
        self.format_qual_frame_6.setMinimumSize(QSize(318, 179))
        self.format_qual_frame_6.setFont(font)
        self.format_qual_frame_6.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame_6.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame_6.setFrameShadow(QFrame.Raised)
        self.logo_text_17 = QLabel(self.format_qual_frame_6)
        self.logo_text_17.setObjectName(u"logo_text_17")
        self.logo_text_17.setGeometry(QRect(50, 13, 231, 21))
        self.logo_text_17.setFont(font4)
        self.logo_text_17.setStyleSheet(u"background-color: transparent;\n"
"color: #9CA3AF;\n"
"outline: none;\n"
"border: none;")
        self.appearance_icon = QLabel(self.format_qual_frame_6)
        self.appearance_icon.setObjectName(u"appearance_icon")
        self.appearance_icon.setGeometry(QRect(20, 13, 21, 21))
        self.appearance_icon.setFont(font3)
        self.appearance_icon.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.appearance_icon.setPixmap(QPixmap(u":/images/images/palette-solid.png"))
        self.appearance_icon.setScaledContents(True)
        self.line_3 = QFrame(self.format_qual_frame_6)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(20, 107, 300, 1))
        self.line_3.setFont(font)
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)
        self.reduce_motion = QPushButton(self.format_qual_frame_6)
        self.reduce_motion.setObjectName(u"reduce_motion")
        self.reduce_motion.setGeometry(QRect(283, 50, 41, 28))
        self.reduce_motion.setFont(font)
        self.reduce_motion.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.reduce_motion.setCheckable(True)
        self.logo_text_25 = QLabel(self.format_qual_frame_6)
        self.logo_text_25.setObjectName(u"logo_text_25")
        self.logo_text_25.setGeometry(QRect(20, 40, 211, 38))
        self.logo_text_25.setFont(font4)
        self.logo_text_25.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.logo_text_26 = QLabel(self.format_qual_frame_6)
        self.logo_text_26.setObjectName(u"logo_text_26")
        self.logo_text_26.setGeometry(QRect(20, 115, 211, 38))
        self.logo_text_26.setFont(font4)
        self.logo_text_26.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.always_on_top = QPushButton(self.format_qual_frame_6)
        self.always_on_top.setObjectName(u"always_on_top")
        self.always_on_top.setGeometry(QRect(283, 123, 41, 28))
        self.always_on_top.setFont(font)
        self.always_on_top.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.always_on_top.setCheckable(True)
        self.logo_text_27 = QLabel(self.format_qual_frame_6)
        self.logo_text_27.setObjectName(u"logo_text_27")
        self.logo_text_27.setGeometry(QRect(20, 66, 211, 31))
        self.logo_text_27.setFont(font10)
        self.logo_text_27.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"outline: none;")
        self.logo_text_28 = QLabel(self.format_qual_frame_6)
        self.logo_text_28.setObjectName(u"logo_text_28")
        self.logo_text_28.setGeometry(QRect(20, 141, 211, 31))
        self.logo_text_28.setFont(font10)
        self.logo_text_28.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"outline: none;")
        self.format_qual_frame_7 = QFrame(self.settings_page)
        self.format_qual_frame_7.setObjectName(u"format_qual_frame_7")
        self.format_qual_frame_7.setGeometry(QRect(390, 10, 381, 201))
        sizePolicy.setHeightForWidth(self.format_qual_frame_7.sizePolicy().hasHeightForWidth())
        self.format_qual_frame_7.setSizePolicy(sizePolicy)
        self.format_qual_frame_7.setMinimumSize(QSize(318, 179))
        self.format_qual_frame_7.setFont(font)
        self.format_qual_frame_7.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame_7.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame_7.setFrameShadow(QFrame.Raised)
        self.logo_text_18 = QLabel(self.format_qual_frame_7)
        self.logo_text_18.setObjectName(u"logo_text_18")
        self.logo_text_18.setGeometry(QRect(50, 13, 231, 21))
        self.logo_text_18.setFont(font4)
        self.logo_text_18.setStyleSheet(u"background-color: transparent;\n"
"color: #9CA3AF;\n"
"outline: none;\n"
"border: none;")
        self.behavior_icon = QLabel(self.format_qual_frame_7)
        self.behavior_icon.setObjectName(u"behavior_icon")
        self.behavior_icon.setGeometry(QRect(20, 13, 21, 21))
        self.behavior_icon.setFont(font3)
        self.behavior_icon.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.behavior_icon.setPixmap(QPixmap(u":/images/images/hotjar-brands-solid.png"))
        self.behavior_icon.setScaledContents(True)
        self.logo_text_29 = QLabel(self.format_qual_frame_7)
        self.logo_text_29.setObjectName(u"logo_text_29")
        self.logo_text_29.setGeometry(QRect(20, 50, 211, 38))
        self.logo_text_29.setFont(font4)
        self.logo_text_29.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.logo_text_30 = QLabel(self.format_qual_frame_7)
        self.logo_text_30.setObjectName(u"logo_text_30")
        self.logo_text_30.setGeometry(QRect(20, 76, 251, 31))
        self.logo_text_30.setFont(font10)
        self.logo_text_30.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"outline: none;")
        self.poll_interval = QComboBox(self.format_qual_frame_7)
        self.poll_interval.setObjectName(u"poll_interval")
        self.poll_interval.setGeometry(QRect(20, 120, 331, 36))
        font12 = QFont()
        self.poll_interval.setFont(font12)
        self.poll_interval.setStyleSheet(u"QComboBox {\n"
"    background-color: #0f0f12;\n"
"    border: 1px solid #2c2c2e;\n"
"    border-radius: 6px;\n"
"    padding: 8px 12px;\n"
"    color: #c8c8c8;\n"
"    font-size: 12px;\n"
"    min-height: 18px;\n"
"}\n"
"QComboBox:hover {\n"
"    border: 1px solid #3a3a3f;\n"
"}\n"
"QComboBox:focus {\n"
"    border: 1px solid #3b82f6;\n"
"    outline: none;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1a1a1f;\n"
"    border: 1px solid #2c2c2e;\n"
"    border-radius: 6px;\n"
"    color: #c8c8c8;\n"
"    selection-background-color: #2563eb;\n"
"    selection-color: #ffffff;\n"
"    padding: 4px;\n"
"    outline: none;\n"
"}\n"
"QComboBox QAbstractItemView::item {\n"
"    padding: 6px 10px;\n"
"    border-radius: 4px;\n"
"    min-height: 18px;\n"
"}\n"
"QComboBox QAbstractItemView::item:hover {\n"
"    background-color: #1f1f25;\n"
"}")
        self.format_qual_frame_8 = QFrame(self.settings_page)
        self.format_qual_frame_8.setObjectName(u"format_qual_frame_8")
        self.format_qual_frame_8.setGeometry(QRect(390, 230, 381, 231))
        sizePolicy.setHeightForWidth(self.format_qual_frame_8.sizePolicy().hasHeightForWidth())
        self.format_qual_frame_8.setSizePolicy(sizePolicy)
        self.format_qual_frame_8.setMinimumSize(QSize(318, 179))
        self.format_qual_frame_8.setFont(font)
        self.format_qual_frame_8.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame_8.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame_8.setFrameShadow(QFrame.Raised)
        self.logo_text_19 = QLabel(self.format_qual_frame_8)
        self.logo_text_19.setObjectName(u"logo_text_19")
        self.logo_text_19.setGeometry(QRect(50, 13, 231, 21))
        self.logo_text_19.setFont(font4)
        self.logo_text_19.setStyleSheet(u"background-color: transparent;\n"
"color: #9CA3AF;\n"
"outline: none;\n"
"border: none;")
        self.data_icon = QLabel(self.format_qual_frame_8)
        self.data_icon.setObjectName(u"data_icon")
        self.data_icon.setGeometry(QRect(20, 13, 21, 21))
        self.data_icon.setFont(font3)
        self.data_icon.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.data_icon.setPixmap(QPixmap(u":/images/images/database-solid.png"))
        self.data_icon.setScaledContents(True)
        self.open_settings_folder = QPushButton(self.format_qual_frame_8)
        self.open_settings_folder.setObjectName(u"open_settings_folder")
        self.open_settings_folder.setGeometry(QRect(20, 43, 341, 41))
        self.open_settings_folder.setFont(font12)
        self.open_settings_folder.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.open_settings_folder.setStyleSheet(u"QPushButton {\n"
"    background-color: transparent;\n"
"    border: 1px solid #2c2c2e;\n"
"    border-radius: 6px;\n"
"    padding: 8px 14px;\n"
"    color: #c8c8c8;\n"
"    font-size: 12px;\n"
"    text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #1f1f25;\n"
"    border: 1px solid #3a3a3f;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #18181c;\n"
"}")
        self.open_settings_folder.setIconSize(QSize(14, 14))
        self.open_settings_folder.setCheckable(True)
        self.clear_log = QPushButton(self.format_qual_frame_8)
        self.clear_log.setObjectName(u"clear_log")
        self.clear_log.setGeometry(QRect(20, 104, 341, 41))
        self.clear_log.setFont(font12)
        self.clear_log.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clear_log.setStyleSheet(u"QPushButton {\n"
"    background-color: transparent;\n"
"    border: 1px solid #2c2c2e;\n"
"    border-radius: 6px;\n"
"    padding: 8px 14px;\n"
"    color: #c8c8c8;\n"
"    font-size: 12px;\n"
"    text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #1f1f25;\n"
"    border: 1px solid #3a3a3f;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #18181c;\n"
"}")
        self.clear_log.setIconSize(QSize(14, 14))
        self.clear_log.setCheckable(True)
        self.reset_calibration = QPushButton(self.format_qual_frame_8)
        self.reset_calibration.setObjectName(u"reset_calibration")
        self.reset_calibration.setGeometry(QRect(20, 170, 341, 41))
        font13 = QFont()
        font13.setFamilies([u"Manrope"])
        font13.setBold(True)
        self.reset_calibration.setFont(font13)
        self.reset_calibration.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.reset_calibration.setStyleSheet(u"QPushButton {\n"
"    background-color: rgba(239, 68, 68, 25);\n"
"    color: #ef4444;\n"
"    border: 1px solid rgba(239, 68, 68, 80);\n"
"    border-radius: 6px;\n"
"    padding: 6px 16px;\n"
"    font-weight: bold;\n"
"    font-size: 13px;\n"
"    font-family: 'Manrope';\n"
"    text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(239, 68, 68, 50);\n"
"    border: 1px solid rgba(239, 68, 68, 150);\n"
"    color: #f87171;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(239, 68, 68, 75);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgba(239, 68, 68, 10);\n"
"    color: rgba(239, 68, 68, 80);\n"
"    border: 1px solid rgba(239, 68, 68, 30);\n"
"}")
        self.reset_calibration.setIconSize(QSize(14, 14))
        self.reset_calibration.setCheckable(True)
        self.line_4 = QFrame(self.format_qual_frame_8)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setGeometry(QRect(25, 93, 333, 1))
        self.line_4.setFont(font)
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_5 = QFrame(self.format_qual_frame_8)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setGeometry(QRect(25, 156, 333, 1))
        self.line_5.setFont(font)
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)
        self.format_qual_frame_9 = QFrame(self.settings_page)
        self.format_qual_frame_9.setObjectName(u"format_qual_frame_9")
        self.format_qual_frame_9.setGeometry(QRect(390, 480, 381, 131))
        sizePolicy.setHeightForWidth(self.format_qual_frame_9.sizePolicy().hasHeightForWidth())
        self.format_qual_frame_9.setSizePolicy(sizePolicy)
        self.format_qual_frame_9.setMinimumSize(QSize(0, 0))
        self.format_qual_frame_9.setFont(font)
        self.format_qual_frame_9.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame_9.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame_9.setFrameShadow(QFrame.Raised)
        self.logo_text_20 = QLabel(self.format_qual_frame_9)
        self.logo_text_20.setObjectName(u"logo_text_20")
        self.logo_text_20.setGeometry(QRect(50, 13, 231, 21))
        self.logo_text_20.setFont(font4)
        self.logo_text_20.setStyleSheet(u"background-color: transparent;\n"
"color: #9CA3AF;\n"
"outline: none;\n"
"border: none;")
        self.about_icon = QLabel(self.format_qual_frame_9)
        self.about_icon.setObjectName(u"about_icon")
        self.about_icon.setGeometry(QRect(20, 13, 21, 21))
        self.about_icon.setFont(font3)
        self.about_icon.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.about_icon.setPixmap(QPixmap(u":/images/images/circle-info-solid.png"))
        self.about_icon.setScaledContents(True)
        self.logo_text_31 = QLabel(self.format_qual_frame_9)
        self.logo_text_31.setObjectName(u"logo_text_31")
        self.logo_text_31.setGeometry(QRect(20, 52, 111, 31))
        self.logo_text_31.setFont(font4)
        self.logo_text_31.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"outline: none;")
        self.app_version = QLabel(self.format_qual_frame_9)
        self.app_version.setObjectName(u"app_version")
        self.app_version.setGeometry(QRect(260, 52, 111, 31))
        self.app_version.setFont(font7)
        self.app_version.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.app_version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.logo_text_33 = QLabel(self.format_qual_frame_9)
        self.logo_text_33.setObjectName(u"logo_text_33")
        self.logo_text_33.setGeometry(QRect(20, 90, 91, 31))
        self.logo_text_33.setFont(font4)
        self.logo_text_33.setStyleSheet(u"background-color: transparent;\n"
"color: #6B7280;\n"
"border: none;\n"
"outline: none;")
        self.log_file_location = QLabel(self.format_qual_frame_9)
        self.log_file_location.setObjectName(u"log_file_location")
        self.log_file_location.setGeometry(QRect(170, 90, 201, 31))
        self.log_file_location.setFont(font7)
        self.log_file_location.setStyleSheet(u"background-color: transparent;\n"
"color: rgb(63, 98, 233);\n"
"border: none;\n"
"outline: none;")
        self.log_file_location.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.stackedWidget.addWidget(self.settings_page)
        self.updates_page = QWidget()
        self.updates_page.setObjectName(u"updates_page")
        self.format_qual_frame_13 = QFrame(self.updates_page)
        self.format_qual_frame_13.setObjectName(u"format_qual_frame_13")
        self.format_qual_frame_13.setGeometry(QRect(30, 10, 741, 601))
        sizePolicy.setHeightForWidth(self.format_qual_frame_13.sizePolicy().hasHeightForWidth())
        self.format_qual_frame_13.setSizePolicy(sizePolicy)
        self.format_qual_frame_13.setMinimumSize(QSize(318, 179))
        self.format_qual_frame_13.setFont(font)
        self.format_qual_frame_13.setStyleSheet(u"background-color: #1c1c1e;\n"
"border-radius: 16px;\n"
"border: 1px solid #2c2c2e;")
        self.format_qual_frame_13.setFrameShape(QFrame.StyledPanel)
        self.format_qual_frame_13.setFrameShadow(QFrame.Raised)
        self.up_to_date = QLabel(self.format_qual_frame_13)
        self.up_to_date.setObjectName(u"up_to_date")
        self.up_to_date.setGeometry(QRect(200, 120, 331, 41))
        self.up_to_date.setFont(font3)
        self.up_to_date.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.up_to_date.setAlignment(Qt.AlignCenter)
        self.update_status = CircularProgressButton(self.format_qual_frame_13)
        self.update_status.setObjectName(u"update_status")
        self.update_status.setGeometry(QRect(320, 20, 91, 91))
        self.update_status.setFont(font9)
        self.update_status.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.update_status.setStyleSheet(u"QPushButton {\n"
"    background-color: #0d2818;\n"
"    border: 1px solid #16a34a;\n"
"    border-radius: 45px;\n"
"    padding: 14px;\n"
"    color: #22c55e;\n"
"    font-size: 14px;\n"
"    font-weight: 700;\n"
"    letter-spacing: 1px;\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u":/images/images/check-solid.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.update_status.setIcon(icon5)
        self.update_status.setIconSize(QSize(35, 35))
        self.update_status.setCheckable(False)
        self.line_10 = QFrame(self.format_qual_frame_13)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setGeometry(QRect(20, 285, 700, 1))
        self.line_10.setFont(font)
        self.line_10.setFrameShape(QFrame.Shape.HLine)
        self.line_10.setFrameShadow(QFrame.Shadow.Sunken)
        self.release_notes = QTextBrowser(self.format_qual_frame_13)
        self.release_notes.setObjectName(u"release_notes")
        self.release_notes.setGeometry(QRect(20, 310, 701, 111))
        self.release_notes.setStyleSheet(u"QTextBrowser {\n"
"    background-color: rgba(255, 255, 255, 5);\n"
"    border: 1px solid rgba(255, 255, 255, 13);\n"
"    border-radius: 8px;\n"
"    padding: 14px 16px;\n"
"    color: #c8c8c8;\n"
"    font-family: \"Manrope\";\n"
"    font-size: 13px;\n"
"    selection-background-color: rgba(96, 165, 250, 60);\n"
"    selection-color: #ffffff;\n"
"}\n"
"\n"
"QTextBrowser QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 8px;\n"
"    margin: 4px 2px 4px 0;\n"
"}\n"
"\n"
"QTextBrowser QScrollBar::handle:vertical {\n"
"    background: rgba(255, 255, 255, 30);\n"
"    border-radius: 3px;\n"
"    min-height: 24px;\n"
"}\n"
"\n"
"QTextBrowser QScrollBar::handle:vertical:hover {\n"
"    background: rgba(96, 165, 250, 120);\n"
"}\n"
"\n"
"QTextBrowser QScrollBar::add-line:vertical,\n"
"QTextBrowser QScrollBar::sub-line:vertical {\n"
"    height: 0;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QTextBrowser QScrollBar::add-page:vertical,\n"
"QTextBrowser QScrollBar::sub-page:vertical {\n"
"    "
                        "background: transparent;\n"
"}")
        self.download_update = QPushButton(self.format_qual_frame_13)
        self.download_update.setObjectName(u"download_update")
        self.download_update.setGeometry(QRect(20, 220, 341, 41))
        self.download_update.setFont(font13)
        self.download_update.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.download_update.setStyleSheet(u"QPushButton {\n"
"    background-color: rgba(34, 197, 94, 20);\n"
"    border: 1px solid rgba(34, 197, 94, 115);\n"
"    border-radius: 8px;\n"
"    color: #22c55e;\n"
"    font-family: \"Manrope\";\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    letter-spacing: 0.5px;\n"
"    padding: 12px 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(34, 197, 94, 40);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(34, 197, 94, 55);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgba(34, 197, 94, 120);\n"
"    border-color: rgba(34, 197, 94, 60);\n"
"    background-color: rgba(34, 197, 94, 10);\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u":/images/images/download-green.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.download_update.setIcon(icon6)
        self.download_update.setIconSize(QSize(20, 20))
        self.download_update.setCheckable(False)
        self.check_updates = QPushButton(self.format_qual_frame_13)
        self.check_updates.setObjectName(u"check_updates")
        self.check_updates.setGeometry(QRect(380, 220, 341, 41))
        self.check_updates.setFont(font13)
        self.check_updates.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.check_updates.setStyleSheet(u"QPushButton {\n"
"    background-color: rgba(96, 165, 250, 15);\n"
"    border: 1px solid rgba(96, 165, 250, 75);\n"
"    border-radius: 8px;\n"
"    color: #60a5fa;\n"
"    font-family: \"Manrope\";\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    letter-spacing: 0.5px;\n"
"    padding: 12px 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(96, 165, 250, 35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(96, 165, 250, 50);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgba(96, 165, 250, 120);\n"
"    border-color: rgba(96, 165, 250, 40);\n"
"    background-color: rgba(96, 165, 250, 8);\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u":/images/images/repeat-solid.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.check_updates.setIcon(icon7)
        self.check_updates.setIconSize(QSize(20, 20))
        self.check_updates.setCheckable(False)
        self.installed_version = QLabel(self.format_qual_frame_13)
        self.installed_version.setObjectName(u"installed_version")
        self.installed_version.setGeometry(QRect(250, 150, 231, 38))
        self.installed_version.setFont(font4)
        self.installed_version.setLayoutDirection(Qt.LeftToRight)
        self.installed_version.setStyleSheet(u"background-color: transparent;\n"
"color: #9CA3AF;\n"
"outline: none;\n"
"border: none;")
        self.installed_version.setAlignment(Qt.AlignCenter)
        self.last_checked = QLabel(self.format_qual_frame_13)
        self.last_checked.setObjectName(u"last_checked")
        self.last_checked.setGeometry(QRect(250, 180, 231, 31))
        self.last_checked.setFont(font4)
        self.last_checked.setLayoutDirection(Qt.LeftToRight)
        self.last_checked.setStyleSheet(u"background-color: transparent;\n"
"color: #9CA3AF;\n"
"outline: none;\n"
"border: none;")
        self.last_checked.setAlignment(Qt.AlignCenter)
        self.releases_table = QTableWidget(self.format_qual_frame_13)
        self.releases_table.setObjectName(u"releases_table")
        self.releases_table.setGeometry(QRect(20, 450, 701, 131))
        self.releases_table.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.PointingHandCursor))
        self.releases_table.setStyleSheet(u"QTableWidget {\n"
"    background-color: rgba(255, 255, 255, 5);\n"
"    border: 1px solid rgba(255, 255, 255, 15);\n"
"    border-radius: 8px;\n"
"    color: #e6e8ec;\n"
"    font-family: 'Manrope';\n"
"    font-size: 13px;\n"
"    gridline-color: transparent;\n"
"    outline: none;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    padding: 8px 12px;\n"
"    border: none;\n"
"    border-bottom: 1px solid rgba(255, 255, 255, 10);\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: rgba(55, 138, 221, 25);\n"
"    color: #5fa8e8;\n"
"}\n"
"\n"
"QTableWidget::item:hover {\n"
"    background-color: rgba(255, 255, 255, 8);\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: transparent;\n"
"    color: rgba(230, 232, 236, 115);\n"
"    padding: 8px 12px;\n"
"    border: none;\n"
"    border-bottom: 1px solid rgba(255, 255, 255, 20);\n"
"    font-family: 'Manrope';\n"
"    font-size: 11px;\n"
"    font-weight: 500;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: 1px;\n"
"}\n"
"\n"
""
                        "QHeaderView {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 8px;\n"
"    margin: 0;\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: rgba(255, 255, 255, 30);\n"
"    border-radius: 4px;\n"
"    min-height: 24px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: rgba(255, 255, 255, 50);\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    height: 0;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: transparent;\n"
"}")
        self.logo_text_13 = QLabel(self.format_qual_frame_13)
        self.logo_text_13.setObjectName(u"logo_text_13")
        self.logo_text_13.setGeometry(QRect(50, 10, 231, 21))
        self.logo_text_13.setFont(font5)
        self.logo_text_13.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"outline: none;\n"
"border: none;")
        self.mp4_icon_7 = QLabel(self.format_qual_frame_13)
        self.mp4_icon_7.setObjectName(u"mp4_icon_7")
        self.mp4_icon_7.setGeometry(QRect(20, 10, 21, 21))
        self.mp4_icon_7.setFont(font3)
        self.mp4_icon_7.setStyleSheet(u"background-color: transparent;\n"
"color: white;\n"
"border: none;\n"
"outline: none;")
        self.mp4_icon_7.setPixmap(QPixmap(u":/images/images/download-solid.png"))
        self.mp4_icon_7.setScaledContents(True)
        self.stackedWidget.addWidget(self.updates_page)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.logo_text_9.setText(QCoreApplication.translate("MainWindow", u"SYSTEM LOG", None))
        self.mp3_icon_2.setText("")
        self.logo_text_3.setText(QCoreApplication.translate("MainWindow", u"Join Order", None))
        self.logo_text_10.setText(QCoreApplication.translate("MainWindow", u"CONFIGURATION", None))
        self.mp4_icon_3.setText("")
        self.logo_text_6.setText(QCoreApplication.translate("MainWindow", u"Silence Timeout", None))
        self.logo_text_7.setText(QCoreApplication.translate("MainWindow", u"Time to wait before assuming failed join", None))
        self.time.setText(QCoreApplication.translate("MainWindow", u"5.0s", None))
        self.logo_text_11.setText(QCoreApplication.translate("MainWindow", u"CALIBRATION", None))
        self.mp4_icon_4.setText("")
        self.calibrate_position.setText(QCoreApplication.translate("MainWindow", u" Calibrate Positions", None))
        self.calibrated.setText(QCoreApplication.translate("MainWindow", u"NOT SET", None))
        self.logo_text_14.setText(QCoreApplication.translate("MainWindow", u"STATUS", None))
        self.mp4_icon_5.setText("")
        self.status.setText(QCoreApplication.translate("MainWindow", u"IDLE", None))
        self.logo_text_15.setText(QCoreApplication.translate("MainWindow", u"CURRENT SLOT", None))
        self.current_slot.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.logo_text_32.setText(QCoreApplication.translate("MainWindow", u"ATTEMPTS", None))
        self.attempts.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.logo_text_34.setText(QCoreApplication.translate("MainWindow", u"EXECUTION", None))
        self.mp4_icon_6.setText("")
        self.stop.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.start.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.logo_text_12.setText(QCoreApplication.translate("MainWindow", u"SYSTEM TRAY", None))
        self.system_icon.setText("")
        self.logo_text_21.setText(QCoreApplication.translate("MainWindow", u"Enable system tray", None))
        self.system_tray.setText("")
        self.logo_text_22.setText(QCoreApplication.translate("MainWindow", u"Auto-launch with SCP:SL", None))
        self.auto_launch.setText("")
        self.logo_text_35.setText(QCoreApplication.translate("MainWindow", u"Opens the GUI when SCP:SL  opens", None))
        self.logo_text_36.setText(QCoreApplication.translate("MainWindow", u"Allows to minimize to system tray", None))
        self.logo_text_41.setText(QCoreApplication.translate("MainWindow", u"Open on startup", None))
        self.logo_text_42.setText(QCoreApplication.translate("MainWindow", u"Starts app on Windows Start", None))
        self.open_startup.setText("")
        self.logo_text_16.setText(QCoreApplication.translate("MainWindow", u"HOTKEYS", None))
        self.hotkey_icon.setText("")
        self.logo_text_24.setText(QCoreApplication.translate("MainWindow", u"Stop Sequence", None))
        self.logo_text_23.setText(QCoreApplication.translate("MainWindow", u"Start Sequence", None))
        self.start_seq.setText(QCoreApplication.translate("MainWindow", u"S", None))
        self.stop_seq.setText(QCoreApplication.translate("MainWindow", u"Q", None))
        self.logo_text_17.setText(QCoreApplication.translate("MainWindow", u"APPEARANCE", None))
        self.appearance_icon.setText("")
        self.reduce_motion.setText("")
        self.logo_text_25.setText(QCoreApplication.translate("MainWindow", u"Reduce Motion", None))
        self.logo_text_26.setText(QCoreApplication.translate("MainWindow", u"Always on top", None))
        self.always_on_top.setText("")
        self.logo_text_27.setText(QCoreApplication.translate("MainWindow", u"Disable page fades", None))
        self.logo_text_28.setText(QCoreApplication.translate("MainWindow", u"Default pin state at launch", None))
        self.logo_text_18.setText(QCoreApplication.translate("MainWindow", u"GAME BEHAVIOR", None))
        self.behavior_icon.setText("")
        self.logo_text_29.setText(QCoreApplication.translate("MainWindow", u"Game watcher poll interval", None))
        self.logo_text_30.setText(QCoreApplication.translate("MainWindow", u"How often to check if SCP:SL  is running", None))
        self.logo_text_19.setText(QCoreApplication.translate("MainWindow", u"DATA", None))
        self.data_icon.setText("")
        self.open_settings_folder.setText(QCoreApplication.translate("MainWindow", u"Open settings folder", None))
        self.clear_log.setText(QCoreApplication.translate("MainWindow", u"Clear console log", None))
        self.reset_calibration.setText(QCoreApplication.translate("MainWindow", u"Reset Calibration", None))
        self.logo_text_20.setText(QCoreApplication.translate("MainWindow", u"ABOUT", None))
        self.about_icon.setText("")
        self.logo_text_31.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.app_version.setText(QCoreApplication.translate("MainWindow", u"v1.0.2", None))
        self.logo_text_33.setText(QCoreApplication.translate("MainWindow", u"Log file", None))
        self.log_file_location.setText(QCoreApplication.translate("MainWindow", u"..\\Northwood\\SCPSL\\Player.log", None))
        self.up_to_date.setText(QCoreApplication.translate("MainWindow", u"You're up to date", None))
        self.update_status.setText("")
        self.download_update.setText(QCoreApplication.translate("MainWindow", u"DOWNLOAD && INSTALL", None))
        self.check_updates.setText(QCoreApplication.translate("MainWindow", u"CHECK FOR UPDATES", None))
        self.installed_version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
        self.last_checked.setText(QCoreApplication.translate("MainWindow", u"Last Checked", None))
        self.logo_text_13.setText(QCoreApplication.translate("MainWindow", u"UPDATES", None))
        self.mp4_icon_7.setText("")
    # retranslateUi

