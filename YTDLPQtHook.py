from PySide6.QtCore import QObject, Signal
from yt_dlp.downloader.common import FileDownloader
from DownloadItem import DownloadItem


class YTDLPQtHook(QObject):
    ReDraw = Signal(int)
    STATUS_DICT = {"downloading": "下載中", "error": "錯誤", "finished": "下載完成"}

    def __init__(self, item: DownloadItem, idx, parent=None) -> None:
        super(YTDLPQtHook, self).__init__(parent)
        self.item = item
        self.idx = idx

    def __call__(self, d: dict):
        self.hook(d)

    def hook(self, d: dict):
        self.item.Status = self.STATUS_DICT[d["status"]]

        downloaded_bytes = d["downloaded_bytes"]
        if d.get("total_bytes") is not None:
            total_bytes = d["total_bytes"]
            self.item.Progress = float(downloaded_bytes) / float(total_bytes) * 100
        elif d.get("total_bytes_estimate") is not None:
            total_bytes_estimate = d["total_bytes_estimate"]
            self.item.Progress = (
                float(downloaded_bytes) / float(total_bytes_estimate) * 100
            )
        else:
            self.item.Progress = -1.0

        if d["status"] == "downloading":
            self.item.ETA = (
                "未知"
                if d.get("eta") is None
                else FileDownloader.format_seconds(d.get("eta"))
            )
            self.item.Speed = (
                "未知"
                if d.get("speed") is None
                else FileDownloader.format_speed(d.get("speed")).strip()
            )
        else:
            self.item.ETA = FileDownloader.format_seconds(0)
            self.item.Speed = FileDownloader.format_speed(0).strip()
        self.ReDraw.emit(self.idx)
