
# 編輯UI
`uv run pyside6-designer .\MainUi.ui`

# 把ui檔案轉成python檔案
`uv run pyside6-uic .\MainUi.ui -o MainUi_ui.py`

# 把資源檔編譯成python檔案
`uv run pyside6-rcc resource.qrc -o resource_rc.py`

# 打包成exe
`uv run pyinstaller main.py -i ./resources/frog_icon_removed_bg.ico -w -F -n YT_DLP_QT`
