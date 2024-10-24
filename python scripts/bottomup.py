rules={
    1: ("E", 3),
    2: ("E", 1),
    3: ("T", 3),
    4: ("T", 1),
}

#goto table
action_table={
    0: {"id": "S5", "+": None, "(": "S4", ")": None, "$": None},
    1: {"id": None, "+": "S3", "(": None, ")": None, "$": "Accept"},
    2: {"id": None, "+": "R2", "(": None, ")": "R2", "$": "R2"},
    3: {"id": "S5", "+": None, "(": "S4", ")": None, "$": None},
    4: {"id": "S5", "+": None, "(": "S4", ")": None, "$": None},
    5: {"id": None, "+": "R4", "(": None, ")": "R4", "$": "R4"},
    6: {"id": None, "+": "R1", "(": None, ")": "R1", "$": "R1"},
    7: {"id": None, "+": "S3", "(": None, ")": "S8", "$": None},
    8: {"id": None, "+": "R3", "(": None, ")": "R3", "$": "R3"},

}
goto_table={
    0: {"E": 1, "T": 2},
    1: {"E": None, "T": None},
    2: {"E": None, "T": None},
    3: {"E": None, "T": 6},
    4: {"E": 7, "T": 2},
    5: {"E": None, "T": None},
    6: {"E": None, "T": None},
    7: {"E": None, "T": None},
    8: {"E": None, "T": None},
}

def shift_reduce_parser(input_tokens):
    input_tokens.append("$")#this is the end of input symbol

    stack=[0]#initial state
    index=0#first input token

    print("Stack\t\t Input\t\tAction")
    while True:
      state=stack[-1]
      current=input_tokens[index]

      action=action_table.get(state,{}).get(current,None)#action based on current state and input token

      if action is None:
        print(f"Error: Unexpected token '{current}' at index {index}")
        return False
    
      stack_str=" ".join(map(str,stack))
      input_str=" ".join(input_tokens[index:])#shows the remaining index after current token
 
      if action=="Accept":#handle accept action
        print(f"{stack_str}\t\t{input_str}\t\tAccept")
        print("Accepted!!")
        return True
    
      elif isinstance(action,str) and action.startswith("S"):#handle shift action
        print(f"{stack_str}\t\t{input_str}\t\tShift {current}")
        stack.append(current)#pushes the current token to the stack
        stack.append(int(action[1:]))#push the state from the shift action
        index+=1#next input token

      elif isinstance(action,str) and action.startswith("R"):#reduce action
        rule=int(action[1:])#gets the rule number to apply
        lhs,rhs_len=rules[rule]#gets the left handside and the length of the RHS for the reduction action
        print(f"{stack_str}\t\t{input_str}\t\tReduce {lhs} -> {''.join(map(str,stack[-2*rhs_len:][1::2]))}")

        stack=stack[:-2*rhs_len]#pop the symbol and state pairs from stack

        state=stack[-1]#gets the new state to go to after reduction
        goto=goto_table[state].get(lhs,None)

        if goto is not None:
            stack.append(lhs)#push the LHS non terminal
            stack.append(goto)#push new state from goto table

        else:
            print("Error in goto table!")
            return False
      else:
        print("Unexpected action")
        return False
    
user=input("Enter the input string(tokens should be separated by spaces e.g. 'id + id'):")
tokens=user.split()
shift_reduce_parser(tokens)
