import pygame
import math
from pygame.locals import *
class insert_expression_in_pygame :
    def __init__(self,data_file):
        self.data = []
        with open(data_file,'r') as data_in_line :
            for item in data_in_line :
                self.data.append(item.strip('\n'))
        initialize_pygame(self.data)

class initialize_pygame :

    white = (255,255,255)
    red = (255,0,0)
    pink = (247,166,243)
    yellow = (242,198,77)
    grey = (150,150,150)
    black = (0,0,0)
    blue = (20,60,90)
    green = (78,216,50)
    scr_w,scr_h = 620,600
    screen = pygame.display.set_mode( (scr_w,scr_h) )
    
    def __init__(self,data):
        self.data = data
        #start pygame
        pygame.init()
        #font
        pygame.font.init()
        # create a clock
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode( (initialize_pygame.scr_w, initialize_pygame.scr_h) )
        self.surface = pygame.Surface( self.screen.get_size(), pygame.SRCALPHA )
        self.screen.fill(initialize_pygame.white)
        self.running = True
        self.index = 0
        self.time = 5 
        self.run()

    def run(self):
        while self.running :
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
            if self.time == 0 :
                self.index = ((self.index+1)%(len(self.data)))
                self.time = 5
            if len(self.data) != 0 :
                #show tree
                self.display_tree(self.index)
                
            
            pygame.display.update()
            self.time -= 1
            self.clock.tick(1)

    def display_tree(self,index):
        #reset screen
        self.screen.fill(initialize_pygame.white)
        #create tree
        self.tree = Tree(self.data[index])
        #list tree with data only
        self.new_tree = self.tree.new_tree
        rows = len(self.new_tree) + 1
        #last index
        position_start = rows -1
        columns = int(math.log2(rows) + 1)
        depth = int(math.log2(rows))
        new_table = table(rows,columns)

        self.tree.mark_point(depth,Tree.start_index,Tree.level,
        position_start,Tree.direction_left,self.new_tree,new_table,draw_circle.data_circle)

        self.item_circle = self.tree.data_circle

        #check all item that aren't overlapped
        for item in self.item_circle :
            for item_check in self.item_circle :
                if (item != item_check) and (item is not None) and (item_check is not None) :
                    item.check_overlapped_circle(item_check)
        
        #draw circle
        for item in self.item_circle :
            if item is not None :
                item.circle()

        if self.time == 1 :
            # save image and show truth table, then write files
            image = "exp_tree_line_{}.jpg".format(self.index+1)
            pygame.image.save(initialize_pygame.screen,image)
            self.display_truth_table(self.tree.get_postorder_tree())

            # the last data and stop program
            if self.index == len(self.data)-1 :
                self.running = False

    def display_truth_table(self,data_list):
        self.exp_tree_evaluate = exp_cal(data_list)
        self.spacebar = ' '
        data = self.exp_tree_evaluate.get_data_list()
        set_data = []
        self.count = 0
        for item in range(len(data)) :
            key_all = data[item]
            if item == 0 :

                # key values of dict
                for item_dict_keys in key_all.keys():
                    self.count += 1
                    header = 4*self.spacebar + item_dict_keys + 4*self.spacebar
                    set_data.append(header)

                # values of dict
                for item_dict_vals in key_all.values():
                    if item_dict_vals is True :
                        set_data.append('T')
                    else:
                        set_data.append('F')
                # values of dict
            else:
                for item_dict_vals in key_all.values():
                    if item_dict_vals is True :
                        set_data.append('T')
                    else:
                        set_data.append('F')
        num_of_header = self.count
        str1 = ''
        comma = ','
        new_line = '\n'
        address = '@'
        line = len(set_data)//num_of_header
        name_text_file = "data_output_{}.txt".format(self.index+1)
        #clear file
        with open(name_text_file,'w') as file_output :
            file_output.write(str1)

        # get data and write files
        for num_line in range(line):
            for char_index in range(num_of_header):
                index = num_line*num_of_header + char_index 
                if num_line == 0 :
                    str1 +=  address +  set_data[index]  + address
                else :
                    data_header = list(set_data[char_index])
                    # find mid point for insert value
                    mid = len(data_header)//2
                    for item in range(len(data_header)):
                        if item == mid :
                            data_header[item] = set_data[index]
                        else :
                            data_header[item] = self.spacebar
                    new_str = ''
                    # sum of all string value
                    for item in data_header :
                        new_str += item
                    str1 += address + new_str + address
            with open(name_text_file,'a') as file_output :
                file_output.write(str1+new_line)
            # reset value
            str1 = ''

        
class Node :

    def __init__(self,original_data,data):
        self.original_data = original_data
        self.data = data
        self.left = None
        self.right = None
    
    def set_index(self,index):
        self.index = index

