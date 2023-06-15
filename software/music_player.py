import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QSlider, QLabel, QVBoxLayout, QWidget, \
    QAction, QMenuBar, QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtCore import Qt, QUrl


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建音乐播放器和音乐列表
        self.player = QMediaPlayer(self)
        self.playlist = QMediaPlaylist(self)

        # 创建音乐列表控件
        self.music_list = QListWidget()

        # 创建滑动条和标签
        self.progress_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_label = QLabel("音量:")

        # 创建按钮
        self.play_button = QPushButton("播放")
        self.pause_button = QPushButton("暂停")
        self.stop_button = QPushButton("停止")
        self.previous_button = QPushButton("上一首")
        self.next_button = QPushButton("下一首")

        # 创建当前播放歌曲标签
        self.current_song_label = QLabel("当前播放：")

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.music_list)
        layout.addWidget(self.progress_slider)
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)
        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.previous_button)
        layout.addWidget(self.next_button)
        layout.addWidget(self.current_song_label)

        # 创建主窗口
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # 创建菜单栏
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # 创建菜单和动作
        file_menu = self.menu_bar.addMenu("文件")
        open_action = QAction("导入音乐", self)
        file_menu.addAction(open_action)
        open_action.triggered.connect(self.open_files)

        # 创建音乐播放器的相关信号和槽函数
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.player.mediaStatusChanged.connect(self.update_current_song)
        self.player.mediaChanged.connect(self.update_current_song)

        # 连接按钮的点击信号到槽函数
        self.play_button.clicked.connect(self.player.play)
        self.pause_button.clicked.connect(self.player.pause)
        self.stop_button.clicked.connect(self.player.stop)
        self.previous_button.clicked.connect(self.previous_song)
        self.next_button.clicked.connect(self.next_song)

        # 连接音乐列表的双击信号到槽函数
        self.music_list.itemDoubleClicked.connect(self.handle_double_click)

        # 连接滑动条的值改变信号到槽函数
        self.progress_slider.sliderMoved.connect(self.set_position)
        self.volume_slider.valueChanged.connect(self.set_volume)

        # 设置音乐播放器默认音量和循环模式
        self.player.setVolume(50)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

    def open_files(self):
        # 打开文件选择对话框，选择音乐文件
        files, _ = QFileDialog.getOpenFileNames(self, "选择音乐文件", "", "音频文件 (*.mp3 *.wav)")
        if files:
            # 将选择的音乐文件添加到音乐列表中
            for file in files:
                url = QUrl.fromLocalFile(file)
                content = QMediaContent(url)
                self.playlist.addMedia(content)

                # 获取音乐文件的名称并显示在列表中
                music_name = file.split("/")[-1]
                self.music_list.addItem(music_name)

            # 设置音乐列表为当前播放列表
            self.player.setPlaylist(self.playlist)

    def handle_double_click(self, item):
        # 处理音乐列表的双击事件
        index = self.music_list.row(item)
        self.playlist.setCurrentIndex(index)
        self.player.play()

    def update_position(self, position):
        # 更新音乐播放进度
        self.progress_slider.setValue(position)

    def update_duration(self, duration):
        # 更新音乐总时长
        self.progress_slider.setMaximum(duration)

    def set_position(self, position):
        # 设置音乐播放位置
        self.player.setPosition(position)

    def set_volume(self, volume):
        # 设置音量
        self.player.setVolume(volume)

    def update_current_song(self, status):
        # 更新当前播放歌曲标签
        if status == QMediaPlayer.LoadedMedia:
            index = self.playlist.currentIndex()
            item = self.music_list.item(index)
            if item:
                self.current_song_label.setText(f"当前播放：{item.text().split('.')[0]}")

    def previous_song(self):
        # 上一首
        current_index = self.playlist.currentIndex()
        if current_index > 0:
            self.playlist.previous()
            self.player.play()

    def next_song(self):
        # 下一首
        current_index = self.playlist.currentIndex()
        if current_index < self.playlist.mediaCount() - 1:
            self.playlist.next()
            self.player.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
