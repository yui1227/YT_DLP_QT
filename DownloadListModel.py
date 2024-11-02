from PySide6.QtCore import QAbstractTableModel, QPersistentModelIndex, Qt, QModelIndex

from DownloadItem import DownloadItem

TITLE, URL, VCODEC, ACODEC = range(4)


class DownloadListModel(QAbstractTableModel):
    def __init__(self):
        super(DownloadListModel, self).__init__()
        self._data: list[DownloadItem] = []
        self.columns = ["標題", "網址", "影片格式", "音訊格式"]

    def headerData(self, section, orientation, role=...):
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return self.columns[section]

        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return 4

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        if index.column() == VCODEC or index.column() == ACODEC:
            return Qt.ItemFlag(
                QAbstractTableModel.flags(self, index) | Qt.ItemFlag.ItemIsEditable
            )
        else:
            return Qt.ItemFlag(QAbstractTableModel.flags(self, index))

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            if index.column() == TITLE:
                return self._data[row].Title
            elif index.column() == URL:
                return self._data[row].Url
            elif index.column() == VCODEC:
                return self._data[row].SelectedVideoFormat
            elif index.column() == ACODEC:
                return self._data[row].SelectedAudioFormat
        return None

    def insertRows(self, position, data: DownloadItem, index=QModelIndex()):
        self.beginInsertRows(index, position, position)
        self._data.append(data)
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent=QModelIndex()):
        if row < 0 or row > len(self._data) - 1:
            return
        self.beginRemoveRows(parent, row, row + count - 1)
        self._data.remove(self._data[row])
        self.endRemoveRows()
        return True
