import sys
from urllib.request import urlopen, Request
from lxml import etree
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QMenu, QAction, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy


# 爬取网页内容
url = "http://resou.today/art/11.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'Referer': 'http://www.example.com'
}
req = Request(url, headers=headers)
html = urlopen(req).read()

# 使用lxml解析HTML
parser = etree.HTMLParser()
tree = etree.HTML(html)

# 提取<span>标签内容
span_tags = tree.xpath('//span/text()')

# 创建应用程序
app = QApplication(sys.argv)
widget = QWidget()
widget.resize(800, 800)  # 设置窗口大小为800x800

# 创建布局
layout = QVBoxLayout(widget)

# 创建列表小部件
list_widget = QListWidget()
list_widget.setSizePolicy(
    QSizePolicy.Expanding, QSizePolicy.Expanding
)  # 设置列表大小策略为铺满窗口

# 设置字体大小
font = QFont()
font.setPointSize(28)

# 将<span>标签内容添加到列表中
for span in span_tags:
    item = QListWidgetItem(span)
    item.setFont(font)  # 设置字体大小
    item.setFlags(item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    list_widget.addItem(item)

# 右键菜单的复制操作
def copy_selected_item():
    selected_items = list_widget.selectedItems()
    if selected_items:
        text = selected_items[0].text()
        clipboard = QApplication.instance().clipboard()
        clipboard.setText(text)

# 创建右键菜单
def show_context_menu(position):
    menu = QMenu()
    copy_action = QAction("复制", menu)
    copy_action.triggered.connect(copy_selected_item)
    menu.addAction(copy_action)

    if list_widget.selectedItems():
        menu.exec_(list_widget.viewport().mapToGlobal(position))

# 将右键菜单绑定到列表小部件上
list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
list_widget.customContextMenuRequested.connect(show_context_menu)

# 将列表小部件添加到布局中
layout.addWidget(list_widget)

# 显示窗口
widget.show()
sys.exit(app.exec_())
