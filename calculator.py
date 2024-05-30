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

def read_abs(line, index):
    if (line[index + 1] == 'b' and
        line[index + 2] == 's' and
        line[index + 3] == '('):
        return {'type': 'ABS'}, index + 4

def read_int(line, index):
    if (line[index + 1] == 'n' and
        line[index + 2] == 't' and
        line[index + 3] == '('):
        return {'type': 'INT'}, index + 4

def read_round(line, index):
    if (line[index + 1] == 'o' and
        line[index + 2] == 'u' and
        line[index + 3] == 'n' and
        line[index + 4] == 'd' and
        line[index + 5] == '('):
        return {'type': 'ROUND'}, index + 6

def read_ops(letter):
    ops = {'+': 'PLUS', '-': 'MINUS', '*': 'MULTIPLY', '/': 'DIVIDE'}
    op = ops.get(letter)
    if not op:
        print("Invalid character found: ' + line[index]")
        exit(1)
    return {'type': op}

def tokenize(line):
    tokens = []
    index = 0
    bracket_cnt = 0
    abs_cnt = 0
    int_cnt = 0
    round_cnt = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == 'a':
            (token, index) = read_abs(line, index)
            bracket_cnt += 1
            abs_cnt = bracket_cnt
        elif line[index] == 'i':
            (token, index) = read_int(line, index)
            bracket_cnt += 1
            int_cnt = bracket_cnt
        elif line[index] == 'r':
            (token, index) = read_round(line, index)
            bracket_cnt += 1
            round_cnt = bracket_cnt
        elif line[index] == '(':
            token = {'type': 'OPEN'}
            index += 1
            bracket_cnt += 1
        elif line[index] == ')':
            if bracket_cnt == 0:
                print('Unmatched ) found')
                exit(1)
            if bracket_cnt == abs_cnt:
                token = {'type': 'ABS_CLOSE'}
            elif bracket_cnt == int_cnt:
                token = {'type': 'INT_CLOSE'}
            elif bracket_cnt == round_cnt:
                token = {'type': 'ROUND_CLOSE'}
            else:
                token = {'type': 'CLOSE'}
            index += 1
            bracket_cnt += -1
        else:
            token = read_ops(line[index])
            index += 1
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
                        op_stack.pop()
                    elif op_stack[-1] == 'DIVIDE':
                        num_stack.append(safePop(num_stack) / token['number'])
                        op_stack.pop()
                    else:
                        num_stack.append(token['number'])
                else:
                    num_stack.append(token['number'])
                op_flag = False
            case 'CLOSE':
                while op_stack[-1] != 'OPEN':
                    calculate(num_stack, op_stack)
                op_stack.pop()
            case 'ABS_CLOSE':
                while op_stack[-1] != 'ABS':
                    calculate(num_stack, op_stack)
                op_stack.pop()
                num_stack.append(abs(num_stack.pop()))
            case 'INT_CLOSE':
                while op_stack[-1] != 'INT':
                    calculate(num_stack, op_stack)
                op_stack.pop()
                num_stack.append(int(num_stack.pop()))
            case 'ROUND_CLOSE':
                while op_stack[-1] != 'ROUND':
                    calculate(num_stack, op_stack)
                op_stack.pop()
                num_stack.append(round(num_stack.pop()))
            case default:
                if (op_flag and
                    default in {'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'}):
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
        case 'MULTIPLY':
            num_stack.append(safePop(num_stack) * safePop(num_stack))
        case 'DIVIDE':
            num_stack.append(1 / safePop(num_stack) * safePop(num_stack))

def safePop(stack):
    if not stack:
        invalid()
    return stack.pop()

def invalid():
    print('Invalid syntax')
    exit(1)
