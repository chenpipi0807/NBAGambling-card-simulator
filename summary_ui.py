# summary_ui.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt5.QtGui import QPalette, QPixmap, QBrush, QFont
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

class SummaryUI(QWidget):
    def __init__(self, on_retry):
        super().__init__()
        self.on_retry = on_retry
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(50, 50, 50, 50)  # 设置边距
        self.layout.setSpacing(20)  # 设置控件间距
        self.setLayout(self.layout)

    def show_summary(self, total_attempts, total_successes):
        self.clear_layout()

        set_background(self, resource_path('END.png'))  # 更换背景图
        success_rate = (total_successes / total_attempts) * 100 if total_attempts > 0 else 0

        # 创建结算信息的标签
        summary_info = f"""
        结算信息：
        赌卡次数: {total_attempts} 次
        赌卡成功数: {total_successes} 次
        赌卡成功率: {success_rate:.2f}%
        """
        
        # 解锁称号
        title = self.get_title(success_rate)

        # 创建一个半透明的方框
        summary_label = QLabel(summary_info)
        summary_label.setAlignment(Qt.AlignCenter)
        summary_label.setFont(QFont('Arial', 18, QFont.Bold))  # 加粗字体
        summary_label.setStyleSheet("color: #FFFFFF; background-color: rgba(0, 0, 0, 180); padding: 15px; border-radius: 15px;")

        title_label = QLabel(f"解锁称号: {title}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 18, QFont.Bold))  # 加粗字体
        title_label.setStyleSheet("color: #FFFFFF; background-color: rgba(0, 0, 0, 180); padding: 15px; border-radius: 15px;")

        retry_button = QPushButton('老子不服')
        retry_button.setStyleSheet(""" 
            QPushButton {
                font-size: 22px;
                padding: 20px;
                background-color: #FF5722;
                color: white;
                border-radius: 15px;
                min-width: 300px;
                max-width: 300px;
            }
            QPushButton:pressed {
                background-color: #D84315;
            }
            QPushButton:hover {
                background-color: #E64A19;
            }
        """)
        retry_button.clicked.connect(self.on_retry)

        self.layout.addWidget(summary_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(title_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(retry_button, alignment=Qt.AlignCenter)

    def clear_layout(self):
        """清理布局中的所有控件"""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def get_title(self, success_rate):
        """根据成功率获取称号"""
        if success_rate < 20:
            return "黑脸大汉"
        elif success_rate < 40:
            return "狗运不错"
        elif success_rate < 55:
            return "天选之子"
        elif success_rate < 70:
            return "寿元战士"
        else:
            return "玩赖是吧？"
