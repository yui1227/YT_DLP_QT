from dataclasses import dataclass

@dataclass
class DownloadItem:
    Title: str
    Url: str
    VideoFormat: str
    AudioFormat: str
