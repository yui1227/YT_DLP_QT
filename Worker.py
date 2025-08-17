from PySide6.QtCore import QObject, Signal
from DownloadItem import DownloadItem
import yt_dlp
from Logger import Logger
from YTDLPQtHook import YTDLPQtHook
from Config import Config


class Worker(QObject):
    SendResult = Signal(DownloadItem)
    ReDraw = Signal(int)

    def __init__(self, parent=None, config: Config = None):
        super(Worker, self).__init__(parent)
        self.config = config
        self.logger = Logger(self.config.output_color)
        self.video_dict = {
            "avc1": "bv[vcodec^=avc1]",
            "vp09": "bv[vcodec^=vp09]",
            "av01": "bv[vcodec^=av01]"
        }
        self.audio_dict = {
            "mp4a": "ba[acodec^=mp4a]",
            "opus": "ba[acodec^=opus]"
        }

    @staticmethod
    def getFormats(videoEntry):
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
            'forcefilename': True,
            'noprogress': True,
            'outtmpl': {'default': self.config.default_output_filename_template},
            'quiet': True,
            'simulate': True
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            info_dict: dict = ydl.sanitize_info(info)
        if "entries" in info_dict:
            for entry in info_dict["entries"]:
                if entry is None:
                    continue
                videoFormat, audioFormat = Worker.getFormats(entry)
                data = DownloadItem(
                    entry["title"],
                    entry["webpage_url"],
                    self.video_dict.get(self.config.video_codec),
                    self.audio_dict.get(self.config.audio_codec),
                    videoFormat,
                    audioFormat,
                    entry["fulltitle"],
                    entry.get("is_live", False),
                )
                self.SendResult.emit(data)
        elif "formats" in info_dict:
            videoFormat, audioFormat = Worker.getFormats(info_dict)
            data = DownloadItem(
                info_dict["title"],
                info_dict["webpage_url"],
                self.video_dict.get(self.config.video_codec),
                self.audio_dict.get(self.config.audio_codec),
                videoFormat,
                audioFormat,
                info_dict["fulltitle"],
                info_dict.get("is_live", False),
            )
            self.SendResult.emit(data)

    def doDownload(self, infos: list[DownloadItem], downloadPath: str, isMp3: bool = False):
        for item in infos:
            if item.Status == "下載完成":
                continue
            if (
                item.SelectedVideoFormat != "僅音訊"
                and item.SelectedAudioFormat != "僅影片"
            ):
                format_str = f"{item.SelectedVideoFormat}+{item.SelectedAudioFormat}"
            elif item.SelectedVideoFormat != "僅音訊":
                format_str = item.SelectedVideoFormat
            elif item.SelectedAudioFormat != "僅影片":
                format_str = item.SelectedAudioFormat
            hook = YTDLPQtHook(item, infos.index(item))
            def func(row): return self.ReDraw.emit(row)
            hook.ReDraw.connect(func)
            options = {
                "paths": {"home": downloadPath},
                "ignoreerrors": "only_download",
                "logger": self.logger,
                "color": {"stderr": "no_color", "stdout": "no_color"},
                "format": format_str,
                "progress_hooks": [hook],
                'outtmpl': {'default': item.OutputFileName},
            }
            if isMp3:
                options["final_ext"] = "mp3"
                options["format"] = "ba[acodec^=mp3]/ba/b"
                options["postprocessors"] = [{"key": "FFmpegExtractAudio",
                                              "nopostoverwrites": False,
                                              "preferredcodec": "mp3",
                                              "preferredquality": "5"}]
            if item.IsLive:
                options["live_from_start"] = True
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([item.Url])
            hook.ReDraw.disconnect(func)
