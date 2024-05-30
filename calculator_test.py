from calculator import tokenize, evaluate

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

def run_test():
    print("==== Test started! ====")

    test("1+2")
    test("1.0+2.1-3")
    test("1.4+2*3.1")
    test("1.5/3.2+2")

    test("(1.2+1.3)*3")
    test("(2)+(3)")
    test("2*(3+4*(2+5))")
    test("((1+2)*3+4)*5")

    test("abs(5)")
    test("abs(2-3)")
    test("abs(1.1*(3.5-7))")
    test("int(2.5)")
    test("int(2-3)")
    test("int(1.2*(3.4+1))")
    test("round(3.1)")
    test("round(6+2)")
    test("round((2.3+1.2)*3)")

    test("abs(int(round(3.2-5.9)+1.5)+2.6)+7.2")
    test("round(2.8)+int(3.1+(1.2*abs(3.8-12)))")

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
