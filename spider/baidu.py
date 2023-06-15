import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QMenu, QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class WebPageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Page Viewer")
        self.setGeometry(100, 100, 800, 800)  # 设置初始窗口大小为800x800
        self.list_widget = QListWidget(self)
        self.list_widget.setFont(QFont("", 24))  # 设置列表项字体大小为24号
        self.list_widget.setWordWrap(True)  # 设置自动换行
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 始终显示垂直滚动条
        self.setCentralWidget(self.list_widget)

        self.worker = Worker()
        self.worker.finished.connect(self.populate_list)  # 绑定信号和槽函数
        self.worker.start()  # 启动工作线程

    def populate_list(self):
        items = self.worker.items
        counter = 1
        for item in items:
            text = item.text.strip()
            list_item = QListWidgetItem(f"{counter}. {text}")  # 添加序号
            self.list_widget.addItem(list_item)
            counter += 1

    def contextMenuEvent(self, event):
        # 启用右键菜单，可以复制内容
        menu = QMenu(self)
        copy_action = menu.addAction("复制")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == copy_action:
            selected_item = self.list_widget.currentItem()
            if selected_item:
                text = selected_item.text()
                # 去掉序号部分
                content = text.split('. ', 1)[1]
                clipboard = QApplication.clipboard()
                clipboard.setText(content)

class Worker(QThread):
    finished = pyqtSignal()  # 定义一个信号，用于在工作完成时发射信号

    def __init__(self):
        super().__init__()
        self.items = []

    def run(self):
        url = 'https://top.baidu.com/board?tab=realtime'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='c-single-text-ellipsis')
        self.items = items
        self.finished.emit()  # 发射信号，通知主线程工作完成

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = WebPageViewer()
    viewer.show()
    sys.exit(app.exec_())
