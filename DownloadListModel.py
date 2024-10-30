from PySide6.QtCore import QAbstractTableModel ,Qt

from DownloadItem import DownloadItem


class DownloadListModel(QAbstractTableModel):
    def __init__(self):
        super(DownloadListModel, self).__init__()
        self._data: list[DownloadItem] = []
        self.columns = ['標題','網址','影片格式','音訊格式']

    def headerData(self, section, orientation, role = ...):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]
        
        return super().headerData(section, orientation, role)

    def rowCount(self,index):
        return len(self._data)
    
    def columnCount(self,index):
        return 4
    
    def data(self, index, role = ...):
        if not index.isValid():
            return None
        
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            if index.column() == 0:
                return self._data[row].Title
            elif index.column() == 1:
                return self._data[row].Url
            elif index.column() == 2:
                return self._data[row].VideoFormat
            elif index.column() == 3:
                return self._data[row].AudioFormat
        return None

            