class Tree :
    start_index = 0
    level = 0
    parent = 0
    direction_left = 'left'
    direction_right = 'right'
    def __init__(self,expression):
        self.text_label(expression)
        self.data_tree = []
        self.data_circle = []
        self.root = Node(expression,None)
        self.full_tree(expression,self.root)
    def tree_struct(self,expression,root):
        self.counter = 0
        self.repeat = False
        # find {+,&}  
        for item in range(len(expression)):
            #if found parentheses , skipped it until found closed parentheses
            if expression[item] == '(':
                self.counter += 1
            elif expression[item] == ')':
                self.counter -= 1
            # ________________operand_______________
            elif (expression[item] in {'+','&'}) and (self.counter == 0):
                self.find_item_plus_and_and(expression,item,root)
                self.repeat = True
                break
        # some part are fall out from loop , so that part doesn't want to calculate
        if not self.repeat :
            # check parenthese
            if expression[0] == '(' and len(expression) >= 3:
                self.tree_struct(expression[1:-1],root)
            # check exclamation
            elif expression.startswith('!'):
                if expression[0] == '!' or expression[1] == '(':
                    # !(___________)
                    if expression.startswith('!(') and len(expression) >= 4 :
                        root.data = '!'
                        root.original_data = expression
                        root.left = Node(expression[2:-1],expression[2:-1])
                        self.tree_struct(expression[2:-1],root.left)
                    # !_____________
                    else :
                        root.data = '!'
                        root.original_data = expression
                        root.left = Node(expression[1:],expression[1:])
                        self.tree_struct(expression[1:],root.left)
        elif expression.count('+') == 0 and expression.count('&') == 0:
            root.original_data = expression
            root.data = expression
        else :
            pass
    # binary two section
    def find_item_plus_and_and(self,expression,item,root):
        root.original_data = expression
        root.data = expression[item]
        root.left = Node(expression,expression[0:item])
        root.right = Node(expression,expression[(item+1):])
        #left
        self.tree_struct(root.left.data,root.left)
        #right
        self.tree_struct(root.right.data,root.right)

    def postorder(self,root,parent):
        if root:
            # recur left side
            Tree.postorder(self,root.left,2*parent+1)
            # recur right side
            Tree.postorder(self,root.right,2*parent+2)
            # recur until left and right side is None
            root.set_index(parent)
            self.data_tree.append(root)
    
    def get_postorder_tree(self):

        return self.data_tree

    def __len__(self):
        return len(self.data_tree)

    def full_tree(self,expression,root):
        # get tree
        self.tree_struct(expression,root)
        #sort to postorder tree
        self.postorder(root,Tree.parent)
        max_size = 0
        for item in self.get_postorder_tree():
            if max_size < item.index :
                max_size = item.index 
        self.depth = 0
        while max_size > (2**(self.depth)-1):
            self.depth += 1
        self.new_tree = (2**(self.depth)-1)*[None]
        for item in self.get_postorder_tree() :
            self.new_tree[item.index] = item.data
    
    def mark_point(self,depth,index,level,position,direction,data_input,grid,data_circle):
        if level < depth and data_input[index] is not None :
            if direction == 'left':
                mid = position - (2**depth//2**(level+1))
            else :
                mid = position + (2**depth//2**(level+1))
            #mid + level = mid + count of index 0
            index_table = ((level*len(data_input))+(mid+level))
            x = grid.data_output[index_table].x + grid.data_output[index_table].width
            y = grid.data_output[index_table].y + grid.data_output[index_table].height
            radius = grid.data_output[index_table].height//(4)
            data = data_input[index]
            odd = 2*index + 1
            even = 2*index + 2
            next_level = level + 1
            if level ==  0:
                self.data_circle = (2**(depth)-1)*[None]
                self.data_circle[index] = draw_circle(x,y,radius,data)
                # recursive in root.left and root.right
                self.mark_point(depth,odd,next_level,mid,Tree.direction_left,data_input,grid,data_circle)
                self.mark_point(depth,even,next_level,mid,Tree.direction_right,data_input,grid,data_circle)
            else :
                self.data_circle[index] = draw_circle(x,y,radius,data)
                if direction == 'left':
                    index_target = (index-1)//2
                    target = self.data_circle[index_target]
                else :
                    index_target = (index-2)//2
                    target = self.data_circle[index]
                # draw line in point of child and parent
                self.data_circle[index].connect_line(self.data_circle[index_target])
                # recursive in root.left and root.right
                self.mark_point(depth,odd,next_level,mid,Tree.direction_left,data_input,grid,data_circle)
                self.mark_point(depth,even,next_level,mid,Tree.direction_right,data_input,grid,data_circle)
    def text_label(self,text):
        self.name = text
        self.font_size = 20
        self.font = pygame.font.SysFont('Comic Sans MS', self.font_size)
        self.color = initialize_pygame.red
        self.screen = initialize_pygame.screen
        text_surface = self.font.render( self.name, True, self.color )
        text_width, text_height = text_surface.get_rect()[2:]
        y_text = 10
        x_text = (initialize_pygame.scr_w//2 - text_width//2)
        self.screen.blit(text_surface,(x_text,y_text))            
class draw_circle :
    data_circle = []
    def __init__(self,x,y,radius,data):
        self.x = x
        self.y = y
        self.radius = radius
        self.name = data
        self.font_size = self.radius
        self.font = pygame.font.SysFont('Comic Sans MS', self.font_size)
    def connect_line(self,target):
        self.line_size = 4
        screen = initialize_pygame.screen
        green = initialize_pygame.green
        pygame.draw.line(screen,green,(self.x,self.y),(target.x,target.y),self.line_size)
    def circle(self):
        screen = initialize_pygame.screen
        yellow = initialize_pygame.yellow
        black = initialize_pygame.black
        pygame.draw.circle(screen,yellow,(self.x,self.y),self.radius)    
        text_surface = self.font.render( self.name, True, black )
        text_width, text_height = text_surface.get_rect()[2:]
        self.y_text = self.y - text_height//2
        self.x_text = self.x - text_width//2
        screen.blit(text_surface,(self.x_text,self.y_text))
    def check_overlapped_circle(self,target):
        distance = (self.x - target.x)**2 + (self.y - target.y)**2
        if distance <= (self.radius + target.radius)**2 :
            self.radius -= 1
            target.radius -= 1
            self.font_size = self.radius
            target.font_size = self.radius
            self.check_overlapped_circle(target)

class table :

    def __init__(self,rows,columns):
        self.rows = rows
        self.columns = columns
        self.x_scales = initialize_pygame.scr_w//self.rows
        self.y_scales = initialize_pygame.scr_h//self.columns
        self.create_grid()
    def create_grid(self):
        self.data_output = []
        for j in range(self.columns):
            for i in range(self.rows):
                x = self.x_scales*i 
                y = self.y_scales*j
                self.data_output.append(draw_square(x,y,self.x_scales,self.y_scales))
   
class draw_square:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class exp_cal :
    booltype = (0,1)
    def __init__(self,data_list):
        self.parameter1 = 0
        self.count = 0
        self.data = []
        self.stack = []
        self.data_class = []
        self.data_check_repeat = []
        self.data_in_rows = {}
        for item in data_list:
            if item.data.startswith('I') and (item.data not in self.data_check_repeat):
                self.count += 1
                self.data_check_repeat.append(item.data)
                self.data_class.append(boolean_control(item.data,2**(self.count-1)))
        self.data_check_repeat = []
        while self.parameter1 < 2**self.count :
            # check value of I_____ when its change and change boolean value when parameter divide evenly with 2^n
            for item in self.data_class :
                if (int(self.parameter1/item.num_divide) - int(item.old_number)) == 1:
                    item.set_boolean_number(((item.boolean_number+1)%2),int(self.parameter1))
            for item in data_list :
                item_all = item
                item = item.data
                if item.startswith('I') :
                    for item_class in self.data_class :
                        # non-repeated
                        if item == item_class.name and (item not in self.data_check_repeat) :
                            self.data_check_repeat.append(item)
                            self.data_in_rows[item] = item_class.booltype
                            self.stack.append(item)
                        # repeated
                        elif item == item_class.name:
                            self.stack.append(item)
                elif item in {'0','1'}:
                    if item == '0' :
                        if item == '0' and (item not in self.data_check_repeat):
                            self.data_check_repeat.append(item)
                            self.data_in_rows[item] = False
                            self.stack.append(item)
                        else:
                            self.stack.append(item)
                    else:
                        if item == '1' and (item not in self.data_check_repeat):
                            self.data_check_repeat.append(item)
                            self.data_in_rows[item] = True
                            self.stack.append(item)
                        else:
                            self.stack.append(item)
                elif item in {'+','&'}:
                    item1 = self.stack.pop()
                    item2 = self.stack.pop()
                    argument =  item_all.original_data
                    if item == '+' :
                        self.data_in_rows[argument] = (self.data_in_rows[item2] or self.data_in_rows[item1])
                    else :
                        self.data_in_rows[argument] = (self.data_in_rows[item2] and self.data_in_rows[item1])
                    self.stack.append(argument)
                else:
                    item_negate = self.stack.pop()
                    argument = item_all.original_data
                    self.data_in_rows[argument] = (not(self.data_in_rows[item_negate]))
                    self.stack.append(argument)
            self.data.append(self.data_in_rows)
            self.parameter1 += 1
            #reset data
            self.data_check_repeat = []
            self.data_in_rows = {}
            self.stack = []
    def get_data_list(self):
        return self.data

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


    
    


