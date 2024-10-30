# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainUi.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_MainUi(object):
    def setupUi(self, MainUi):
        if not MainUi.objectName():
            MainUi.setObjectName(u"MainUi")
        MainUi.resize(526, 469)
        self.centralwidget = QWidget(MainUi)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.txtUrl = QLineEdit(self.centralwidget)
        self.txtUrl.setObjectName(u"txtUrl")

        self.horizontalLayout.addWidget(self.txtUrl)

        self.btnAnalysis = QPushButton(self.centralwidget)
        self.btnAnalysis.setObjectName(u"btnAnalysis")

        self.horizontalLayout.addWidget(self.btnAnalysis)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.txtSavePath = QLineEdit(self.centralwidget)
        self.txtSavePath.setObjectName(u"txtSavePath")

        self.horizontalLayout_5.addWidget(self.txtSavePath)

        self.btnSetSavePath = QPushButton(self.centralwidget)
        self.btnSetSavePath.setObjectName(u"btnSetSavePath")

        self.horizontalLayout_5.addWidget(self.btnSetSavePath)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tableDownloadList = QTableView(self.groupBox)
        self.tableDownloadList.setObjectName(u"tableDownloadList")

        self.horizontalLayout_2.addWidget(self.tableDownloadList)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.txtOutput = QTextBrowser(self.groupBox_2)
        self.txtOutput.setObjectName(u"txtOutput")

        self.horizontalLayout_3.addWidget(self.txtOutput)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.btnDownload = QPushButton(self.centralwidget)
        self.btnDownload.setObjectName(u"btnDownload")

        self.horizontalLayout_4.addWidget(self.btnDownload)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        MainUi.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainUi)

        QMetaObject.connectSlotsByName(MainUi)
    # setupUi

    def retranslateUi(self, MainUi):
        MainUi.setWindowTitle(QCoreApplication.translate("MainUi", u"Youtube\u5f71\u7247\u4e0b\u8f09\u5668", None))
        self.label.setText(QCoreApplication.translate("MainUi", u"Youtube\u7db2\u5740\uff1a", None))
        self.btnAnalysis.setText(QCoreApplication.translate("MainUi", u"\u5206\u6790", None))
        self.label_2.setText(QCoreApplication.translate("MainUi", u"\u5132\u5b58\u4f4d\u7f6e\uff1a", None))
        self.btnSetSavePath.setText(QCoreApplication.translate("MainUi", u"\u8a2d\u5b9a", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainUi", u"\u4e0b\u8f09\u5217\u8868", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainUi", u"\u8f38\u51fa", None))
        self.btnDownload.setText(QCoreApplication.translate("MainUi", u"\u958b\u59cb\u4e0b\u8f09", None))
    # retranslateUi

