from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

class EventListener(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def event(self, event):
        # 记录事件类型
        print(f"Event: {event.type()}")

        # 处理特定事件
        if event.type() == event.Show:
            print("Widget is shown.")
        elif event.type() == event.Hide:
            print("Widget is hidden.")
        elif event.type() == event.Resize:
            print(f"Widget resized to: {self.size()}")

        return super().event(event)