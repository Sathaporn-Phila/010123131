#Assignment boolean tree part 2
#Sathaporn Phila 6201012630096
#edit from Assignment boolean tree part 1
#---------------------------------------------------------------------------------------------------
import pygame
import math
from pygame.locals import *
class table:
    def __init__(self,x,y,width,height,line_thickness):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.line_thickness = line_thickness

class textbox :
    def __init__(self):

        self.x = border
        self.y = border
        self.width = scr_w - 2*self.x
        self.height = 150
        self.border = border
        pygame.draw.rect(screen,grey,(self.x,self.y,self.width,self.height))
        self.word = ''
        self.font_size = 40
        self.font = pygame.font.SysFont('Comic Sans MS', self.font_size)

    def insert_word(self,word):

        self.word += word

    def delete_word(self):

        self.word = self.word[:-1]
        pygame.draw.rect(screen,grey,(self.x,self.y,self.width,self.height))
        self.msg()

    def msg(self):

        text_surface = self.font.render( self.word, True, black )
        text_width, text_height = text_surface.get_rect()[2:]
        y_text = ((self.y + self.height)//2)-((text_height//2))
        x_text = self.x + self.border
        screen.blit(text_surface,(x_text,y_text))

    def clear(self):
        self.word = ''
        pygame.draw.rect(screen,grey,(self.x,self.y,self.width,self.height))
        self.msg()

    def check_grammar(key,case_input):
        print(key,case_input)
        #first
        if case_input == 0:
            if key in {'!','('}:
                case_input = 0
                return (True,case_input)
            elif key in {'0','1'}:
                case_input = 1
                return (True,case_input)
            elif key == 'I':
                case_input = 2
                return (True,case_input)
            else :
                return ("Your input is incorrect in grammar",case_input)
        elif case_input == 1:
            if key in {'+','&'}:
                case_input = 0
                return (True,case_input)
            elif key == ')':
                case_input = 1
                return (True,case_input)
            else :
                return ("Your input is incorrect in grammar",case_input)
        elif case_input == 2 :
            if key in {'0','1','2','3','4','5','6','7','8','9'} :
                case_input = 2
                return (True,case_input)
            elif key in {'+','&'}:
                case_input = 0
                return (True,case_input)
            elif key == ')':
                case_input = 1
                return (True,case_input)
            else :
                return ("Your input is incorrect in grammar",case_input)

class button(table):
    def set_properties(self,name,color):
        
        self.name = name
        self.color = color
        if self.color != blue :
            self.change_color()
        self.font_size = self.height//2
        self.font = pygame.font.SysFont('Comic Sans MS', self.font_size)
        self.button_name()

    def set_properties_all(self,name,color,font_color):
        
        self.name = name
        self.color = color
        self.font_size = self.height//2
        self.font = pygame.font.SysFont('Comic Sans MS', self.font_size)
        self.font_color = font_color

        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))
        pygame.draw.rect(screen,white,(self.x,self.y,self.width,self.height),self.line_thickness)
        text_surface = self.font.render( self.name, True, self.font_color )
        text_width, text_height = text_surface.get_rect()[2:]
        x_text = self.x + ((self.width - text_width)//2)
        y_text = self.y + ((self.height - text_height)//2)
        screen.blit(text_surface,(x_text,y_text))

    def change_color(self):

        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))
        pygame.draw.rect(screen,white,(self.x,self.y,self.width,self.height),self.line_thickness)

    def button_name(self):

        text_surface = self.font.render( self.name, True, black )
        text_width, text_height = text_surface.get_rect()[2:]
        x_text = self.x + ((self.width - text_width)//2)
        y_text = self.y + ((self.height - text_height)//2)
        screen.blit(text_surface,(x_text,y_text))
    
class true_table(table):

    def set_text(self,word,color):
        self.name = word   
        self.color = color
        self.set_font_text()
    def set_font_text(self):
        self.font_size = self.height//2
        self.font = pygame.font.SysFont('Comic Sans MS', self.font_size)
        self.font_color = (0,0,0)

    def draw_table(self):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))
        pygame.draw.rect(screen,black,(self.x,self.y,self.width,self.height),self.line_thickness)
        text_surface = self.font.render( self.name, True, self.font_color )
        text_width, text_height = text_surface.get_rect()[2:]
        check = False
        divide_size = 2
        while check == False:
            # check if text width more than border
            if self.width - text_width < 0 :
                self.font_size = self.height//(divide_size+1)
                self.font = pygame.font.SysFont('Comic Sans MS', self.font_size)
                text_surface = self.font.render( self.name, True, self.font_color )
                text_width, text_height = text_surface.get_rect()[2:]
                divide_size += 1 
            else :
                check = True
        x_text = self.x + ((self.width - text_width)//2)
        y_text = self.y + ((self.height - text_height)//2)
        screen.blit(text_surface,(x_text,y_text))

class Node :
    def __init__(self,key):
        self.left = None
        self.right = None
        self.key = key

    def set_index(self,index):
        self.index = index

class Tree :
    def tree_struct(expression,root):
        counter = 0
        repeat = False
        # find {+,&}  
        for item in range(len(expression)):
            if expression[item] == '(':
                counter += 1
            elif expression[item] == ')':
                counter -= 1
            elif (expression[item] in {'+','&'}) and (counter == 0):
                Tree.find_item_plus_and_and(expression,item,root)
                repeat = True
                break
        # some part are fall out from loop , so that part doesn't want to calculate
        if not repeat :
            # check parenthese
            if expression[0] == '(' and len(expression) >= 3:
                Tree.tree_struct(expression[1:-1],root)
            # check exclamation
            elif expression.startswith('!'):
                if expression[0] == '!' or expression[1] == '(':
                    if expression.startswith('!(') and len(expression) > 4 :
                        root.key = '!'
                        root.left = Node(expression[2:-1])
                        Tree.tree_struct(expression[2:-1],root.left)
                    else :
                        root.key = '!'
                        root.left = Node(expression[1:])
                        Tree.tree_struct(expression[1:],root.left)
        elif expression.count('+') == 0 and expression.count('&') == 0:
            root.key = expression
        else :
            pass

    def find_item_plus_and_and(expression,item,root):
        root.key = expression[item]
        root.left = Node(expression[0:item])
        root.right = Node(expression[(item+1):])
        Tree.tree_struct(root.left.key,root.left)
        Tree.tree_struct(root.right.key,root.right)

    def postorder(root,data_store,index_store,parent): 
        # if root isn't None
        if root:                                                        
            # First recur on left child 
            Tree.postorder(root.left,data_store,index_store,2*parent+1)
            # the recur on right child 
            Tree.postorder(root.right,data_store,index_store,2*parent+2)
            data_store.append(root.key)
            root.set_index(parent)
            index_store.append(parent)

class circle:
    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.name = ""
        self.font_size = self.radius
        self.font = pygame.font.SysFont('Comic Sans MS', self.font_size)
    def draw_line(self,target):
        self.line_size = 4
        pygame.draw.line(screen,green,(self.x,self.y),(target.x,target.y),self.line_size)
    def set_name(self,name):
        self.name = name
        self.insert_text()
    def insert_text(self):
        pygame.draw.circle(screen,yellow,(self.x,self.y),self.radius)    
        text_surface = self.font.render( self.name, True, black )
        text_width, text_height = text_surface.get_rect()[2:]
        y_text = self.y - self.radius//2
        x_text = self.x - text_width//2
        screen.blit(text_surface,(x_text,y_text))
#data_type of boolean
class boolean_control :
    def __init__(self,name,num_divide):
        self.name = name
        self.num_divide = num_divide
        self.boolean_number = 0
        self.old_number = 0
        self.booltype = bool(self.boolean_number)
    def set_boolean_number(self,number_boolean,number):
        self.boolean_number = number_boolean
        self.old_number = int(number)
        self.booltype = bool(self.boolean_number)
def create_table(i,j,cases,data_list):

    global arr_of_class,case,grid
    #bool calculater 
    if cases is case[0]:
        arr_of_class = data_list
        x_initial = border
        y_initial = (input_text.y  + input_text.height + border)
        x_scale = (scr_w - 2*border)//i
        y_scale = (scr_h - y_initial - border)//j
        line_thickness = 5
        for rows in range(j):
            for columns in range(i):
                x = (x_scale*columns + x_initial)
                y = (y_scale*rows + y_initial)
                arr_of_class.append(str( rows*columns + rows ))
                arr_of_class[-1] =  button(x,y,x_scale,y_scale,line_thickness)
        for item in arr_of_class :
            pygame.draw.rect(screen,blue,(item.x,item.y,item.width,item.height))
            pygame.draw.rect(screen,white,(item.x,item.y,item.width,item.height),item.line_thickness)
    
    #tree gui
    elif cases is case[1]:
        grid = data_list
        x_initial = border
        height_of_area_loading = 40
        y_initial = border + height_of_area_loading
        x_scale = (scr_w - 2*border)//i
        y_scale = (scr_h - y_initial - border)//j
        line_thickness = 5
        for rows in range(j):
            for columns in range(i):
                x = (x_scale*columns + x_initial)
                y = (y_scale*rows + y_initial)
                grid.append(str( rows*columns + rows ))
                grid[-1] =  table(x,y,x_scale,y_scale,line_thickness)

        for item in grid :
            pygame.draw.rect(screen,white,(item.x,item.y,item.width,item.height))
    #truth table
    elif cases is case[2]:
        grid = []
        data = data_list
        print(data)
        x_initial = border
        y_initial = border 
        x_scale = (scr_w - 2*border)//i
        y_scale = (scr_h - y_initial - border)//j
        line_thickness = 5
        for rows in range(j):
            for columns in range(i):
                print(rows*columns+rows,columns,rows)
                data_char = data[i*rows + columns] 
                if data_char in {True,False}:
                    if data_char == True :
                        data_char = 'T'
                    else:
                        data_char = 'F'
                x = (x_scale*columns + x_initial)
                y = (y_scale*rows + y_initial)
                grid.append(str( columns*rows + columns ))
                grid[-1] =  true_table(x,y,x_scale,y_scale,line_thickness)
                if rows == 0 :
                    grid[-1].set_text(data_char,green)
                else:
                    grid[-1].set_text(data_char,yellow)
        for item in grid :
            item.draw_table()

def create_button():

    button_I = arr_of_class[0]
    button_I.set_properties("I",red)

    button_exclamation_mark = arr_of_class[1]
    button_exclamation_mark.set_properties("!",red)

    button_and = arr_of_class[2]
    button_and.set_properties("&",red)

    button_off = arr_of_class[3]
    button_off.set_properties_all("Off",black, white)

    button_1 = arr_of_class[4]
    button_1.set_properties("1",blue)

    button_2 = arr_of_class[5]
    button_2.set_properties("2",blue) 

    button_3 = arr_of_class[6]
    button_3.set_properties("3",blue)

    button_plus = arr_of_class[7]
    button_plus.set_properties("+",red)

    button_4 = arr_of_class[8]
    button_4.set_properties("4",blue)

    button_5 = arr_of_class[9]
    button_5.set_properties("5",blue)

    button_6 = arr_of_class[10]
    button_6.set_properties("6",blue)

    button_delete = arr_of_class[11]
    button_delete.set_properties_all("Delete",yellow,black)

    button_7 = arr_of_class[12]
    button_7.set_properties("7",blue)

    button_8 = arr_of_class[13]
    button_8.set_properties("8",blue)

    button_9 = arr_of_class[14]
    button_9.set_properties("9",blue)

    button_clear = arr_of_class[15]
    button_clear.set_properties_all("Clear",yellow,black)

    button_bracketleft = arr_of_class[16]
    button_bracketleft.set_properties("(",red)

    button_0 = arr_of_class[17]
    button_0.set_properties("0",blue)

    button_bracketright = arr_of_class[18]
    button_bracketright.set_properties(")",red)

    button_ans = arr_of_class[19]
    button_ans.set_properties_all("Ans",green,black)

def check_button(x,y):
    index = 0
    for item in arr_of_class :
        if (item.line_thickness < x - item.x < 
            item.width - item.line_thickness) and (item.line_thickness < y - item.y < 
            item.height - item.line_thickness) :
            # button that clicked is activated
            return index
        else :
            index += 1
    return None
#----------------------------------page------------------------------------#
#create gui for bool calculator
def pg1():
    global case_input
    case_input = 0
    screen.fill(green)
    input_text = textbox()
    create_table(4,5,case[0],arr_of_class)
    create_button()

def pg2(index_store,data_store,real_data,depth):
    #print(depth)
    i = 2**(depth)
    j = depth + 1
    level = 0
    create_table(i,j,case[1],grid)
    parent = 0
    position = len(real_data)
    #print(position,"position",depth,'depth')
    parameter_left_or_right = 'left'
    binary_circle(parent,level,depth,real_data,position,parameter_left_or_right)
    for item in arr_of_class :
        if not item == None:
            item.insert_text()
        pygame.display.flip()

def pg3(data_store):
    screen.fill(blue)
    arr = expression_tree(data_store)
    item_all = []
    for item in range(len(arr)) :
        key_all = arr[item]
        if item == 0 :
            for item_dict_keys in key_all.keys():
                item_all.append(item_dict_keys)
            for item_dict_vals in key_all.values():
                item_all.append(item_dict_vals)
        else:
            for item_dict_vals in key_all.values():
                item_all.append(item_dict_vals)
    print(item_all) 
    columns = len(arr[0])
    rows = (len(item_all)//columns)               
    create_table(columns,rows,case[2],item_all)

#----------------------------------------tree------------------------------------#
#create list from tree class that it will use for construct circlass
def get_arr(expression,root,data_store,index_store,real_data,parent):
    if expression.count('(')-expression.count(')') == 0 :
        Tree.tree_struct(expression,root)
        Tree.postorder(root,data_store,index_store,parent)
        #return value and index
        value_max = max(index_store)
        depth = 0
        while (2**(depth)-1) <= value_max :
            depth += 1
        real_data = (2**depth -1)*[None]
        for i in range(len(index_store)):
            real_data[index_store[i]] = data_store[i]
        return (index_store,data_store,real_data,depth)

    
def binary_circle(parent,level,depth,real_data,position,parameter_left_or_right):
    global arr_of_class
    
    if level < depth :
        data = real_data[parent]
        if parameter_left_or_right == 'left' :
            mid = position - (2**depth//2**(level+1))
        else :
            mid = position + (2**depth//2**(level+1))
        index_table = ((level*len(real_data))+(mid+level))
        if not data == None:
            x = grid[index_table].x + grid[index_table].width
            y = grid[index_table].y + grid[index_table].height
            radius = grid[index_table].height//(4)
            if level == 0 :
                print(data)
                #construct a class in list as same as button
                arr_of_class = []
                arr_of_class = (2**depth -1)*[None]
                arr_of_class[parent] = circle(x,y,radius)
                arr_of_class[parent].set_name(data)
                binary_circle(2*parent+1,level+1,depth,real_data,mid,'left')
                binary_circle(2*parent+2,level+1,depth,real_data,mid,'right') 
            else :
                arr_of_class[parent] = circle(x,y,radius)
                if parameter_left_or_right == 'left' :
                    index = (parent-1)//2
                    target = arr_of_class[index]
                else :
                    index = (parent-2)//2
                    target = arr_of_class[index]
                arr_of_class[index].draw_line(arr_of_class[parent])
                arr_of_class[parent].set_name(data)
                binary_circle(2*parent+1,level+1,depth,real_data,mid,'left')
                binary_circle(2*parent+2,level+1,depth,real_data,mid,'right')

def expression_tree(data_list):
    print(data_list)    
    param_1 = 0
    count = 0
    booltype_index = (0,1)
    data = []
    stack = []
    data_class = []
    data_check_repeat = []
    data_in_rows = {}
    for item in data_list:
        if item.startswith('I') and (item not in data_check_repeat):
            count += 1
            data_check_repeat.append(item)
            data_class.append(boolean_control(item,2**(count-1)))
    data_check_repeat = []
    while param_1 < 2**count :
        for item in data_class :
            if (int(param_1/item.num_divide) - int(item.old_number)) == 1:
                item.set_boolean_number(((item.boolean_number+1)%2),int(param_1))
        for item in data_list :
            if item.startswith('I') :
                for item_class in data_class :
                    if item == item_class.name and (item not in data_check_repeat) :
                        data_check_repeat.append(item)
                        data_in_rows[item] = item_class.booltype
                        stack.append(item)
                    elif item == item_class.name:
                        stack.append(iem)
            elif item in {'0','1'}:
                if item == '0' :
                    if item == '0' and (item not in data_check_repeat):
                        data_check_repeat.append(item)
                        data_in_rows[item] = True
                        stack.append(item)
                    else:
                        stack.append(item)
                else:
                    if item == '1' and (item not in data_check_repeat):
                        data_check_repeat.append(item)
                        data_in_rows[item] = True
                        stack.append(item)
                    else:
                        stack.append(item)
            elif item in {'+','&'}:
                print(stack)
                item1 = stack.pop()
                item2 = stack.pop()
                argument =  (item2+item+item1)
                if item == '+' :
                    data_in_rows[argument] = (data_in_rows[item2] or data_in_rows[item1])
                else :
                    data_in_rows[argument] = (data_in_rows[item2] or data_in_rows[item1])
                stack.append(argument)
            else:
                item_negate = stack.pop()
                argument = (item+item_negate)
                data_in_rows[argument] = (not(data_in_rows[item_negate]))
                stack.append(argument)
        data.append(data_in_rows)
        param_1 += 1
        data_check_repeat = []
        data_in_rows = {}
        stack = []
    return data
    
    


pygame.init()
#font
pygame.font.init()
# create a clock
clock = pygame.time.Clock()
#color
white = (255,255,255)
red = (255,0,0)
pink = (247,166,243)
yellow = (242,198,77)
grey = (150,150,150)
black = (0,0,0)
blue = (20,60,90)
green = (78,216,50)
#class node
root = Node(None)
data_store = []
index_store = []
real_data = []
grid = []
arr_of_class = []
parent = 0
# screen display
global scr_w,scr_h,border,case
border = 10
scr_w,scr_h = 620,600
screen = pygame.display.set_mode( (scr_w, scr_h) )
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )
bg = green
screen.fill(bg)

#program running
running = True
first_create = True
parameter = False
case = ['case1','case2','case3']
#case 1 = gui for boolean calculator

case_target = case[0]
case_input = 0
while running :
    if case_target == case[0]:
        if first_create:
            print('in loop')
            first_create = False
            input_text = textbox()
            create_table(4,5,case[0],arr_of_class)
            create_button()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            #Keyboard input
            if e.type == KEYDOWN :
                keyname = e.unicode
                if keyname in {'0','1','2','3','4','5','6','7','8','9','I','!','&','+',' ','(',')'} :
                    if keyname in {'0','1','2','3','4','5','6','7','8','9','I','!','&','+','(',')'} :
                        parameter1 = textbox.check_grammar(keyname,case_input)
                        case_input = parameter1[1]
                        booltype = parameter1[0]
                        if booltype == True :
                            input_text.word += e.unicode
                        #boolltype == show error 
                        else :
                            word = input_text.word
                            input_text.clear()
                            input_text.insert_word(booltype)
                            input_text.clear()
                            input_text.msg()
                            input_text.clear()
                            input_text.insert_word(word)
                elif keyname == ' ' :
                    input_text.insert_word(" ")
                elif e.key == K_BACKSPACE or e.key == K_DELETE :
                    input_text.delete_word()
                else :
                    pass
            if e.type == pygame.MOUSEBUTTONDOWN:   
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                arr_index = check_button(x,y)
                #check button function
                if arr_index in (set(list(range(20))) - {3,11,15,19}):
                    word = arr_of_class[arr_index].name
                    parameter1 = textbox.check_grammar(word,case_input)
                    case_input = parameter1[1]
                    booltype = parameter1[0]
                    if booltype == True :
                        input_text.word += word
                    #else : booltype == error and cannot inserted word
                    
                # function that isn't inserted string
                elif arr_index in {3,11,15,19}:
                    if arr_index == 3 :
                        running = False
                    elif arr_index == 11 :
                        input_text.delete_word()
                    elif arr_index == 15 :
                        input_text.clear()
                    else :
                        pygame.image.save(screen,"boolean calculator.jpg")
                        arr = get_arr(input_text.word,root,data_store,index_store,real_data,parent)
                        index_store,data_store,real_data,depth = arr[0],arr[1],arr[2],arr[3]
                        case_target = case[1]
                        first_create = True
                        screen.fill(white)
                        #create next page
                        pg2(index_store,data_store,real_data,depth)
                        pygame.image.save(screen,"tree gui.jpg")
                        input_text.word = ""
                else:
                    pass

        input_text.msg()
        clock.tick( 10 )
    if case_target == case[1]:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == KEYDOWN and e.key == K_LEFT :
                #reset data
                case_target = case[0]
                first_create = True
                data_store = []
                index_store = []
                arr_of_class = []
                real_data = []
                grid = []
                root = Node(None)
                pg1()
            if e.type == KEYDOWN and e.key == K_RIGHT :
               case_target = case[2]
               #data_store is postorder tree
               pg3(data_store) 

        if first_create :
            first_create = False

        clock.tick(1)   
    if case_target == case[2]:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                pygame.image.save(screen,"truth table")
            if e.type == KEYDOWN and e.key == K_RIGHT :
                #reset data
                case_target = case[0]
                first_create = True
                data_store = []
                index_store = []
                arr_of_class = []
                real_data = []
                grid = []
                root = Node(None)
                pg1()

    pygame.display.update()
pygame.quit()
