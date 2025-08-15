# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OptionsDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_OptionDialog(object):
    def setupUi(self, OptionDialog):
        if not OptionDialog.objectName():
            OptionDialog.setObjectName(u"OptionDialog")
        OptionDialog.resize(424, 163)
        self.centralwidget = QWidget(OptionDialog)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.cmbPreferVideo = QComboBox(self.centralwidget)
        self.cmbPreferVideo.setObjectName(u"cmbPreferVideo")

        self.horizontalLayout.addWidget(self.cmbPreferVideo)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.cmbPreferAudio = QComboBox(self.centralwidget)
        self.cmbPreferAudio.setObjectName(u"cmbPreferAudio")

        self.horizontalLayout_3.addWidget(self.cmbPreferAudio)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.txtOutputFileNameTemplate = QLineEdit(self.centralwidget)
        self.txtOutputFileNameTemplate.setObjectName(u"txtOutputFileNameTemplate")

        self.horizontalLayout_2.addWidget(self.txtOutputFileNameTemplate)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        OptionDialog.setCentralWidget(self.centralwidget)

        self.retranslateUi(OptionDialog)

        QMetaObject.connectSlotsByName(OptionDialog)
    # setupUi

    def retranslateUi(self, OptionDialog):
        OptionDialog.setWindowTitle(QCoreApplication.translate("OptionDialog", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("OptionDialog", u"\u504f\u597d\u683c\u5f0f(\u5f71\u7247)", None))
        self.label_3.setText(QCoreApplication.translate("OptionDialog", u"\u504f\u597d\u683c\u5f0f(\u97f3\u8a0a)", None))
        self.label_2.setText(QCoreApplication.translate("OptionDialog", u"\u8f38\u51fa\u6a94\u6848\u540d\u7a31", None))
    # retranslateUi

