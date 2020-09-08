import sys,time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import button,input_controller,cal_part

class Textbox(QLineEdit):

    click = pyqtSignal()

    def __init__(self,parent):
        super().__init__(parent)
    def mousePressEvent(self,event:QMouseEvent):
        self.point = event.pos()
        self.click.emit()
    def get_point(self):
        return self.point

class App(QWidget):

    border = 20
    normal_font_size = 20
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
        self.font_size = 20
        self.num_sqrt,self.num_text_other_sqrt = 0,0
        self.data_storage = []
        self.no_text = True
        self.error_text = '0'
        self.init_gui()
    
    def init_gui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.initial_x, self.initial_y, self.app_width, self.app_height)
        self.create_textbox()
        self.create_button()
        self.set_button_name()
        self.show()

    def create_textbox(self):    
        self.textbox = Textbox(self)
        self.textbox.move(App.border,App.border)
        self.textbox_width = self.app_width - 2*App.border
        self.textbox_height = (1/4)*self.app_height
        self.textbox.resize(self.textbox_width,self.textbox_height)
        self.textbox.setFont(QFont('Comic Sans MS',self.font_size))
        self.textbox.setAlignment(Qt.AlignRight)
        self.textbox.click.connect(self.change_cursor_by_click)

    def create_button(self):
        #group of calculator button
        #-----------set label---------------
        self.calculator_label = QLabel("Calculator part",self)
        self.calculator_label_x = self.border
        self.calculator_label_y = self.textbox_height + 2*self.border
        self.label_width = self.textbox_width//5
        self.label_height = self.textbox_height//5
        self.calculator_label.move(self.calculator_label_x,self.calculator_label_y)
        self.calculator_label.resize(self.label_width,self.label_height)
        #--------------set calculator button------------------
        self.group_button_x = self.border
        self.group_button_y = self.calculator_label_y + self.border + self.label_height
        self.location_button = []
        self.rows = 5
        self.columns = 5
        self.scale_x = (self.app_width - 2*self.border)//self.rows
        self.scale_y = (self.app_height - self.group_button_y - self.border)//self.columns
        for column in range(self.columns):
            for row in range(self.rows):
                x = self.group_button_x + (row * self.scale_x)
                y = self.group_button_y + (column * self.scale_y)
                self.location_button.append(QPushButton("",self))
                self.location_button[-1].move(x,y)
                self.location_button[-1].resize(self.scale_x,self.scale_y)
                self.location_button[-1].clicked.connect(lambda:self.insert_text_from_button())


    def set_button_name(self):
        self.button_fontsize = self.scale_y//4
        self.button_font = QFont('Comic Sans MS',self.button_fontsize)
        self.button_text = button.all_button_name()
        for item,button_name in zip(self.location_button,self.button_text) :
            item.setText(button_name)
            item.setFont(self.button_font)
    
    def insert_text_from_button(self):
        button = self.sender()
        text = button.text()
        self.check_grammar(text)

    def check_grammar(self,text):    
        if text == 'X^n':
            text = text[1]       
        elif text == 'sqrt' :
            text += '('
        # check textbox is empty or not
        if self.no_text :
            self.value = input_controller.Check_grammar()
            value = self.value.check_case(text)
            if value is not None :
                self.no_text = False
        else:
            value = self.value.check_case(text)
        # insert dot between numeric
        if ((text == '.') and ( 0 < self.textbox.cursorPosition() < len(self.textbox.text())-1)) :
                self.check_word(self.textbox.text()[self.textbox.cursorPosition()])
        elif (text == '.') and (self.textbox.cursorPosition() == len(self.textbox.text())-1) :
            self.value.no_dot = True
        #If it is in case switch
        if value is not None :
            #Insert data into textbox
            cursor_position = self.textbox.cursorPosition()
            left_side_text = self.textbox.text()[:cursor_position]
            right_side_text = self.textbox.text()[cursor_position:]
            self.textbox.setText(left_side_text+value.data+right_side_text)
            count = self.value.check_num_square_root(self.textbox.text(),cursor_position)
            self.data_storage.insert(cursor_position-4*count,value)
            self.textbox.setFocus()
            self.textbox.setCursorPosition(cursor_position+len(value.data))
        #If it is button function or error type
        else :
            self.check_function(text)

    def check_function(self,text):
        value_type = self.value.check_type(text)
        if value_type == "Function type" :
            if text == "AC" :
                self.value.no_text = True
                self.no_text = True
                self.value.change_case("")
                self.textbox.clear()
                self.textbox.setFont(QFont('Comic Sans MS',self.normal_font_size))
                self.data_storage = []
                self.textbox.setFocus()
                self.textbox.setCursorPosition(0)
            elif text == "DEL":
                self.check_not_sqrt = True
                cursor_position = self.textbox.cursorPosition()
                # if it is some texts in textbox:
                if cursor_position - 1 >= 0 :
                    # Will it be ( or sqrt(
                    if self.textbox.text()[cursor_position-1] == '(' :
                        if cursor_position >= 5 :
                            #check if it isn't sqrt()
                            if self.textbox.text()[cursor_position-2] == 't' :
                                left_text = self.textbox.text()[:cursor_position-5]
                                self.check_not_sqrt = False
                        else:
                            left_text = self.textbox.text()[:cursor_position-1]
                    else:
                        left_text = self.textbox.text()[:cursor_position-1]
                    right_text = self.textbox.text()[cursor_position:]
                else :
                    left_text = ""
                    right_text = ""
                #find num of sqrt()
                count = self.value.check_num_square_root(self.textbox.text(),cursor_position)
                # remove data from list which it is a case and data
                try :
                    self.data_storage.pop(cursor_position-1 -4*count)
                except IndexError:
                    pass
                # sum data after delete
                self.textbox.setText(left_text+right_text)
                self.textbox.setFocus()
                # Did you delete sqrt(), It will change the cursor vary on length of character
                if self.check_not_sqrt :
                    if cursor_position != 0:
                        self.textbox.setCursorPosition(cursor_position-1)
                    else:
                        self.textbox.setCursorPosition(0)
                        self.no_text = True
                else :
                    self.textbox.setCursorPosition(cursor_position-5)
                #find case switch before cursor position
                self.find_case()    
                #check dot
                try :
                    if self.textbox.text()[self.textbox.cursorPosition()] in self.value.numeric :
                        self.check_word(self.textbox.text()[self.textbox.cursorPosition()])
                except IndexError :
                    pass
                
            elif text == '=' :
                result = self.check_final_grammar()
                if isinstance(result,(int,float)) :
                    # clear textbox and insert value
                    result = str(result)
                    self.check_function('AC')
                    for item in range(len(result)) :
                        self.check_grammar(result[item])

    def change_cursor_by_click(self):
        self.textbox.setFocus()
        self.textbox.setCursorPosition(self.textbox.cursorPositionAt(self.textbox.get_point()))
        self.find_case()

    def find_case(self):
        cursor_position = self.textbox.cursorPosition()
        if len(self.textbox.text()) > 0 :
            try :
                count = self.value.check_num_square_root(self.textbox.text(),cursor_position)
                case_input = self.data_storage[cursor_position-1-4*count].case
            except Exception :
                pass
            else:
                self.value.change_case(case_input)
    # check word that is numeric or float
    def check_word(self,word):
        left_side,right_side = True,True
        left_index,right_index = self.textbox.cursorPosition(),self.textbox.cursorPosition()
        while left_side or right_side :
            if ((self.textbox.text()[left_index] in '0123456789'  or self.textbox.text()[left_index] == '.')
                and left_index > 0):
                left_index -= 1
            else:
                left_side = False
            if ((self.textbox.text()[right_index] in '0123456789' or self.textbox.text()[right_index] == '.') 
                and right_index < len(self.textbox.text())-1):
                right_index += 1
            else:
                right_side = False
        word = self.textbox.text()[left_index:right_index]
        self.value.check_dot(word)
    # last check
    def check_final_grammar(self):
        text = self.textbox.text()
        self.old_text = text
        self.different_two_bracket = text.count('(') - text.count(')') 
        if self.different_two_bracket != 0 :
            if text.count('(') >  text.count(')') :
                self.error_value = str(self.different_two_bracket) + ' close bracket'
            else :
                self.error_value = str(self.different_two_bracket) + ' open bracket'
            self.error_text = "Miss {} ".format(self.error_value)
            self.show_error_text()
            
        else :
            result_continuous = self.value.check_continuous_case(self.data_storage)
            if result_continuous :
                if text[-1] in self.value.operator or text[-1] == self.value.square:
                    self.error_text = "Your mathematical statement isn't corrected grammar"
                    self.show_error_text()
                else :
                    return cal_part.Evaluate(text).eval()
            else:
                self.error_text = "Your mathematical statement isn't corrected grammar"
                self.show_error_text()
                
    def show_error_text(self):
        self.textbox.setText(self.error_text)
        self.textbox.setFont(QFont('Comic Sans MS',self.font_size//2))
        
def run_app():
    print(sys.argv)
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


run_app()
