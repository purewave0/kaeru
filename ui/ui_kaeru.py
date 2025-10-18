# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'kaeru.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModality.NonModal)
        MainWindow.resize(830, 804)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(16)
        MainWindow.setFont(font)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.actionKana_reading = QAction(MainWindow)
        self.actionKana_reading.setObjectName(u"actionKana_reading")
        self.actionKana_reading.setCheckable(True)
        self.actionKana_reading.setChecked(True)
        self.actionKana_reading.setMenuRole(QAction.MenuRole.TextHeuristicRole)
        self.actionWord_type = QAction(MainWindow)
        self.actionWord_type.setObjectName(u"actionWord_type")
        self.actionWord_type.setCheckable(True)
        self.actionWord_type.setChecked(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(16)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.word_to_conjugate = QLabel(self.centralwidget)
        self.word_to_conjugate.setObjectName(u"word_to_conjugate")
        font1 = QFont()
        font1.setPointSize(64)
        self.word_to_conjugate.setFont(font1)
        self.word_to_conjugate.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.word_to_conjugate.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_to_conjugate.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_2.addWidget(self.word_to_conjugate)

        self.kana_reading = QLabel(self.centralwidget)
        self.kana_reading.setObjectName(u"kana_reading")
        self.kana_reading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.kana_reading)

        self.word_type = QLabel(self.centralwidget)
        self.word_type.setObjectName(u"word_type")
        self.word_type.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.word_type)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.inflection_helper_text = QLabel(self.centralwidget)
        self.inflection_helper_text.setObjectName(u"inflection_helper_text")
        self.inflection_helper_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.inflection_helper_text)

        self.conjugation = QLabel(self.centralwidget)
        self.conjugation.setObjectName(u"conjugation")
        font2 = QFont()
        font2.setPointSize(24)
        font2.setBold(True)
        self.conjugation.setFont(font2)
        self.conjugation.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.conjugation)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.answer = QLineEdit(self.centralwidget)
        self.answer.setObjectName(u"answer")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.answer.sizePolicy().hasHeightForWidth())
        self.answer.setSizePolicy(sizePolicy1)
        self.answer.setMaximumSize(QSize(512, 16777215))
        font3 = QFont()
        font3.setPointSize(24)
        self.answer.setFont(font3)
        self.answer.setAutoFillBackground(False)
        self.answer.setStyleSheet(u"padding: 8px;")
        self.answer.setClearButtonEnabled(False)

        self.horizontalLayout.addWidget(self.answer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.answer_button = QPushButton(self.centralwidget)
        self.answer_button.setObjectName(u"answer_button")
        self.answer_button.setMaximumSize(QSize(512, 16777215))
        self.answer_button.setFont(font3)
        self.answer_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.answer_button.setAutoDefault(True)
        self.answer_button.setFlat(False)

        self.horizontalLayout_2.addWidget(self.answer_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.score_section = QHBoxLayout()
        self.score_section.setObjectName(u"score_section")
        self.score_section.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.current_streak_layout = QHBoxLayout()
        self.current_streak_layout.setSpacing(6)
        self.current_streak_layout.setObjectName(u"current_streak_layout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.current_streak_layout.addItem(self.horizontalSpacer_3)

        self.current_streak_helper_text = QLabel(self.centralwidget)
        self.current_streak_helper_text.setObjectName(u"current_streak_helper_text")
        font4 = QFont()
        font4.setPointSize(16)
        font4.setBold(False)
        self.current_streak_helper_text.setFont(font4)

        self.current_streak_layout.addWidget(self.current_streak_helper_text)

        self.current_streak = QLabel(self.centralwidget)
        self.current_streak.setObjectName(u"current_streak")
        self.current_streak.setMinimumSize(QSize(32, 0))

        self.current_streak_layout.addWidget(self.current_streak)


        self.score_section.addLayout(self.current_streak_layout)

        self.horizontalSpacer_2 = QSpacerItem(24, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.score_section.addItem(self.horizontalSpacer_2)

        self.highest_streak_layout = QHBoxLayout()
        self.highest_streak_layout.setObjectName(u"highest_streak_layout")
        self.highest_streak_helper_text = QLabel(self.centralwidget)
        self.highest_streak_helper_text.setObjectName(u"highest_streak_helper_text")
        self.highest_streak_helper_text.setFont(font4)

        self.highest_streak_layout.addWidget(self.highest_streak_helper_text)

        self.highest_streak = QLabel(self.centralwidget)
        self.highest_streak.setObjectName(u"highest_streak")
        self.highest_streak.setMinimumSize(QSize(32, 0))

        self.highest_streak_layout.addWidget(self.highest_streak)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.highest_streak_layout.addItem(self.horizontalSpacer)


        self.score_section.addLayout(self.highest_streak_layout)


        self.verticalLayout_2.addLayout(self.score_section)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 830, 31))
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuView.menuAction())
        self.menuView.addAction(self.actionKana_reading)
        self.menuView.addAction(self.actionWord_type)

        self.retranslateUi(MainWindow)

        self.answer_button.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"kaeru", None))
        self.actionKana_reading.setText(QCoreApplication.translate("MainWindow", u"Kana reading", None))
        self.actionWord_type.setText(QCoreApplication.translate("MainWindow", u"Word type", None))
        self.word_to_conjugate.setText(QCoreApplication.translate("MainWindow", u"\u9ad8\u3044", None))
        self.kana_reading.setText(QCoreApplication.translate("MainWindow", u"\uff08\u305f\u304b\u3044\uff09", None))
        self.word_type.setText(QCoreApplication.translate("MainWindow", u"\u3044-adjective", None))
        self.inflection_helper_text.setText(QCoreApplication.translate("MainWindow", u"Conjugate to:", None))
        self.conjugation.setText(QCoreApplication.translate("MainWindow", u"POLITE", None))
        self.answer.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your answer", None))
        self.answer_button.setText(QCoreApplication.translate("MainWindow", u"Answer", None))
        self.current_streak_helper_text.setText(QCoreApplication.translate("MainWindow", u"Current Streak:", None))
        self.current_streak.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.highest_streak_helper_text.setText(QCoreApplication.translate("MainWindow", u"Highest Streak:", None))
        self.highest_streak.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

