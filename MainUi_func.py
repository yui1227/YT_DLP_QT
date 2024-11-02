from DownloadListModel import DownloadListModel
from DownloadTableDelegate import DownloadTableDelegate
from MainUi_ui import Ui_MainUi
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QHeaderView,
    QTableView,
    QMenu,
)
from PySide6.QtCore import Signal, QThread, Qt
from PySide6.QtGui import QCloseEvent, QCursor
from Worker import Worker
from DownloadItem import DownloadItem


class Ui_MainFunc(QMainWindow, Ui_MainUi):
    UrlSended = Signal(str)
    Download = Signal(list, str)

    def __init__(self, parent=None):
        super(Ui_MainFunc, self).__init__(parent)
        self.setupUi(self)
        self.model = DownloadListModel()
        self.tableDownloadList.setModel(self.model)
        self.delegate = DownloadTableDelegate()
        self.tableDownloadList.setItemDelegate(self.delegate)
        self.tableDownloadList.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.tableDownloadList.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )
        self.tableDownloadList.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.menu = self.generateMenu()
        self.tableDownloadList.customContextMenuRequested.connect(self.showMenu)

        # 按鈕事件綁定
        self.btnAnalysis.clicked.connect(self.Analysis)
        self.btnSetSavePath.clicked.connect(self.SetSavePath)
        self.btnDownload.clicked.connect(self.requestDownload)

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

    def showMenu(self, pos):
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
        self.thBackground.quit()
        self.thBackground.wait()
        return super().closeEvent(event)
