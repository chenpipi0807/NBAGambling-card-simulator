import random
import os
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QPixmap, QBrush
from event_listener import EventListener  # 导入事件监听器

# 自定义滑块类
class CustomSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 计算点击位置对应的值
            value = self.minimum() + (self.maximum() - self.minimum()) * event.x() / self.width()
            self.setValue(round(value))
        super().mousePressEvent(event)

def set_background(widget, image_path):
    """设置背景图像"""
    palette = QPalette()
    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        print(f"Failed to load image: {image_path}")
    else:
        scaled_pixmap = pixmap.scaled(widget.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)

def resource_path(relative_path):
    """获取资源的绝对路径，适用于开发和打包后"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class MainGameUI(EventListener):
    def __init__(self, show_summary_callback):
        super().__init__()
        self.show_summary_callback = show_summary_callback
        self.layout = QVBoxLayout()  # 初始化布局
        self.setLayout(self.layout)  # 设置布局
        self.points_label = QLabel()  # 初始化积分标签
        self.result_button = None  # 初始化结果按钮
        self.reset_game()  # 初始化游戏状态

    def reset_game(self):
        """重置游戏状态"""
        self.points = 100  # 重置积分为100
        self.total_attempts = 0  # 重置尝试次数
        self.total_successes = 0  # 重置成功次数
        self.show_purchase_interface()  # 显示购买界面

    def clear_layout(self):
        """清理布局中的所有控件，但保留关键控件"""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget() and child.widget() not in [self.points_label]:
                child.widget().deleteLater()

    def show_purchase_interface(self):
        """显示购买界面，包括滑块、当前积分和合成按钮"""
        print("显示购买界面")  # 调试输出
        set_background(self, resource_path('BUY.png'))  # 设置买界面的背景

        # 清理布局
        self.clear_layout()

        # 隐藏结果按钮
        if self.result_button:
            self.result_button.hide()

        # 更新积分标签文本
        self.points_label.setText(f'当前积分: {self.points}')
        self.points_label.setAlignment(Qt.AlignRight)  # 右对齐
        self.points_label.setStyleSheet("color: #00FF00; font-size: 24px;")
        self.layout.addWidget(self.points_label)  # 使用布局管理器

        # 创建主卡滑块
        self.card1_slider = CustomSlider(Qt.Horizontal, self)
        self.card1_slider.setRange(1, 6)
        self.card1_slider.setValue(1)
        self.card1_slider.setFixedWidth(500)
        self.card1_slider.valueChanged.connect(self.update_labels)
        self.layout.addWidget(self.card1_slider, alignment=Qt.AlignCenter)  # 居中

        self.card1_label = QLabel(f'主卡等级: {self.card1_slider.value()}', self)
        self.card1_label.setAlignment(Qt.AlignCenter)
        self.card1_label.setStyleSheet("color: #00FF00; font-size: 20px;")
        self.layout.addWidget(self.card1_label, alignment=Qt.AlignCenter)  # 居中

        # 创建副卡滑块
        self.card2_slider = CustomSlider(Qt.Horizontal, self)
        self.card2_slider.setRange(1, 6)
        self.card2_slider.setValue(1)
        self.card2_slider.setFixedWidth(500)
        self.card2_slider.valueChanged.connect(self.update_labels)
        self.layout.addWidget(self.card2_slider, alignment=Qt.AlignCenter)  # 居中

        self.card2_label = QLabel(f'副卡等级: {self.card2_slider.value()}', self)
        self.card2_label.setAlignment(Qt.AlignCenter)
        self.card2_label.setStyleSheet("color: #00FF00; font-size: 20px;")
        self.layout.addWidget(self.card2_label, alignment=Qt.AlignCenter)  # 居中

        # 合成按钮
        self.combine_button = QPushButton('合成', self)
        self.combine_button.setFixedWidth(300)
        self.combine_button.setFixedHeight(60)
        self.combine_button.clicked.connect(self.on_combine)
        self.layout.addWidget(self.combine_button, alignment=Qt.AlignCenter)  # 居中

    def update_labels(self):
        """更新滑块对应的标签"""
        self.card1_label.setText(f'主卡等级: {self.card1_slider.value()}')
        self.card2_label.setText(f'副卡等级: {self.card2_slider.value()}')

    def on_combine(self):
        """处理合成按钮点击���件"""
        card1_level = self.card1_slider.value()
        card2_level = self.card2_slider.value()

        # 计算消耗和奖励积分
        cost = min(card1_level, card2_level)  # 固定消耗积分为最低等级
        reward = max(card1_level, card2_level)  # 成功奖励积分为最高等级

        # 检查积分是否足够
        if self.points <= 2:
            print("积分不足，游戏失败。")  # 添加调试信息
            self.show_summary()  # 跳转到结算界面
            return

        self.points -= cost  # 减去消耗的积分
        self.total_attempts += 1
        result = self.combine_cards(card1_level, card2_level)

        if result:
            self.points += reward  # 合成成功，增加奖励积分
            self.total_successes += 1  # 更新成功次数

        # 更新积分标签
        self.points_label.setText(f'当前积分: {self.points}')  # 更新积分显示

        # 隐藏滑块和标签
        self.card1_slider.hide()
        self.card2_slider.hide()
        self.card1_label.hide()
        self.card2_label.hide()

        print("主卡滑块和副卡滑块已隐藏。")  # 记录隐藏状态

        # 跳转到合成结果界面
        self.show_combination_result(result)

    def show_combination_result(self, result):
        """显示合成结果界面"""
        self.clear_layout()  # 清理布局

        # 根据合成结果设置按钮文本和背景
        max_level = max(self.card1_slider.value(), self.card2_slider.value())
        if result:
            self.result_button = QPushButton('趁热打铁', self)
            set_background(self, resource_path(f'C{max_level + 1}.png'))  # 合成成功背景
        else:
            self.result_button = QPushButton('下次必成', self)
            set_background(self, resource_path(f'B{max_level}.png'))  # 合成失败背景

        self.result_button.setFixedWidth(300)
        self.result_button.setFixedHeight(60)
        self.result_button.move(500, 300)  # 根据需要调整坐标
        self.result_button.clicked.connect(self.show_purchase_interface)  # 返回购买界面
        self.result_button.show()

        # 确保积分标签在合成结果界面中显示
        self.points_label.show()  # 确保积分标签在合成结果界面中显示

    def combine_cards(self, card1_level, card2_level):
        """合成卡片的逻辑"""
        if card1_level == card2_level:
            return card1_level + 1 if card1_level < 7 else None
        level_difference = abs(card1_level - card2_level)
        # 将成功率降低一半
        success_rate = {1: 25, 2: 15, 3: 10, 4: 5, 5: 1}.get(level_difference, 0)
        if random.randint(1, 100) <= success_rate:
            max_level = max(card1_level, card2_level)
            return max_level + 1 if max_level < 7 else None
        else:
            return None

    def show_summary(self):
        """显示结算界面"""
        self.show_summary_callback(self.total_attempts, self.total_successes)  # 调用回调函数显示结算界面

    def debug_button_status(self):
        """调试输出所有按钮的位置和状态"""
        print(f"积分标签位置: {self.points_label.geometry()} 显示状态: {self.points_label.isVisible()}")
        print(f"主卡滑���位置: {self.card1_slider.geometry()} 显示状态: {self.card1_slider.isVisible()}")
        print(f"主卡标签位置: {self.card1_label.geometry()} 显示状态: {self.card1_label.isVisible()}")
        print(f"副卡滑块位置: {self.card2_slider.geometry()} 显示状态: {self.card2_slider.isVisible()}")
        print(f"副卡标签位置: {self.card2_label.geometry()} 显示状态: {self.card2_label.isVisible()}")
        print(f"合成按钮位置: {self.combine_button.geometry()} 显示状态: {self.combine_button.isVisible()}")

    def print_game_status(self):
        """打印游戏状态"""
        print(f"总尝试次数: {self.total_attempts}, 成功次数: {self.total_successes}")

class StartEndUI(QWidget):
    def __init__(self, on_start_game):
        super().__init__()
        self.on_start_game = on_start_game
        self.initUI()

    def initUI(self):
        self.set_background('BUY.png')

        self.start_button = QPushButton('开始游戏', self)
        self.start_button.setStyleSheet(""" 
            QPushButton {
                font-size: 20px;
                padding: 15px;
                background-color: #FF5722;
                color: white;
                border-radius: 12px;
            }
            QPushButton:pressed {
                background-color: #D84315;
            }
            QPushButton:hover {
                background-color: #E64A19;
            }
        """)
        self.start_button.clicked.connect(self.on_start_game)
        self.start_button.setGeometry(330, 200, 300, 60)  # 设置绝对位置

    def set_background(self, image_path):
        """设置背景图像"""
        palette = QPalette()
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(960, 452, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)










