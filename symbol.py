class symbol_table:
    def __init__(self):#constructor
        self.symbol={}#assigns it to an empty set
    def add_symbol(self,name,type,value=None):#add function 
        self.symbol[name]={'type':type,'value':value}#assigned to the type and value
    def update_symbol(self,name,value):#update function
       #printd the value if name is found in the list
        if name in self.symbol:
            self.symbol[name]['value']=value
        else:#prints an error message
            print("Symbol '{name}' not found")

    def retrieve_symbol(self,name):#get function
        #returns name if it is found in the set
        if name in self.symbol:
            return self.symbol[name]
        else:#prints an error if not found
            print("Symbol '{name}' not found")

    #prints the output
    def print(self):
        for name, details in self.symbol.items():
            print(f"{name}: Type:{details['type']},Value:{details['value']}")

def Zara():
  symbol_tab=symbol_table()
  symbol_tab.add_symbol("x", "integer", 10)
  symbol_tab.add_symbol("m","float",54.43)
  symbol_tab.update_symbol("x",20)
 #symbol_tab.update_symbol("m",32.1)
  symbol_tab.retrieve_symbol("m")
  symbol_tab.print()
  print("Retrieved:",symbol_tab.retrieve_symbol("m"))

Zara()
