import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class Worker(QObject):
    finished = pyqtSignal()
    
    def run(self):
        while True:
            print("Worker thread is running...")
            time.sleep(1)  # 何らかのタスクを実行
            # イベントやタスクを処理

class ExampleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.startWorkerThread()

    def initUI(self):
        # レイアウトの設定
        layout = QVBoxLayout()

        # ボタンの作成
        self.button = QPushButton('ボタン', self)
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.setWindowTitle('Qt Thread Example')

    def startWorkerThread(self):
        # ワーカースレッドの設定
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def on_click(self):
        print("Button clicked")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleApp()
    ex.show()
    sys.exit(app.exec_())
