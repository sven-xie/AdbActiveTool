import sys
import os
from PySide6.QtWidgets import QApplication
from ui_main import MainWindow

def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath("."), relative)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(resource_path)
    window.show()
    sys.exit(app.exec())