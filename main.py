import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from start_ui import StartUI
from main_game import MainGameUI
from summary_ui import SummaryUI
import os

def resource_path(relative_path):
    """获取资源的绝对路径，适用于开发和打包后"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.start_ui = StartUI(self.start_game)
        self.main_game_ui = MainGameUI(self.show_summary)
        self.summary_ui = SummaryUI(self.restart_game)

        self.addWidget(self.start_ui)
        self.addWidget(self.main_game_ui)
        self.addWidget(self.summary_ui)

        self.setCurrentWidget(self.start_ui)
        self.setFixedSize(960, 452)

    def start_game(self):
        self.main_game_ui.reset_game()  # 重置游戏状态
        self.setCurrentWidget(self.main_game_ui)

    def show_summary(self, total_attempts, total_successes):
        self.summary_ui.show_summary(total_attempts, total_successes)
        self.setCurrentWidget(self.summary_ui)

    def restart_game(self):
        self.start_game()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("赌卡模拟器")  # 设置任务栏显示名称
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

# 使用 resource_path 函数来加载图像
set_background(self, resource_path('END.png'))
