from PySide6.QtCore import (
    QModelIndex,
    QPersistentModelIndex,
    QSize,
    SIGNAL,
    Qt,
)
from PySide6.QtWidgets import (
    QStyleOptionViewItem,
    QStyledItemDelegate,
    QComboBox,
    QStyleOptionProgressBar,
    QApplication,
    QStyle,
    QProgressBar,
)

from DownloadListModel import DownloadListModel
from DownloadItem import DownloadItem

TITLE, URL, VCODEC, ACODEC, STATUS, PROGRESS, ETA, SPEED = range(8)


class DownloadTableDelegate(QStyledItemDelegate):
    def __init__(self, parent=None) -> None:
        super(DownloadTableDelegate, self).__init__(parent)

    def commitAndCloseEditor(self, str):
        editor = self.sender()
        if isinstance(editor, (QComboBox)):
            self.emit(SIGNAL("commitData(QWidget*)"), editor)
            self.emit(SIGNAL("closeEditor(QWidget*)"), editor)

    def setModelData(self, editor, model, index):
        if index.column() in (VCODEC, ACODEC):
            model.setData(index, editor.currentText())
        else:
            QStyledItemDelegate.setModelData(self, editor, model, index)

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        data: DownloadItem = index.model()._data[index.row()]
        if index.column() == VCODEC:
            editor.setStyleSheet("QComboBox QAbstractItemView {min-width: 600px;}")
            default_item = [
                f"""{"id":<3}\t{"檔案大小":<10}\t{"fps":<10}\t{"副檔名":<8}\t{"視訊編碼":<20}\t{"備註":<15}"""
            ]
            editor.addItems(default_item + list(data.vfDict.values()))
            disable_item = editor.model().item(0)
            disable_item.setEnabled(False)
            editor.setCurrentText(data.vfDict[text])
        elif index.column() == ACODEC:
            editor.setStyleSheet("QComboBox QAbstractItemView {min-width: 800px;}")
            default_item = [
                f"""{"id":<3}\t{"檔案大小":<20}\t{"副檔名":<4}\t{"音訊編碼":<20}\t{"備註":<15}"""
            ]
            editor.addItems(default_item + list(data.afDict.values()))
            disable_item = editor.model().item(0)
            disable_item.setEnabled(False)
            editor.setCurrentText(data.afDict[text])
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)

    def createEditor(self, parent, option, index):
        if index.column() == VCODEC:
            combobox = QComboBox(parent)
            self.connect(
                combobox,
                SIGNAL("currentTextChanged(QString&)"),
                self.commitAndCloseEditor,
            )
            return combobox
        elif index.column() == ACODEC:
            combobox = QComboBox(parent)
            self.connect(
                combobox,
                SIGNAL("currentTextChanged(QString&)"),
                self.commitAndCloseEditor,
            )
            return combobox
        else:
            return QStyledItemDelegate.createEditor(self, parent, option, index)
