
# 編輯UI
`pyside6-designer.exe .\MainUi.ui`

# 把ui檔案轉成python檔案
`pyside6-uic.exe .\MainUi.ui -o MainUi_ui.py`

# 把資源檔編譯成python檔案
`pyside6-rcc resource.qrc -o resource_rc.py`

# 打包成exe
`pyinstaller -i .\frog_icon_removed_bg.ico -w -F main.py`
