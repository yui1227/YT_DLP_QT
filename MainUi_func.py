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
from OptionsDialog_func import Ui_OptionFunc
import base64
import shutil
import sys
from pathlib import Path


class Ui_MainFunc(QMainWindow, Ui_MainUi):
    UrlSended = Signal(str)
    Download = Signal(list, str, bool)

    URLS = {
        "ffmpeg": "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
        "deno": "https://github.com/denoland/deno/releases"
    }

    def __init__(self, parent=None):
        super(Ui_MainFunc, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(
            f"Youtube影片下載器 (YTDLP版本:{yt_dlp.version.CHANNEL}@{yt_dlp.version.__version__})"
        )

        self.model = DownloadListModel()
        self.tableDownloadList.setModel(self.model)
        self.delegate = DownloadTableDelegate()
        self.tableDownloadList.setItemDelegate(self.delegate)

        # 表格樣式設置
        self.setup_table_style()

        self.menu = self.generate_menu()
        self.tableDownloadList.customContextMenuRequested.connect(
            self.show_menu)

        # 按鈕事件綁定
        self.bind_events()

        self.config = Config()
        self.txtSavePath.setText(self.config.output_path)
        size = self.config.size
        self.resize(size["width"], size["height"])

        if self.config.columns_state is not None:
            self.tableDownloadList.horizontalHeader().restoreState(
                base64.b64decode(self.config.columns_state.encode())
            )

        self.setup_thread()
        self.check_dependencies()

    def setup_table_style(self):
        """設置表格樣式"""
        self.tableDownloadList.horizontalHeader().setSectionsMovable(True)
        self.tableDownloadList.horizontalHeader().setStretchLastSection(True)
        self.tableDownloadList.horizontalHeader(
        ).setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.tableDownloadList.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows)
        self.tableDownloadList.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableDownloadList.setHorizontalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.tableDownloadList.setAlternatingRowColors(True)
        self.tableDownloadList.setShowGrid(True)

    def bind_events(self):
        """綁定事件"""
        self.btnAnalysis.clicked.connect(self.Analysis)
        self.btnSetSavePath.clicked.connect(self.SetSavePath)
        self.btnDownload.clicked.connect(self.requestDownload)
        self.btnOpenDownloadFolder.clicked.connect(self.openDownloadFolder)
        self.btnDownloadMp3.clicked.connect(self.requestDownloadMp3)
        self.btnOptions.clicked.connect(self.openOptionDialog)

    def setup_thread(self):
        self.thBackground = QThread()
        self.worker = Worker(config=self.config)
        self.worker.SendResult.connect(self.AddData)
        self.UrlSended.connect(self.worker.getInfo)
        self.worker.logger.log.connect(self.onLog)
        self.worker.ReDraw.connect(self.reDrawTable)
        self.Download.connect(self.worker.doDownload)

        self.worker.moveToThread(self.thBackground)
        self.thBackground.start()

    def generate_menu(self):
        menu = QMenu(self)
        delete_action = menu.addAction("刪除")
        delete_action.triggered.connect(self.onDelete)
        return menu

    def show_menu(self, pos: QPoint):
        self.menu.exec(QCursor.pos())

    def onDelete(self):
        idx = self.tableDownloadList.currentIndex()
        row = idx.row()
        self.model.removeRow(row)

    def Analysis(self):
        url = self.txtUrl.text()
        if url.isspace() or len(url) == 0:
            return
        self.UrlSended.emit(url)

    def SetSavePath(self):
        path = QFileDialog.getExistingDirectory(self, "請選擇影片下載位置...")
        if path:  # 只有當用戶選擇了路徑時才設置
            self.txtSavePath.setText(path)

    def requestDownload(self):
        self.Download.emit(self.model._data, self.txtSavePath.text(), False)

    def requestDownloadMp3(self):
        self.Download.emit(self.model._data, self.txtSavePath.text(), True)

    def AddData(self, item: DownloadItem):
        row = self.model.rowCount()
        self.model.insertRows(row, item)

    def onLog(self, log: str):
        self.txtOutput.append(log)

    def reDrawTable(self, row: int):
        for i in [4, 5, 6, 7]:
            self.tableDownloadList.update(self.model.index(row, i))

    def closeEvent(self, event: QCloseEvent) -> None:
        self.config.columns_state = \
            base64.b64encode(
                self.tableDownloadList.horizontalHeader().saveState().data()).decode()
        self.config.size = {"width": self.width(), "height": self.height()}
        self.config.output_path = self.txtSavePath.text()
        self.config.save()
        self.thBackground.quit()
        return super().closeEvent(event)

    def openDownloadFolder(self):
        folder_path = self.txtSavePath.text()
        if len(folder_path) == 0:
            folder_path = os.getcwd()
        os.system(f"start {folder_path}")

    def openOptionDialog(self):
        self.optionDialog = Ui_OptionFunc(self, self.config)
        self.optionDialog.show()

    def get_app_dir(self):
        """取得程式執行檔所在的絕對路徑"""
        if getattr(sys, 'frozen', False):
            return Path(sys.executable).parent
        return Path(__file__).parent

    def is_tool_available(self, name):
        """檢查特定工具是否存在於程式目錄或 PATH"""
        # 1. 檢查系統 PATH (shutil.which 會自動處理 Windows 的 .exe)
        if shutil.which(name):
            return True

        # 2. 檢查程式當前目錄
        ext = ".exe" if sys.platform == "win32" else ""
        local_path = self.get_app_dir() / f"{name}{ext}"
        return local_path.exists()

    def check_dependencies(self):
        """統一檢查所有必要的相依程式"""
        missing_tools = []

        # 這裡列出所有要檢查的工具名稱
        for tool in ["ffmpeg", "deno"]:
            if not self.is_tool_available(tool):
                missing_tools.append(tool)

        if missing_tools:
            self._show_missing_alert(missing_tools)
            return False
        return True

    def _show_missing_alert(self, missing_tools):
        """根據缺少的工具生成警告訊息"""
        # 建立動態訊息
        msg_details = ""
        for tool in missing_tools:
            url = self.URLS.get(tool, "請搜尋官網下載")
            msg_details += f"• **{tool.upper()}**: 請至 {url} 下載並放在程式目錄。\n"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setWindowTitle("缺少的相依程式")
        msgBox.setText("偵測到系統缺少必要的執行檔，部分功能將受限：")
        msgBox.setInformativeText(msg_details)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()
