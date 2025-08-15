from OptionsDialog_ui import Ui_OptionDialog
from PySide6.QtWidgets import QMainWindow
from Config import Config


class Ui_OptionFunc(QMainWindow, Ui_OptionDialog):
    def __init__(self, parent=None, config: Config = None):
        super(Ui_OptionFunc, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("選項設定")
        self.config = config
        self.videolist = ["avc1", "vp09", "av01"]
        self.audiolist = ["mp4a", "opus"]

        self.cmbPreferVideo.addItems(self.videolist)
        self.cmbPreferAudio.addItems(self.audiolist)

        self.cmbPreferVideo.setCurrentIndex(self.videolist.index(config.video_codec))
        self.cmbPreferAudio.setCurrentIndex(self.audiolist.index(config.audio_codec))
        self.txtOutputFileNameTemplate.setText(config.default_output_filename_template)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accept(self):
        self.config.default_output_filename_template = self.txtOutputFileNameTemplate.text()
        self.config.video_codec = self.cmbPreferVideo.currentText()
        self.config.audio_codec = self.cmbPreferAudio.currentText()
        self.config.save()
        self.close()

    def reject(self):
        self.close()
