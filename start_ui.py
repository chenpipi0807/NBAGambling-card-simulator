# start_ui.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPalette, QPixmap, QBrush, QPainter, QLinearGradient, QColor
from PyQt5.QtCore import Qt
import os
import sys

def resource_path(relative_path):
    """获取资源的绝对路径，适用于开发和打包后"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def set_background(widget, image_path):
    """设置背景图像"""
    palette = QPalette()
    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        print("Failed to load image.")
    else:
        scaled_pixmap = pixmap.scaled(widget.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)

class StartUI(QWidget):
    def __init__(self, on_start_game):
        super().__init__()
        self.on_start_game = on_start_game
        self.initUI()

    def initUI(self):
        set_background(self, resource_path('BASE.png'))

        self.start_button = QPushButton('开始游戏')
        self.start_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 15px;
                background-color: #FF5722;
                color: white;
                border-radius: 12px;
                min-width: 250px;
                max-width: 250px;
            }
            QPushButton:pressed {
                background-color: #D84315;
            }
            QPushButton:hover {
                background-color: #E64A19;
            }
        """)
        self.start_button.clicked.connect(self.on_start_game)

        layout = QVBoxLayout()
        layout.addSpacerItem(QSpacerItem(20, self.height() // 4 * 3, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        layout.addSpacerItem(QSpacerItem(20, self.height() // 4, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height() // 4)
        gradient.setColorAt(0, QColor(0, 0, 0, 128))  # 50% 黑色
        gradient.setColorAt(1, QColor(0, 0, 0, 0))    # 0% 黑色
        painter.fillRect(0, 0, self.width(), self.height() // 4, gradient)

        gradient = QLinearGradient(0, self.height(), 0, self.height() - self.height() // 4)
        gradient.setColorAt(0, QColor(0, 0, 0, 128))  # 50% 黑色
        gradient.setColorAt(1, QColor(0, 0, 0, 0))    # 0% 黑色
        painter.fillRect(0, self.height() - self.height() // 4, self.width(), self.height() // 4, gradient)

    def resizeEvent(self, event):
        set_background(self, resource_path('BASE.png'))
        super().resizeEvent(event)
