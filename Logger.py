from PySide6.QtCore import Signal,QObject
class Logger(QObject):
    log = Signal(str)
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.log.emit(f'''<span style='color:aqua'>{msg}</span>''')

    def info(self, msg):
        self.log.emit(f'''<span style='color:aqua'>{msg}</span>''')

    def warning(self, msg):
        self.log.emit(f'''<span style='color:orange'>{msg}</span>''')

    def error(self, msg):
        self.log.emit(f'''<span style='color:red'>{msg}</span>''')
