class Case_storage :
    def __init__(self,case,data):
        self.case = case
        self.data = data

# class of probability that user will input correct grammar.
class Check_grammar :
    numeric = '0123456789'
    point = '.'
    operator = {'+','-','x','/','mod'}
    square_root = 'sqrt('
    square = '^'
    open_bracket = '('
    close_bracket = ')'
    type_of_case = {0:[0,1,4],1:[1,2,3,4,5],2:[1],3:[0,1],4:[0,1],5:[3,4,5]}
    def __init__(self):
        self.no_text = True
        self.case_input = ''
        self.no_dot = True
        self.count_bracket = 0
    def check_case(self,value):
        if self.no_text :
            if (value == self.open_bracket) or (value == self.square_root) or (value in self.numeric) or (value == '-'):
                if (value == self.open_bracket) or (value == self.square_root):
                    self.case_input = 0
                else :
                    self.case_input = 1
                self.no_text = False

        # open bracket and square root
        if self.case_input == 0:
            if (value == self.open_bracket) or (value == self.square_root) or (value in self.numeric):
                if value == self.open_bracket or value == self.square_root :
                    self.case_input = 0
                elif value in self.numeric :
                    self.case_input = 1
                return Case_storage(self.case_input,value)

        #numeric
        elif self.case_input == 1 :
            if (value in self.numeric) or (value == self.point) or (value == self.square) or (value in self.operator) or (value == self.close_bracket):
                if value in self.numeric :
                    self.case_input = 1
                    return Case_storage(self.case_input,value)
                elif (value == self.point and self.no_dot) :
                    self.case_input = 2
                    self.no_dot = False
                    return Case_storage(self.case_input,value)
                elif value == self.square :
                    self.case_input = 3
                    return Case_storage(self.case_input,value)
                elif value in self.operator :
                    self.case_input = 4
                    return Case_storage(self.case_input,value)
                elif value == self.close_bracket and self.count_bracket == 0:
                    self.case_input = 5
                    return Case_storage(self.case_input,value)

        #dot
        elif self.case_input == 2 :
            if value in self.numeric:
                self.case_input = 1
                return Case_storage(self.case_input,value)

        #square
        elif self.case_input == 3:
            if value == self.open_bracket or value in self.numeric or value == self.square_root :
                if (value == self.open_bracket) or (value == self.square_root):
                    self.case_input = 0
                else:
                    self.case_input = 1
                    self.no_dot = True
                return Case_storage(self.case_input,value)

        #operator
        elif self.case_input == 4:
            if (value == self.open_bracket) or (value in self.numeric) or (value == self.square_root):
                if value == self.open_bracket or value == self.square_root:
                    self.case_input = 0
                else:
                    self.case_input = 1
                    self.no_dot = True                                                                                                                                                                                                                                                                                                                      
                return Case_storage(self.case_input,value)


        #close_bracket
        elif self.case_input == 5 :
            if value == self.square or value in self.operator or value == self.close_bracket:
                if value == self.square :
                    self.case_input = 3
                    return Case_storage(self.case_input,value)
                elif value in self.operator:
                    self.case_input = 4
                    return Case_storage(self.case_input,value)
                elif value == self.close_bracket and self.count_bracket == 0 :
                    self.case_input = 5
                    return Case_storage(self.case_input,value)

    def check_type(self,value):
        if ((value in self.numeric) or (value == self.point) or (value in self.operator) or 
            (value == self.square_root) or (value == self.square) or (value == self.open_bracket) or
            (value == self.close_bracket)) :
            return "Error type"
        else:
            return "Function type"

    def change_case(self,value):
        self.case_input = value

    def check_dot(self,text):
        if text.count(self.point) == 0 :
            self.no_dot = True
        else:
            self.no_dot = False

    def check_num_square_root(self,text,cursor_position):
        self.index = 0
        self.count = 0
        while self.index < cursor_position :
            if text[self.index] == 's' :
                self.count += 1
                self.index += 5
            self.index +=1
        return self.count

    def check_continuous_case(self,data_list):
        if len(data_list) == 0 :
            return True
        else:
            result = ""
            for index in range(1,len(data_list))  :
                if data_list[index].case in self.type_of_case[data_list[index-1].case] :
                    result = True
                else:
                    result = False
                    break
            return result
