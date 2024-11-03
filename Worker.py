from PySide6.QtCore import QObject, Signal
from DownloadItem import DownloadItem
import yt_dlp
from Logger import Logger
from YTDLPQtHook import YTDLPQtHook


class Worker(QObject):
    SendResult = Signal(DownloadItem)
    ReDraw = Signal(int)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.logger = Logger()

    def getFormats(self, videoEntry):
        formats = [
            format_info
            for format_info in videoEntry["formats"]
            if ("vcodec" in format_info) and ("acodec" in format_info)
        ]
        videoFormat = [
            format_info
            for format_info in formats
            if (format_info["vcodec"] != "none" and format_info["acodec"] == "none")
        ]
        audioFormat = [
            format_info
            for format_info in formats
            if (format_info["vcodec"] == "none" and format_info["acodec"] != "none")
        ]
        return videoFormat, audioFormat

    def getInfo(self, url: str):
        options = {
            "ignoreerrors": "only_download",
            "logger": self.logger,
            "color": {"stderr": "no_color", "stdout": "no_color"},
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            info_dict: dict = ydl.sanitize_info(info)
        if "entries" in info_dict:
            for entry in info_dict["entries"]:
                if entry is None:
                    continue
                videoFormat, audioFormat = self.getFormats(entry)
                data = DownloadItem(
                    entry["title"],
                    entry["webpage_url"],
                    videoFormat,
                    audioFormat,
                    entry.get("is_live", False),
                )
                self.SendResult.emit(data)
        elif "formats" in info_dict:
            videoFormat, audioFormat = self.getFormats(info_dict)
            data = DownloadItem(
                info_dict["title"],
                info_dict["webpage_url"],
                videoFormat,
                audioFormat,
                info_dict.get("is_live", False),
            )
            self.SendResult.emit(data)

    def doDownload(self, infos: list[DownloadItem], downloadPath: str):
        for item in infos:
            if item.Status == "下載完成":
                continue
            if (
                item.SelectedVideoFormat != "不下載影片"
                and item.SelectedAudioFormat != "不下載音訊"
            ):
                format_str = f"{item.SelectedVideoFormat}+{item.SelectedAudioFormat}"
            elif item.SelectedVideoFormat != "不下載影片":
                format_str = item.SelectedVideoFormat
            elif item.SelectedAudioFormat != "不下載音訊":
                format_str = item.SelectedAudioFormat
            hook = YTDLPQtHook(item, infos.index(item))
            func = lambda row: self.ReDraw.emit(row)
            hook.ReDraw.connect(func)
            options = {
                "paths": {"home": downloadPath},
                "ignoreerrors": "only_download",
                "logger": self.logger,
                "color": {"stderr": "no_color", "stdout": "no_color"},
                "format": format_str,
                "progress_hooks": [hook],
            }
            if item.IsLive:
                options["live_from_start"] = True
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([item.Url])
            hook.ReDraw.disconnect(func)
