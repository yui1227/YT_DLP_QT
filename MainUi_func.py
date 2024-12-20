from Config import Config
from DownloadListModel import DownloadListModel
from DownloadTableDelegate import DownloadTableDelegate
from MainUi_ui import Ui_MainUi
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QHeaderView,
    QTableView,
    QMenu,
    QMessageBox,
    QAbstractItemView,
)
from PySide6.QtCore import Signal, QThread, Qt, QPoint
from PySide6.QtGui import QCloseEvent, QCursor
from Worker import Worker
from DownloadItem import DownloadItem
import yt_dlp.version
import os


class Ui_MainFunc(QMainWindow, Ui_MainUi):
    UrlSended = Signal(str)
    Download = Signal(list, str)
    FFMPEG_URL = "https://www.gyan.dpyev/ffmpeg/builds/ffmpeg-release-essentials.zip"

    def __init__(self, parent=None):
        super(Ui_MainFunc, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(
            f"Youtube影片下載器(YTDLP版本:{yt_dlp.version.CHANNEL}@{yt_dlp.version.__version__})"
        )
        self.model = DownloadListModel()
        self.tableDownloadList.setModel(self.model)
        self.delegate = DownloadTableDelegate()
        self.tableDownloadList.setItemDelegate(self.delegate)
        # self.tableDownloadList.horizontalHeader().setSectionResizeMode(
        #     QHeaderView.ResizeMode.Interactive
        # )
        self.tableDownloadList.horizontalHeader().setStretchLastSection(True)
        self.tableDownloadList.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft
        )
        self.tableDownloadList.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )
        self.tableDownloadList.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.tableDownloadList.setHorizontalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.menu = self.generateMenu()
        self.tableDownloadList.customContextMenuRequested.connect(self.showMenu)

        # 按鈕事件綁定
        self.btnAnalysis.clicked.connect(self.Analysis)
        self.btnSetSavePath.clicked.connect(self.SetSavePath)
        self.btnDownload.clicked.connect(self.requestDownload)
        self.btnOpenDownloadFolder.clicked.connect(self.openDownloadFolder)

        self.setupThread()

        try:
            import subprocess

            subprocess.run(
                ["ffmpeg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except:
            msgBox = QMessageBox(
                QMessageBox.Icon.Information,
                "找不到推薦可選相依程式",
                f'找不到ffmpeg，將導致下載的影片和音訊無法合併，請至以下網址下載，將壓縮檔內的ffmpeg.exe和ffprobe.exe放在跟本程式相同資料夾。<br/><a href="{self.FFMPEG_URL}">{self.FFMPEG_URL}</a>',
                QMessageBox.StandardButton.Ok,
            )
            msgBox.setTextFormat(Qt.TextFormat.RichText)
            msgBox.exec()

        self.config = Config()
        self.txtSavePath.setText(self.config.getOutputPath())
        size = self.config.getSize()
        self.resize(size["width"], size["height"])
        column_width = self.config.getColumnsWidth()
        for idx, width in enumerate(column_width):
            self.tableDownloadList.setColumnWidth(idx, width)

    def setupThread(self):
        self.thBackground = QThread()
        self.worker = Worker()
        self.worker.SendResult.connect(self.AddData)
        self.UrlSended.connect(self.worker.getInfo)
        self.worker.logger.log.connect(self.onLog)
        self.worker.ReDraw.connect(self.reDrawTable)
        self.Download.connect(self.worker.doDownload)

        self.worker.moveToThread(self.thBackground)
        self.thBackground.start()

    def generateMenu(self):
        menu = QMenu(self)
        menu.addAction("刪除", self.onDelete)
        return menu

    def showMenu(self, pos: QPoint):
        self.menu.exec(QCursor.pos())

    def onDelete(self):
        idx = self.tableDownloadList.currentIndex()
        row = idx.row()
        self.model.removeRow(row)

    def Analysis(self):
        url = self.txtUrl.text()
        self.UrlSended.emit(url)

    def SetSavePath(self):
        path = QFileDialog.getExistingDirectory(self, "請選擇影片下載位置...")
        self.txtSavePath.setText(path)

    def requestDownload(self):
        self.Download.emit(self.model._data, self.txtSavePath.text())

    def AddData(self, item: DownloadItem):
        row = self.model.rowCount()
        self.model.insertRows(row, item)

    def onLog(self, log: str):
        self.txtOutput.append(log)

    def reDrawTable(self, row: int):
        for i in [4, 5, 6, 7]:
            self.tableDownloadList.update(self.model.index(row, i))

    def closeEvent(self, event: QCloseEvent) -> None:
        # self.thBackground.quit()
        # self.thBackground.wait()
        return super().closeEvent(event)

    def openDownloadFolder(self):
        folder_path = self.txtSavePath.text()
        if len(folder_path) == 0:
            folder_path = os.getcwd()
        os.system(f"start {folder_path}")
