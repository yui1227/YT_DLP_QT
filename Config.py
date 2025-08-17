import json
import os


class Config:
    CONFIG_FILENAME = "ytdlpqt.json"
    DEFAULT_DICT = {
        "default_output_filename_template": "%(title)s.%(ext)s",
        "columns_state": None,
        # "size": {"width": 1200, "height": 630},
        "output_color": {
            "info": "aqua",
            "warning": "orange",
            "error": "red",
        },
        "output_path": "",
        "prefferred_video_codec": "avc1",
        "prefferred_audio_codec": "mp4a",
    }

    def __init__(self) -> None:
        if not os.path.isfile(self.CONFIG_FILENAME):
            with open(self.CONFIG_FILENAME, mode="w", encoding="utf-8") as f:
                json.dump(self.DEFAULT_DICT, f, ensure_ascii=False, indent=4)
        with open(self.CONFIG_FILENAME, mode="r", encoding="utf-8") as f:
            # 補上後來新加的設定
            self.setting = self.DEFAULT_DICT | json.load(f)

    def save(self):
        with open(self.CONFIG_FILENAME, mode="w", encoding="utf-8") as f:
            json.dump(self.setting, f, ensure_ascii=False, indent=4)

    @property
    def default_output_filename_template(self) -> str:
        return self.setting["default_output_filename_template"]
    
    @default_output_filename_template.setter
    def default_output_filename_template(self, value: str):
        self.setting["default_output_filename_template"] = value

    @property
    def columns_state(self) -> str | None:
        return self.setting["columns_state"]
    
    @columns_state.setter
    def columns_state(self, value: str):
        self.setting["columns_state"] = value

    @property
    def size(self) -> dict[str, int]:
        return self.setting["size"]
    
    @size.setter
    def size(self, value: dict[str, int]):
        self.setting["size"] = value

    @property
    def output_color(self) -> dict[str, str]:
        return self.setting["output_color"]

    @property
    def output_path(self) -> str:
        return self.setting["output_path"]
    
    @output_path.setter
    def output_path(self, value: str):
        self.setting["output_path"] = value

    @property
    def video_codec(self) -> str:
        return self.setting["prefferred_video_codec"]
    
    @video_codec.setter
    def video_codec(self, value: str):
        self.setting["prefferred_video_codec"] = value

    @property
    def audio_codec(self) -> str:
        return self.setting["prefferred_audio_codec"]
    
    @audio_codec.setter
    def audio_codec(self, value: str):
        self.setting["prefferred_audio_codec"] = value
