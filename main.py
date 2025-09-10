from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
import sys
from os import path
from MainUi_func import Ui_MainFunc

def load_stylesheet(stylesheet_path: str) -> str:
    if not path.exists(stylesheet_path):
        return ""
    with open(stylesheet_path, "r", encoding='utf-8') as f:
        return f.read()

def main():
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(":/Cubic_11.ttf")
    ui = Ui_MainFunc()
    ui.show()
    app.setStyleSheet(load_stylesheet("styles.qss"))
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
