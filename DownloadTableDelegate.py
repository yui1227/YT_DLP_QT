from PySide6.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    QObject,
    QPersistentModelIndex,
)
from PySide6.QtWidgets import QStyledItemDelegate, QComboBox, QWidget

from DownloadListModel import DownloadListModel

TITLE, URL, VCODEC, ACODEC = range(4)


class DownloadTableDelegate(QStyledItemDelegate):
    def __init__(self, parent=None) -> None:
        super(DownloadTableDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        QStyledItemDelegate.paint(self, painter, option, index)

    def setModelData(self, editor, model, index):
        if index.column() == VCODEC:
            model._data[index.row()].SelectedVideoFormat = model._data[
                index.row()
            ].reverse_vfDict[editor.currentText()]
        elif index.column() == ACODEC:
            model._data[index.row()].SelectedAudioFormat = model._data[
                index.row()
            ].reverse_afDict[editor.currentText()]
        return QStyledItemDelegate.setModelData(self, editor, model, index)

    def createEditor(self, parent, option, index):
        model: DownloadListModel = self.parent()
        if index.column() == VCODEC:
            combobox = QComboBox(parent)
            combobox.setStyleSheet("QComboBox QAbstractItemView {min-width: 600px;}")
            default_item = [
                f"""{"id":<3}\t{"檔案大小":<10}\t{"fps":<10}\t{"副檔名":<8}\t{"視訊編碼":<20}\t{"備註":<15}"""
            ]
            combobox.addItems(
                default_item + list(model._data[index.row()].vfDict.values())
            )
            disable_item = combobox.model().item(0)
            disable_item.setEnabled(False)
            selected_format = model._data[index.row()].SelectedVideoFormat
            combobox.setCurrentText(
                model._data[index.row()].vfDict[f"{selected_format}"]
            )
            return combobox
        elif index.column() == ACODEC:
            combobox = QComboBox(parent)
            combobox.setStyleSheet("QComboBox QAbstractItemView {min-width: 800px;}")
            default_item = [
                f"""{"id":<3}\t{"檔案大小":<20}\t{"副檔名":<4}\t{"音訊編碼":<20}\t{"備註":<15}"""
            ]
            combobox.addItems(
                default_item + list(model._data[index.row()].afDict.values())
            )
            disable_item = combobox.model().item(0)
            disable_item.setEnabled(False)
            selected_format = model._data[index.row()].SelectedAudioFormat
            combobox.setCurrentText(
                model._data[index.row()].afDict[f"{selected_format}"]
            )
            return combobox
        else:
            return QStyledItemDelegate.createEditor(self, parent, option, index)
