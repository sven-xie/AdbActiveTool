from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar


class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background: rgba(0, 0, 0, 120);")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setFixedWidth(200)

        # 无限加载模式
        self.progress.setRange(0, 0)

        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background: #333;
                height: 12px;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background: #3a86ff;
                border-radius: 6px;
            }
        """)

        layout.addWidget(self.progress)

    def start(self):
        self.resize(self.parent().size())
        self.show()

    def stop(self):
        self.hide()
