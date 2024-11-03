from dataclasses import dataclass, field
from yt_dlp.utils._utils import format_bytes


@dataclass
class DownloadItem:
    Title: str
    Url: str
    SelectedVideoFormat: str = field(
        init=False, default_factory=lambda: "bv[vcodec^=avc1]"
    )
    SelectedAudioFormat: str = field(
        init=False, default_factory=lambda: "ba[acodec^=mp4a]"
    )
    VideoFormat: list
    AudioFormat: list
    Status: str = field(init=False, default_factory=lambda: "等待下載")
    Progress: float = field(init=False, default_factory=lambda: 0.0)
    ETA: str = field(init=False, default_factory=lambda: "未知")
    Speed: str = field(init=False, default_factory=lambda: "未知")
    IsLive: bool

    @staticmethod
    def checkIfAV1(formatlist: list[dict]):
        return any(
            [
                format_info
                for format_info in formatlist
                if format_info.get("vcodec", "").startswith("av01")
            ]
        )

    def __post_init__(self):
        self.vfDict = {}
        for format_info in self.VideoFormat:
            format_id = format_info.get("format_id")
            if format_info.get("filesize") is not None:
                filesize = f"""{format_bytes(format_info["filesize"])}"""
            elif format_info.get("filesize_approx") is not None:
                filesize = f"""~{format_bytes(format_info["filesize_approx"])}"""
            else:
                filesize = ""
            fps = int(format_info.get("fps"))
            ext = format_info.get("ext")
            vcodec = format_info.get("vcodec")
            format_note = format_info.get("format_note", "")

            self.vfDict[format_id] = (
                f"{format_id:<3}\t{filesize}\t{fps:<10}\t{ext:<10}\t{vcodec:<20}\t{format_note:<15}"
            )

        if DownloadItem.checkIfAV1(self.VideoFormat):
            self.vfDict["bv[vcodec^=av01]"] = (
                "best(格式mp4，編碼av1，壓縮比最高，解碼消耗效能高)"
            )
        self.vfDict["bv[vcodec^=vp09]"] = (
            "best(格式webm，編碼vp9，壓縮比較高，廣泛使用的格式)"
        )
        self.vfDict["bv[vcodec^=avc1]"] = (
            "best(格式mp4，編碼avc1，壓縮比一般，最廣泛使用的格式)"
        )
        self.vfDict["不下載影片"] = "不下載影片"

        self.afDict = {}
        for format_info in self.AudioFormat:
            format_id = format_info.get("format_id")
            if format_info.get("filesize") is not None:
                filesize = f"""{format_bytes(format_info.get("filesize"))}"""
            elif format_info.get("filesize_approx") is not None:
                filesize = f"""~{format_bytes(format_info.get("filesize_approx"))}"""
            else:
                filesize = ""
            ext = format_info.get("ext")
            acodec = format_info.get("acodec")
            format_note = format_info.get("format_note", "")

            self.afDict[format_id] = (
                f"{format_id:<3}\t{filesize:<20}\t{ext:<4}\t{acodec:<20}\t{format_note:<15}"
            )
        self.afDict["ba[acodec^=opus]"] = (
            "best(格式webm，編碼opus，壓縮比較高，廣泛使用的格式)"
        )
        self.afDict["ba[acodec^=mp4a]"] = (
            "best(格式m4a，編碼mp4a，壓縮比高，最廣泛使用的格式)"
        )
        self.afDict["不下載音訊"] = "不下載音訊"

        self.reverse_vfDict = {v: k for k, v in self.vfDict.items()}

        self.reverse_afDict = {v: k for k, v in self.afDict.items()}
