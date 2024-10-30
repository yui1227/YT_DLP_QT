from DownloadListModel import DownloadListModel
from MainUi_ui import Ui_MainUi
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QHeaderView
from urllib.parse import urlparse, parse_qs


class Ui_MainFunc(QMainWindow, Ui_MainUi):
    def __init__(self, parent=None):
        super(Ui_MainFunc, self).__init__(parent)
        self.setupUi(self)
        self.model = DownloadListModel()
        self.tableDownloadList.setModel(self.model)
        self.tableDownloadList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # 按鈕事件綁定
        self.btnAnalysis.clicked.connect(self.Analysis)
        self.btnSetSavePath.clicked.connect(self.SetSavePath)
        self.btnDownload.clicked.connect(self.Download)

    def Analysis(self):
        url = self.txtUrl.text()
        # 解析網址內的query參數
        urldata = urlparse(url)
        query_dict = parse_qs(urldata.query)
        QMessageBox.information(self, '提示', str(
            query_dict), QMessageBox.StandardButton.Ok)
        # 三種情況
        if ('list' in query_dict) and ('v' in query_dict):
            pass
        elif 'v' in query_dict:
            pass
        elif 'list' in query_dict:
            pass
        else:
            pass

    def SetSavePath(self):
        path = QFileDialog.getExistingDirectory(self, '請選擇影片下載位置...')
        self.txtSavePath.setText(path)

    def Download(self):
        pass
