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


class Ui_MainFunc(QMainWindow, Ui_MainUi):
    UrlSended = Signal(str)
    Download = Signal(list, str, bool)
    FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

    def __init__(self, parent=None):
        super(Ui_MainFunc, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(
            f"Youtube影片下載器 (YTDLP版本:{yt_dlp.version.CHANNEL}@{yt_dlp.version.__version__})"
        )
        
        # 應用 Flat Design 樣式
        self.apply_flat_design_style()
        
        self.model = DownloadListModel()
        self.tableDownloadList.setModel(self.model)
        self.delegate = DownloadTableDelegate()
        self.tableDownloadList.setItemDelegate(self.delegate)
        
        # 表格樣式設置
        self.setup_table_style()
        
        self.menu = self.generate_menu()
        self.tableDownloadList.customContextMenuRequested.connect(self.show_menu)

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
        self.check_ffmpeg()

    def apply_flat_design_style(self):
        """應用 Flat Design 樣式"""
        style = """
        /* Flat Design 全局設定 */
        * {
            outline: none;
        }
        
        QMainWindow {
            background: #2c3e50;
            color: #ecf0f1;
        }
        
        QWidget {
            font-size: 10pt;
            font-family: 'Cubic 11';
            background: transparent;
        }
        
        /* 中央 Widget */
        QMainWindow::centralwidget {
            background: #2c3e50;
        }
        
        /* 標籤樣式 */
        QLabel {
            color: #f59201;
            font-weight: 600;
            padding: 8px 5px;
            background: transparent;
            font-size: 18pt;
        }
        
        /* 輸入框樣式 - Flat Design */
        QLineEdit {
            background: #f59201;
            padding: 12px 15px;
            font-size: 18pt;
            font-style: bold;
            color: #2c3e50;
            selection-background-color: #3498db;
            selection-color: white;
            font-weight: 500;
        }
        
        QLineEdit:focus {
            border-color: #3498db;
        }
        
        /* QLineEdit:hover {
            border-color: #5d6d7e;
            background: #ffffff;
        } */
        
        /* 按鈕樣式 - 純 Flat Design */
        QPushButton {
            color: #f59201;
            border: none;
            border-radius: 0px;
            padding: 14px 25px;
            font-weight: 700;
            font-size: 20pt;
            min-width: 100px;
            min-height: 25px;
        }

        QPushButton:hover {
            background: #f59201;
            color: #000000;
        }
        
        QPushButton:pressed {
            background: #21618c;
        }
        
        QPushButton:disabled {
            background: #7f8c8d;
            color: #bdc3c7;
        }
        
        /* 分析按鈕 - 綠色 */
        QPushButton#btnAnalysis,
        QPushButton#btnDownload,
        QPushButton#btnDownloadMp3 {
            background: #f59201;
            color: #000000;
        }
        
        QPushButton#btnAnalysis:hover,
        QPushButton#btnDownload:hover,
        QPushButton#btnDownloadMp3:hover
        {
            background: #b86d00;
        }
        
        QPushButton#btnAnalysis:pressed,
        QPushButton#btnDownload:pressed,
        QPushButton#btnDownloadMp3:pressed  {
            background: #1e8449;
        }
        
        /* 設定相關按鈕 - 深灰色 */
        QPushButton#btnSetSavePath, 
        QPushButton#btnOptions, 
        QPushButton#btnOpenDownloadFolder {
            border-color: #f59201;
        }
        
        QPushButton#btnSetSavePath:pressed, 
        QPushButton#btnOptions:pressed, 
        QPushButton#btnOpenDownloadFolder:pressed {
            background: #1b2631;
        }
        
        /* 分組框樣式 - Flat Design */
        QGroupBox {
            font-weight: 700;
            font-size: 20pt;
            color: #ecf0f1;
            border: 3px solid #f59201;
            border-radius: 0px;
            margin: 15px 0px;
            padding-top: 25px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            
            padding: 10px 20px;
            color: #f59201;
            font-weight: 700;
            font-size: 18pt;
        }
        
        /* 表格樣式 - Flat Design */
        QTableView {
            background: #f59201;
            alternate-background-color: #d5dbdb;
            selection-background-color: #3498db;
            selection-color: white;
            gridline-color: #bdc3c7;
            border: 2px solid #34495e;
            border-radius: 0px;
            font-size: 10pt;
            font-weight: 500;
        }
        
        QTableView::item {
            padding: 12px 10px;
            border: none;
            border-bottom: 1px solid #bdc3c7;
            color: #2c3e50;
        }
        
        QTableView::item:selected {
            background: #3498db;
            color: white;
        }
        
        QTableView::item:hover {
            background: #d6dbdf;
            color: #2c3e50;
        }
        
        /* 表格標題 */
        QHeaderView::section {
            background: #b86d00;
            color: #000000;
            padding: 15px 10px;
            border: none;
            border-right: 1px solid #34495e;
            border-bottom: 2px solid #34495e;
            font-weight: 700;
            font-size: 18pt;
        }
        
        QHeaderView::section:hover {
            background: #a86402;
        }
        
        QHeaderView::section:pressed {
            background: #1b2631;
        }
        
        /* 文字瀏覽器 */
        QTextBrowser {
            background: #f59201;
            border: 2px solid #34495e;
            border-radius: 0px;
            padding: 15px;
            color: #2c3e50;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 9pt;
            selection-background-color: #3498db;
            selection-color: white;
            font-weight: 500;
        }
        
        /* 捲軸 - Flat Design */
        QScrollBar:vertical {
            background: #34495e;
            width: 16px;
            border-radius: 0px;
            margin: 0;
            border: none;
        }
        
        QScrollBar::handle:vertical {
            background: #5d6d7e;
            border-radius: 0px;
            min-height: 30px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #85929e;
        }
        
        QScrollBar::handle:vertical:pressed {
            background: #aab7b8;
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0;
        }
        
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;
        }
        
        QScrollBar:horizontal {
            background: #34495e;
            height: 16px;
            border-radius: 0px;
            margin: 0;
            border: none;
        }
        
        QScrollBar::handle:horizontal {
            background: #5d6d7e;
            border-radius: 0px;
            min-width: 30px;
            margin: 2px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: #85929e;
        }
        
        QScrollBar::handle:horizontal:pressed {
            background: #aab7b8;
        }
        
        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            width: 0;
        }
        
        QScrollBar::add-page:horizontal,
        QScrollBar::sub-page:horizontal {
            background: none;
        }
        
        /* 選單樣式 - Flat Design */
        QMenu {
            background: #ecf0f1;
            border: 2px solid #34495e;
            border-radius: 0px;
            padding: 5px 0;
            color: #2c3e50;
            font-size: 10pt;
            font-weight: 600;
        }
        
        QMenu::item {
            padding: 12px 25px;
            background: transparent;
            border: none;
        }
        
        QMenu::item:selected {
            background: #3498db;
            color: white;
        }
        
        QMenu::item:pressed {
            background: #2980b9;
            color: white;
        }
        
        /* 訊息框樣式 */
        QMessageBox {
            background: #ecf0f1;
            color: #2c3e50;
            border: 3px solid #34495e;
        }
        
        QMessageBox QLabel {
            color: #2c3e50;
            font-size: 11pt;
            padding: 15px;
            font-weight: 500;
        }
        
        QMessageBox QPushButton {
            background: #3498db;
            color: white;
            border: none;
            border-radius: 0px;
            padding: 12px 25px;
            font-weight: 700;
            min-width: 100px;
            margin: 5px;
            font-size: 10pt;
        }
        
        QMessageBox QPushButton:hover {
            background: #2980b9;
        }
        
        QMessageBox QPushButton:pressed {
            background: #21618c;
        }
        """
        
        self.setStyleSheet(style)

    def setup_table_style(self):
        """設置表格樣式"""
        self.tableDownloadList.horizontalHeader().setSectionsMovable(True)
        self.tableDownloadList.horizontalHeader().setStretchLastSection(True)
        self.tableDownloadList.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.tableDownloadList.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tableDownloadList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableDownloadList.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
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
        return super().closeEvent(event)

    def openDownloadFolder(self):
        folder_path = self.txtSavePath.text()
        if len(folder_path) == 0:
            folder_path = os.getcwd()
        os.system(f"start {folder_path}")

    def openOptionDialog(self):
        self.optionDialog = Ui_OptionFunc(self, self.config)
        self.optionDialog.show()

    def check_ffmpeg(self):
        """檢查 FFmpeg 是否存在"""
        try:
            import subprocess
            subprocess.run(
                ["ffmpeg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except:
            msgBox = QMessageBox(
                QMessageBox.Icon.Information,
                "找不到推薦可選相依程式",
                f'找不到 FFmpeg，將導致下載的影片和音訊無法合併。\n\n'
                f'請至以下網址下載，將壓縮檔內的 ffmpeg.exe 和 ffprobe.exe 放在跟本程式相同資料夾：\n\n'
                f'{self.FFMPEG_URL}',
                QMessageBox.StandardButton.Ok,
            )
            msgBox.exec()