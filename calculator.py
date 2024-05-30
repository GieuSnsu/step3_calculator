def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_open(line, index):
    token = {'type': 'OPEN'}
    return token, index + 1

def read_close(line, index):
    token = {'type': 'CLOSE'}
    return token, index + 1

def read_ops(line, index):
    ops = {'+': 'PLUS', '-': 'MINUS', '*': 'MULTIPLY', '/': 'DIVIDE'}
    op = ops.get(line[index])
    if not op:
        print("Invalid character found: ' + line[index]")
        exit(1)
    return {'type': op}, index + 1

def tokenize(line):
    tokens = []
    index = 0
    bracket_cnt = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '(':
            (token, index) = read_open(line, index)
            bracket_cnt += 1
            bracket_cnt
        elif line[index] == ')':
            if bracket_cnt == 0:
                print('Unmatched ) found')
                exit(1)
            (token, index) = read_close(line, index)
            bracket_cnt += -1
        else:
            (token, index) = read_ops(line, index)
        tokens.append(token)
    if bracket_cnt > 0:
        print('Unmatched ( found')
        exit(1)
    return tokens

def evaluate(tokens):
    num_stack = []
    op_stack = []
    op_flag = False
    for token in tokens:
        match token['type']:
            case 'NUMBER':
                if op_stack:
                    if op_stack[-1] == 'MULTIPLY':
                        num_stack.append(safePop(num_stack) * token['number'])
                    elif op_stack[-1] == 'DIVIDE':
                        num_stack.append(safePop(num_stack) / token['number'])
                    else:
                        num_stack.append(token['number'])
                else:
                    num_stack.append(token['number'])
                op_flag = False
            case 'CLOSE':
                while op_stack[-1] != 'OPEN':
                    calculate(num_stack, op_stack)
            case default:
                if op_flag:
                    invalid()
                op_stack.append(default)
                op_flag = True
    while len(num_stack) > 1 or op_stack:
        calculate(num_stack, op_stack)
    if len(num_stack) != 1 or op_stack:
        invalid()
    return num_stack[0]

def calculate(num_stack, op_stack):
    match op_stack.pop():
        case 'PLUS':
            num_stack.append(safePop(num_stack) + safePop(num_stack))
        case 'MINUS':
            num_stack.append(- safePop(num_stack) + safePop(num_stack))

def safePop(stack):
    if not stack:
        invalid()
    return stack.pop()

def invalid():
    print('Invalid syntax')
    exit(1)

# def evaluate(tokens):
#     answer = 0
#     tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
#     index = 1
#     stack = []
#     while index < len(tokens):
#         if tokens[index]['type'] == 'NUMBER':
#             if tokens[index - 1]['type'] == 'PLUS':
#                 answer += tokens[index]['number']
#             elif tokens[index - 1]['type'] == 'MINUS':
#                 answer -= tokens[index]['number']
#             else:
#                 print('Invalid syntax')
#                 exit(1)
#         index += 1
#     return answer
