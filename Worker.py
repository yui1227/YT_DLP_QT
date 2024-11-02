from PySide6.QtCore import QObject, Signal
from DownloadItem import DownloadItem
import yt_dlp
from Logger import Logger


class Worker(QObject):
    SendResult = Signal(DownloadItem)
    DownloadDone = Signal(int, DownloadItem)

    def __init__(self):
        super().__init__()
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
            if (
                format_info["vcodec"] != "none"
                and format_info["acodec"] == "none"
                # and (format_info["protocol"] in ["http", "https"])
            )
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
            # "listformats": True,
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
                )
                self.SendResult.emit(data)
        elif "formats" in info_dict:
            videoFormat, audioFormat = self.getFormats(info_dict)
            data = DownloadItem(
                info_dict["title"], info_dict["webpage_url"], videoFormat, audioFormat
            )
            self.SendResult.emit(data)

    def doDownload(self, infos: list[DownloadItem], downloadPath: str):
        print(infos, downloadPath)
        for item in infos:
            if (
                item.SelectedVideoFormat != "不下載影片"
                and item.SelectedAudioFormat != "不下載音訊"
            ):
                format_str = f"{item.SelectedVideoFormat}+{item.SelectedAudioFormat}"
            elif item.SelectedVideoFormat != "不下載影片":
                format_str = item.SelectedVideoFormat
            elif item.SelectedAudioFormat != "不下載音訊":
                format_str = item.SelectedAudioFormat
            options = {
                "paths": {"home": downloadPath},
                "ignoreerrors": "only_download",
                "logger": self.logger,
                "color": {"stderr": "no_color", "stdout": "no_color"},
                "format": format_str,
                'live_from_start': True
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                ret = ydl.download([item.Url])
                self.DownloadDone.emit(ret, item)
