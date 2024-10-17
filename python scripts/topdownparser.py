import re

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

def  lexical_analyzer(code):
    tokens=[]
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

#using recursive descent parser
tokens=lexical_analyzer("code")
current_index=0
#returns the current token from the token list
def current_token():
    return tokens[current_index] if current_index<len(tokens) else None
#moves to the next token by incrementing the index
def next_token():
    global current_index
    current_index+=1
#checks if the current token matches the expected type and value
def match(expected_type,expected_value=None):
    token=current_token()
    if token is None or token[0] != expected_type or (expected_value and token[1]!=expected_value):
        raise SyntaxError(f'Expected{expected_type} {expected_value} but got {token}')#displays an error if unsuccessful
    next_token()#moves to the next token if successful
#entry point for parsing the program
#checks if method def is being parsed or a statement
def parseProgram():
    if current_token()=='def':
       parseMethod()
    else:
        parseStatement()

#handles method parsing
def parseMethod():
    match('KEYWORD','def')
    match('IDENTIFIER')
    match('SEPARATOR','(')
    match('SEPARATOR',')')
    match('SEPARATOR','{')
    parseStatement()#assumes that a statement is being parsed
    match('SEPARATOR','}')
#parse a statement
def parseStatement():
    token=current_token()
    if token and token[0]=='KEYWORD' and token[1]=='if':
        parse_if_stmt()
    # elif token and token[0]=='KEYWORD' and token[1]=='for':
    #     parse_for_stmt()
    # elif token and token[0]=='KEYWORD' and token[1]=='do':
    #     parse_do_while_stmt()
    elif token and token[0]=='IDENTIFIER':
        match('IDENTIFIER')

        token=current_token()
        if token and token[0]=='OPERATOR' and token[1]=='=':
            match('OPERATOR','=')
            parseExpr()
            match('SEPARATOR',';')
        else:
           parseExpr()
           match('SEPARATOR',';')
    else:
        raise SyntaxError(f'Unexpected statement:{token}')
    
#parses an if statement
def parse_if_stmt():
    match('KEYWORD','if')
    match('SEPARATOR','(')
    parseExpr()
    match('SEPARATOR',')')
    match('SEPARATOR','{')
    parseStatement()
    match('SEPARATOR','}')
    if current_token() and current_token()[0]=='KEYWORD' and current_token()[1]=='else':
        match('KEYWORD','else')
        match('SEPARATOR','{')
        parseStatement()
        match('SEPARATOR','}')

#handles basic mathematical expressions
def parseExpr():
    parse_term() 
    while current_token() and current_token()[0] == 'OPERATOR' and current_token()[1] in ('+', '-','==','!=','<=','>=','<','>'):#operations:+,-
        match('OPERATOR') 
        parse_term() 
#handles multiplication and division 
def parse_term():
    parse_factor()  
    while current_token() and current_token()[0] == 'OPERATOR' and current_token()[1] in ('*', '/'):
        match('OPERATOR')
        parse_factor() 
#handles literals,identifiers and expressions 
def parse_factor():
    token = current_token()
    if token[0] == 'INTEGER_LITERAL' or token[0] == 'FLOAT_LITERAL':
        match(token[0])  
    elif token[0] == 'IDENTIFIER':
        match('IDENTIFIER') 
    elif token[0] == 'SEPARATOR' and token[1]=='(':
        match('SEPARATOR','(')
        parseExpr()  
        match('SEPARATOR',')')
    else:
        raise SyntaxError('Invalid factor')


code = "if (a < 5) { a = a + 1; }"
code="if(n >= 4){n = n + 1;}"
tokens = lexical_analyzer(code)
parseProgram()
print(tokens)