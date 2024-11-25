import json
import os


class Config:
    CONFIG_FILENAME = "ytdlpqt.json"
    DEFAULT_DICT = {
        "default_output_format": "%(title)s [%(id)s].%(ext)s",
        "columns_width": [250] * 9,
        "output_templates": {"default": "%(title)s [%(id)s].%(ext)s"},
        "size": {"width": 1200, "height": 630},
        "output_color": {
            "info": "aqua",
            "warning": "orange",
            "error": "red",
        },
        "output_path": "",
        "prefferred_video_codec": "bv[vcodec^=avc1]",
        "prefferred_audio_codec": "ba[acodec^=mp4a]",
    }

    def __init__(self) -> None:
        if not os.path.isfile(self.CONFIG_FILENAME):
            with open(self.CONFIG_FILENAME, mode="w", encoding="utf-8") as f:
                json.dump(self.DEFAULT_DICT, f, ensure_ascii=False, indent=4)
        with open(self.CONFIG_FILENAME, mode="r", encoding="utf-8") as f:
            # 補上後來新加的設定
            self.setting = self.DEFAULT_DICT | json.load(f)

    def getDefaultOutputFormat(self) -> str:
        return self.setting["default_output_format"]

    def getColumnsWidth(self) -> list[int]:
        return self.setting["columns_width"]

    def getOutputTemplates(self) -> dict[str, str]:
        return self.setting["output_templates"]

    def getSize(self) -> dict[str, int]:
        return self.setting["size"]

    def getOutputColor(self) -> dict[str, str]:
        return self.setting["output_color"]

    def getOutputPath(self) -> str:
        return self.setting["output_path"]

    def getVideoCodec(self) -> str:
        return self.setting["prefferred_video_codec"]

    def getAudioCodec(self) -> str:
        return self.setting["prefferred_audio_codec"]
