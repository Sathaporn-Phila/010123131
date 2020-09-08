from math import sqrt

class Evaluate :
    def __init__(self,expression):
        self.expression = expression
        self.name_change = {'sqrt':'square_root','x':'*','^':'**','mod':'%'}
        self.operator = {'square_root':sqrt}
    def eval(self):
        new_expression = self.expression
        for old_name,new_name in self.name_change.items() :  
            new_expression = new_expression.replace(old_name,new_name)  
        try :
            value = eval(new_expression,self.operator)
        except ZeroDivisionError :
            return "You had divide by zero , please changed expression ,and try again"
        else :
            if isinstance(value,float):
                # check if it's more than 3 three decimal
                if len(str(value)[str(value).find('.'):]) > 3 :
                    value = round(value,3)
            return value

