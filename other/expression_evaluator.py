"""
Goal: compute the result of a simple mathematical expression given as a string.
This is a Dijkstra 2 stack algorithm: if we meet a number - put it in a first stack, if we meet
an operator - put it in a second stack. If we meet ')' - evaluate 2 previous number with the previous operator
and add the result into the numbers stack.
"""


def evaluator(exp):
    numbers = []
    operators = []
    # remove spaces
    exp = exp.replace(' ', '')
    for s in exp:
        try:
            s = int(s)
            numbers.append(s)
        except (ValueError, TypeError):
            if s == ')':
                b = numbers.pop()
                a = numbers.pop()
                # evaluate 2 previous numbers using the previous operator
                numbers.append(operate(a, b, operators.pop()))
            elif s == '(':
                # just ignore a left parenthesis
                continue
            else:
                # add all the operators (like - + / *) in a stack
                operators.append(s)
    return numbers[0]


def operate(a, b, operation):
    if operation == '+':
        return a + b
    elif operation == '*':
        return a * b
    elif operation == '-':
        return a - b
    elif operation == '/':
        return a / b


if __name__ == 'main':
    expression = '(1 +  ( (2 + 3) * (4 * 5) ) )'
    assert evaluator(expression) == 101