import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import button
class App(QWidget):

    border = 20

    # initialized value before runs application
    def __init__(self):
        super().__init__()
        self.screen_width = 1366
        self.screen_height = 768
        self.title = "Calculator"
        self.app_width = 400
        self.app_height = 600
        self.initial_x = (self.screen_width - self.app_width)//2
        self.initial_y = (self.screen_height - self.app_height)//2
        self.font_size = 30
        self.init_gui()
    
    def init_gui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.initial_x, self.initial_y, self.app_width, self.app_height)
        self.create_textbox()
        self.create_button()
        self.set_button_name()
        self.show()

    def create_textbox(self):    
        self.textbox = QLineEdit(self)
        self.textbox.move(App.border,App.border)
        self.textbox_width = self.app_width - 2*App.border
        self.textbox_height = (1/4)*self.app_height
        self.textbox.resize(self.textbox_width,self.textbox_height)
        self.textbox.setFont(QFont('Comic Sans MS',self.font_size))

    def create_button(self):
        self.group_button_x = self.border
        self.group_button_y = self.textbox_height + 2*self.border
        self.location_button = []
        self.rows = 5
        self.columns = 5
        self.scale_x = (self.app_width - 2*self.border)//self.rows
        self.scale_y = (self.app_height - self.textbox_height - 3*self.border)//self.columns
        for column in range(self.columns):
            for row in range(self.rows):
                x = self.group_button_x + (row * self.scale_x)
                y = self.group_button_y + (column * self.scale_y)
                self.button = QPushButton("",self)
                self.button.move(x,y)
                self.button.resize(self.scale_x,self.scale_y)
                self.location_button.append(self.button)
    def set_button_name(self):
        self.button_fontsize = self.scale_y//4
        self.button_font = QFont('Comic Sans MS',self.button_fontsize)
        self.button_text = button.all_button_name()
        print(self.button_text)
        for item,button_name in zip(self.location_button,self.button_text) :
            item.setText(button_name)
            item.setFont(self.button_font)
    
def run_app():
    print(sys.argv)
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

run_app()
