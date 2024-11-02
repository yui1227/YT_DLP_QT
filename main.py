from PySide6.QtWidgets import QApplication
import sys
from MainUi_func import Ui_MainFunc


def main():
    app = QApplication(sys.argv)
    ui = Ui_MainFunc()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
