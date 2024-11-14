import json
import os


class Config:
    CONFIG_FILENAME = "ytdlpqt.json"
    DEFAULT_DICT = {
        "default_output_format": "%(title)s [%(id)s].%(ext)s",
        "columns_width": [100] * 9,
        "output_templates": {"default": "%(title)s [%(id)s].%(ext)s"},
        "size": {"width": 1200, "height": 630},
        "output_color": {
            "info": "aqua",
            "warning": "orange",
            "error": "red",
        },
        "output_path":""
    }

    def __init__(self) -> None:
        if not os.path.isfile(self.CONFIG_FILENAME):
            with open(self.CONFIG_FILENAME, mode="w", encoding="utf-8") as f:
                json.dump(self.DEFAULT_DICT, f, ensure_ascii=False,indent=4)
        with open(self.CONFIG_FILENAME, mode="r", encoding="utf-8") as f:
            self.setting = json.load(f)

    def getDefaultOutputFormat(self):
        return self.setting["default_output_format"]

    def getColumnsWidth(self):
        return self.setting["columns_width"]

    def getOutputTemplates(self):
        return self.setting["output_templates"]

    def getSize(self):
        return self.setting["size"]

    def getOutputColor(self):
        return self.setting["output_color"]
    
    def getOutputPath(self):
        return self.setting["output_path"]
