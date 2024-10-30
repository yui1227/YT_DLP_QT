from PySide6.QtWidgets import QApplication
import sys
import yt_dlp
import json
from MainUi_func import Ui_MainFunc

def main():
    app=QApplication(sys.argv)
    ui=Ui_MainFunc()
    ui.show()
    sys.exit(app.exec())
    # url='https://www.youtube.com/watch?v=8YNzp2vRS9I'
    # with yt_dlp.YoutubeDL() as ytdlp:
    #     info=ytdlp.extract_info(url,download=False)
    #     with open('info.json',mode='w',encoding='utf-8') as f:
    #         json.dump(ytdlp.sanitize_info(info),f,ensure_ascii=False)


if __name__=='__main__':
    main()