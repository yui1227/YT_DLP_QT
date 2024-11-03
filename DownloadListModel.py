from PySide6.QtCore import (
    QAbstractTableModel,
    QPersistentModelIndex,
    Qt,
    QModelIndex,
    SIGNAL,
)

from DownloadItem import DownloadItem

TITLE, URL, VCODEC, ACODEC, STATUS, PROGRESS, ETA, SPEED, ISLIVE = range(9)


class DownloadListModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(DownloadListModel, self).__init__(parent)
        self._data: list[DownloadItem] = []
        self.columns = [
            "標題",
            "網址",
            "影片格式",
            "音訊格式",
            "狀態",
            "進度",
            "剩餘時間",
            "下載速度",
            "直播"
        ]

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
        return 9

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
            elif index.column() == STATUS:
                return self._data[row].Status
            elif index.column() == PROGRESS:
                if self._data[row].Progress == -1:
                    return "未知"
                return f"{self._data[row].Progress:.1f}%"
            elif index.column() == ETA:
                return self._data[row].ETA
            elif index.column() == SPEED:
                return self._data[row].Speed
            elif index.column() == ISLIVE:
                return "是" if self._data[row].IsLive else "否"

        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.EditRole:
            item = self._data[index.row()]
            if index.column() == VCODEC:
                item.SelectedVideoFormat = item.reverse_vfDict[value]
            elif index.column() == ACODEC:
                item.SelectedAudioFormat = item.reverse_afDict[value]
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            return True
        return False

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
