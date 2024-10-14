import re
class symbol_table:
    def __init__(self):#constructor
        self.symbol={}#assigns it to an empty set
    def lexical_analyzer(self,code):#scans the characters
        #defines tokens using regular expression
        token_spec = [
            ('KEYWORD', r'\b(if|else|while|do|int|float|string|array|stack)\b'),
            ('OPERATOR', r'(\+|-|\*|\/|==|!=|<=|>=|<|>)'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('INTEGER_LITERAL', r'\b\d+\b'),
            ('FLOAT_LITERAL', r'\b\d+\.\d+\b'),
            ('STRING_LITERAL', r'"[^"]*"'),
            ('SEPARATOR', r'[{}();]')
                ]
        #combines into a single regular expression
        token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_spec)
         #empty array
        tokens=[]
        #checks the zara code to determine if they match
        for match in re.finditer(token_regex,code):
            kind=match.lastgroup
            value=match.group(kind)

            if kind=='WHITESPACE':
                continue
            elif kind=='MISMATCH':
                print("Unexpected character:{value}")
            else:
                tokens.append((kind,value))


        return tokens
    def print(self):
      for name, details in self.symbol.items():
         print(f"{name}: Type:{details['type']},Value:{details['value']}")

def Zara():
  symbol_tab=symbol_table()
  code = '''
    #     integer x = 10;
    #     float y = 20.5;
    #     if (x > y) {
    #         x = x + y;
    #     } else {
    #         y = x - y;
    #     }
    #     '''
    #   print("Lexical Analysis:", symbol_tab.lexical_analyzer(code))
  code="x=10+54.23"
  print(symbol_tab.lexical_analyzer(code))

Zara()