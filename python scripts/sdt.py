class symbol_table:
    def __init__(self):
        self.symbol={}
    def add_symbol(self,name,type,value=None):#add function 
        self.symbol[name]={'type':type,'value':value}#assigned to the type and value
class intermediateCode:#generation and storage of TAC lines
    def __init__(self):
        self.code=[]
        self.tempc=0
    def temp(self):
        temp_txt=f"t{self.tempc}"
        self.tempc+=1
        return temp_txt
    def emit(self,op,arg1=None,arg2=None,result=None):
        self.code.append(f"{result}={arg1} {op} {arg2}" if arg2 else f"{result}={op} {arg1}")
    def print(self):
        for line in self.code:
            print(line)
#instantiating the symbol table and the code generator
symbolTable=symbol_table()
icg=intermediateCode()
#rule for  expression-E->E+T
def translate_add(E,T):
    E.place=icg.temp()
    icg.emit('+',E.left.place,T.place,E.place)
#while loop rule
def translate_while(condition,body):
    label=icg.temp()
    icg.emit('LABEL', label)
    #emit code for condition
    icg.emit('IF_FALSE',condition.place,'GOTO','end_label')
#emit code for body
    for stmt in body:
        icg.emit(stmt.op,stmt.arg1,stmt.arg2,stmt.result)
#logging back to the start
    icg.emit('GOTO',label)
    icg.emit('LABEL','end_label')

def translate_func(name,param,body):#subprogram rule
    icg.emit('FUNC_BEGIN',name)
    for params in param:
        symbolTable.add_symbol(params,'parameter')
    for stmt in body:
        icg.emit(stmt.op,stmt.arg1,stmt.arg2,stmt.result)

    icg.emit('FUNC_END', name)

symbolTable.add_symbol("x","int")
symbolTable.add_symbol("y","int")

E=type("Expr",(), {"left":type("ExprLeft",(),{"place":"x"}),"place":None})
T=type("Term",(),{"place":"y"})
translate_add(E,T)

translate_while(type("Condition",(),{"place":"x<y"}), [
    type("Statement",(),{"op":"+","arg1":"x","arg2":"1","result":"x"})

])
translate_func("myFunc",["a","b"],[
    type("Statement",(),{"op":"*","arg1":"a","arg2":"b","result":"c"})
])

icg.print()