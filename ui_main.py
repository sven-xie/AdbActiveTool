from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox, QLabel

from active_woker import ActivateWorker
from loading import LoadingOverlay


class MainWindow(QWidget):

    def __init__(self, resource_path):
        super().__init__()

        self.resource_path = resource_path
        self.setWindowTitle("飞鸽远程控制ADB激活助手")
        self.setMinimumSize(500, 400)

        # ===== 布局 =====
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        # ===== 提示文案 =====
        self.label = QLabel("请用USB连接手机，然后一键激活按钮")
        self.label.setAlignment(Qt.AlignCenter)

        label_font = QFont()
        label_font.setPointSize(20)
        self.label.setFont(label_font)

        # ===== 按钮 =====
        self.button = QPushButton("一键激活")
        self.button.setMinimumSize(200, 80)
        self.button.clicked.connect(self.activate)

        button_font = QFont()
        button_font.setPointSize(22)
        button_font.setBold(True)
        self.button.setFont(button_font)

        # ===== 样式 =====
        self.setStyleSheet("""
                  QWidget {
                      background-color: #1e1e1e;
                  }

                  QLabel {
                      color: #ffffff;
                  }

                  QPushButton {
                      background-color: #3a86ff;
                      color: white;
                      border-radius: 40px;
                      padding-top: 15px;   
                      padding-bottom: 15px;
                  }

                  QPushButton:hover {
                      background-color: #5aa0ff;
                  }

                  QPushButton:pressed {
                      background-color: #2f6fd6;
                  }
              """)

        # 添加组件
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

        # 创建 loading 层
        self.loading = LoadingOverlay(self)
        self.loading.stop()

    def activate(self):
        # 显示 loading
        self.loading.start()
        # 启动后台线程
        self.worker = ActivateWorker(self.resource_path)
        self.worker.finished.connect(self.on_activate_finished)
        self.worker.start()

    def on_activate_finished(self, success, msg):
        # 隐藏 loading
        self.loading.stop()
        # 弹出结果
        if success:
            self.label.setText("恭喜你，您的手机ADB已激活成功")
            self.show_message("激活成功", msg)
        else:
            self.label.setText("请用USB连接手机，然后一键激活按钮")
            self.show_message("激活失败", msg)

    def show_message(self, title, text):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)

        msg.setStyleSheet("""
            QMessageBox {
                border-radius: 12px;
            }
            QLabel {
                color: white;
                font-size: 16px;
                padding: 15px;
                qproperty-alignment: AlignCenter;
            }
            QPushButton {
                background-color: #3a86ff;
                color: white;
                border-radius: 8px;
                min-width: 90px;
                min-height: 36px;
                font-size: 14px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #5aa0ff;
            }
        """)

        msg.exec()
