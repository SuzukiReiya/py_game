import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtGui import QFont

GUI_WIN_WDTH  = 330
GUI_WIN_HIGHT = 400

CD_BCK_GRND  = " "
CD_BRCK      = "="
CD_PLYR      = "P"
CD_BMB       = "O"
CD_FAIR      = "*"
OUT_STR_COLS = 20
OUT_STR_ROWS = 20

MD_STG_PLY    = 0x10
MD_STG_SLCT   = 0x20

class ExampleApp(QWidget):
    out_str = [["" for _ in range(OUT_STR_COLS)] for _ in range(OUT_STR_ROWS) ]

    stage_level = 1
    mode = MD_STG_PLY

    plyr_col = 0
    plyr_row = 0
    
    #等間隔フォント定義
    monospaceFont = QFont("Mnonospace")
    monospaceFont.setStyleHint(QFont.Monospace)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # レイアウトの設定
        layout = QVBoxLayout()

        # ボタンの作成
        self.button = QPushButton('リセット', self)
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)

        # ボタンの作成
        self.button2 = QPushButton('リブート', self)
        self.button2.clicked.connect(self.on_click)
        layout.addWidget(self.button2)

        # 出力用テキストボックスの作成
        self.output_textbox = QTextEdit(self)
        self.output_textbox.setReadOnly(True)  # 編集不可に設定
        layout.addWidget(self.output_textbox)

        self.setLayout(layout)

        self.resize(GUI_WIN_WDTH,GUI_WIN_HIGHT)
        self.setWindowTitle('Example App')

    def reset (self) :
        self.resize(GUI_WIN_WDTH,GUI_WIN_HIGHT)
        self.stage_level = 1


    def add_space (self, out_one_str) :
        out_one_str_spc = ' '.join(out_one_str)
        out_one_str_spc = ' ' + out_one_str_spc
        return out_one_str_spc

    
    def set_text_box (self, output_textbox, out_one_str) :
        output_textbox.setFont(self.monospaceFont)
        out_one_str_tmp = self.add_space (out_one_str)
        output_textbox.setText(out_one_str_tmp)
        output_textbox.show()
        print("txt show")

    def create_out_one_str(self, out_str):
        out_one_str = '\n'.join(''.join(row) for row in out_str)
        # print (out_one_str)
        return out_one_str
    
    def  parse_field_file (self, file_name):
        read_str = [["" for _ in range(OUT_STR_COLS)] for _ in range(OUT_STR_ROWS) ]
        with open(file_name, 'r') as file :
            for i in range(0,OUT_STR_COLS) :
                line = file.readline().strip('\n')  # 行末の改行文字のみを除去
                characters = []
                num_rows = 0
                for char in line:
                    characters.append(char)
                    if char == 'P' :
                        plyr_col = i
                        plyr_row = num_rows
                        print(str((plyr_col,plyr_row)))
                    num_rows += 1
                # print(characters)
                read_str[i][:] = characters
        return read_str, (plyr_col,plyr_row)

    def set_out_str_to_txt_box(self, out_str) :
        out_one_str = self.create_out_one_str(out_str)
        self.set_text_box(self.output_textbox, out_one_str)
        # print(self.out_str)
    
    def on_click(self):
        self.reset()
        stage_level_str = f"{self.stage_level:02d}"
        file_name = f"./data/field/{stage_level_str}.txt"
        self.out_str, (self.plyr_col, self.plyr_row) = self.parse_field_file(file_name)
        self.set_out_str_to_txt_box(self.out_str)

    def resizeEvent(self, event):
        new_size = event.size()
        width = new_size.width()
        height = new_size.height()
        print(f"Width: {width}, Height: {height}")

        super().resizeEvent(event)

    def req_mv_plyr( self, plyr_pos, dst_pos) :
        dst_char = self.get_char_from_out_str(dst_pos)
        if dst_char == CD_BCK_GRND :
            self.mv_obj(plyr_pos, dst_pos)
            self.set_plyr_pos(dst_pos)
            
    
    def get_plyr_pos (self):
        return (self.plyr_col, self.plyr_row)

    def set_plyr_pos (self, set_pos) :
        (self.plyr_col, self.plyr_row) = set_pos
    
    def get_char_from_out_str (self,obj_pos ) :
        (obj_col, obj_row) = obj_pos
        return self.out_str[obj_col][obj_row]
    
    def set_char_from_out_str (self,obj_pos, char ) :
        (obj_col, obj_row) = obj_pos
        self.out_str[obj_col][obj_row] = char

    def mv_obj( self, obj_pos, dst_pos ) :
        char = self.get_char_from_out_str(obj_pos)
        self.set_char_from_out_str(obj_pos,CD_BCK_GRND)
        self.set_char_from_out_str(dst_pos,char)
        self.set_out_str_to_txt_box(self.out_str)

    def keyPressEvent(self, event):
        # キーの文字を表示
        key = event.text()
        print("Pressed:", key)
        if (self.mode == MD_STG_PLY) :
            if (key == 'w') :
                (plyr_col, plyr_row) = self.get_plyr_pos()
                self.req_mv_plyr((plyr_col, plyr_row), (plyr_col-1, plyr_row))
            elif (key == 's') :
                (plyr_col, plyr_row) = self.get_plyr_pos()
                self.req_mv_plyr((plyr_col, plyr_row), (plyr_col+1, plyr_row))
            elif (key == 'a') :
                (plyr_col, plyr_row) = self.get_plyr_pos()
                self.req_mv_plyr((plyr_col, plyr_row), (plyr_col, plyr_row-1))
            elif (key == 'd') :
                (plyr_col, plyr_row) = self.get_plyr_pos()
                self.req_mv_plyr((plyr_col, plyr_row), (plyr_col, plyr_row+1))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleApp()
    ex.show()
    sys.exit(app.exec_())

