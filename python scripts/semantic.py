class Symbol:
    def __init__(self,name,type,scope):
        self.name=name#identifier
        self.type=type#data type of the symbo;
        self.scope=scope#scope level
    def __repr__(self):
        return f"Symbol(name={self.name},type={self.type},scope={self.scope})"
    
class SymbolTable:#stores and manages symbols
    def __init__(self):#constructor
        self.symbol={}#assigns it to an empty set

    def define(self,name,type,scope):#adds new symbol to the table
        self.symbol[name]=Symbol(name,type,scope)

    def lookup(self,name):#finds a symbol by its name
        return self.symbol.get(name)

#abstract syntax tree
class AST:#represents the structure of the code
    pass
class Variable(AST):#represent variable(var)
    def __init__(self,name,type):
        self.name=name
        self.type=type

class Function(AST):#represents functions:name,param,body
    def __init__(self,name,param,body):
        self.name=name
        self.param=param
        self.body=body

class Assignment:#assignment of a value to var
    def __init__(self,var,value):
        self.var=var
        self.value=value
#scope management
class ScopeManager:
    def __init__(self):
        self.current=0
        self.scope=[{}]

    def enter(self):#move to a new scope level
        self.current+=1
        self.scope.append({})
    
    def exit(self):#exits the current scope
        if self.current>0:
            self.scope.pop()
            self.current-=1
    
    def define_symbol(self,name,type):#define symbol in the current scope
        self.scope[self.current][name]=Symbol(name,type,self.current)
    def lookup(self,name):#search for symbol in the current scope
        for scope in reversed(self.scope):
            if name in scope:
                return scope[name]
        return None
#type consistency checks

def check_consistency(node,symbol_table):
    if isinstance(node,Assignment):#if node is an assignment,checks if variale has been defined and if types match
        var=symbol_table.lookup(node.var.name)
        if var is None:
            raise Exception(f"Undefined variable:{node.var.name}")
        if var.type!=node.value.type:
            raise Exception(f"Type mismatch:{var.type} vs {node.value.type}")
            
    elif isinstance(node,function):#if function,checks parameter types and types in function body
        for param in node.param:#check parameters and body for type consistency
            symbol=symbol_table.lookup(param.name)
            if symbol is None or symbol_table.lookup(param.name):
                raise Exception(f"Type mismatch in function parameters:{param.name}")
        for statement in node.body:
            check_consistency(statement,symbol_table)
#defining type rules for arrays and stacks
def check_array(array):#checks if all elements are of the same type
    array_type=array.elements[0].type
    for element in array.elements:
        if element.type!=array_type:
            raise Exception("Array elements must be of the same type")
def check_stack(stack,oper):#checks push oper match stack's type and ensure that pop is not performed on an empty stack
    stack_type=stack.type
    if oper=="push":
        if stack.push_value.type!=stack_type:
            raise Exception("Pushed value type must match excpetion type!!")
    elif oper=="pop":
        if not stack.elements:
            raise Exception("Cannot pop from an empty stack")
        
#function checks and method usages

def check_function(function_call,symbol_table):#check if function exists
    func_sym=symbol_table.lookup(function_call.name)
    if func_sym is None:
        raise Exception(f"Undefined function:{function_call.name}")
    if len(func_sym.param)!=len(function_call.args):#checks if no. of arguments matches the function's parameter
        raise Exception(f"Argument count mismatch in function{function_call.name}")
    for param, arg in zip(func_sym.param,function_call.args):#argument types match parameter types
        if param.type!=arg.type:
            raise Exception(f"Type mismatch in function call for parameter {param.name}")
        
#performs semantic analysis
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table=SymbolTable()
        self.scope_manager=ScopeManager()

    def analyze(self,ast):#iterates over the AST and calls visit for each
        for node in ast:
            self.visit(node)
    def visit(self,node):#processes each node based on its types nad applies relevant checks
        if isinstance(node,Variable):
            if self.scope_manager.lookup(node.name):
                raise Exception(f"Variable {node.name} already defined in current scope")
            self.scope_manager.define_symbol(node.name,node.type)
        elif isinstance(node,Assignment):
            check_consistency(node,self.symbol_table)
        elif isinstance(node,Function):
            self.scope_manager.enter()
            for param in node.param:
                self.scope_manager.define_symbol(param.name,param.type)
            for statement in node.body:
                self.visit(statement)
            self.scope_manager.exit()

#example of a zara program
zara=[Variable("x","int"),Assignment(Variable("x","int"),Variable("y","string"))]
analyzer=SemanticAnalyzer()
try:
    analyzer.analyze(zara)
except Exception as e:
    print(e)

