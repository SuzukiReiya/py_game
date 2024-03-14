import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit

class ExampleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # レイアウトの設定
        layout = QVBoxLayout()

        # テキストボックスの作成
        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox)

        # ボタンの作成
        self.button = QPushButton('表示', self)
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)

        # 出力用テキストボックスの作成
        self.output_textbox = QLineEdit(self)
        self.output_textbox.setReadOnly(True)  # 編集不可に設定
        layout.addWidget(self.output_textbox)

        self.setLayout(layout)
        self.setWindowTitle('PyQt Example')

    def on_click(self):
        input_text = self.textbox.text()
        self.output_textbox.setText(input_text)

    def keyPressEvent(self, event):
        # キーの文字を表示
        print("Pressed:", event.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleApp()
    ex.show()
    sys.exit(app.exec_())

