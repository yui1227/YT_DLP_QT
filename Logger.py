from PySide6.QtCore import Signal, QObject


class Logger(QObject):
    log = Signal(str)

    def __init__(self, color_dict: dict[str, str], parent=None) -> None:
        super(Logger, self).__init__(parent)
        self.color_dict = color_dict

    def debug(self, msg: str):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith("[debug] "):
            pass
        else:
            self.log.emit(
                f"""<span style='color:{self.color_dict["info"]}'>{msg}</span>"""
            )

    def info(self, msg):
        self.log.emit(f"""<span style='color:{self.color_dict["info"]}'>{msg}</span>""")

    def warning(self, msg):
        self.log.emit(
            f"""<span style='color:{self.color_dict["warning"]}'>{msg}</span>"""
        )

    def error(self, msg):
        self.log.emit(
            f"""<span style='color:{self.color_dict["error"]}'>{msg}</span>"""
        )
