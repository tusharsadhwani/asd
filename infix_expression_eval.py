"""Evaluate shit"""
from typing import List


def is_higher_precedence(operator: str, operator_stack: List[str]) -> bool:
    """If the operator is of higher precedence than top of the stack"""
    # TODO: complete this
    if len(operator_stack) == 0:
        return True

    stack_top = operator_stack[-1]
    if operator == '+' and stack_top == '*':
        return False

    return True


def evaluate(operand1: int, operand2: int, operator: str) -> int:
    """Evaluate expression"""
    if operator == '+':
        return operand1 + operand2
    if operator == '*':
        return operand1 * operand2

    raise AssertionError('Invalid operator value', operator)


def process_operation(
        operand_stack: List[int],
        operator_stack: List[str]) -> None:
    """Process the top operator and two top operands from the stacks"""
    operator = operator_stack.pop()
    operand1 = operand_stack.pop()
    operand2 = operand_stack.pop()

    result = evaluate(operand1, operand2, operator)
    operand_stack.append(result)


def infix_eval() -> None:
    """Evaluates infix expression"""
    line = "((9 + 6 * 8 * 5) + 9 + 9 + 6 * 4 * 2) + (6 * 3 * 3 * 4 * 8) * (6 + (2 + 8) + 8 * 4 + (3 * 4 + 6 * 7 + 4 * 8)) * 8 * 8"

    operand_stack: List[int] = []
    operator_stack: List[str] = []

    for char in line:
        if char == ' ':
            continue

        if char == '(':
            operator_stack.append(char)

        elif char.isdigit():
            operand_stack.append(int(char))

        elif char in ['+', '-', '*', '/']:
            while not is_higher_precedence(char, operator_stack):
                process_operation(operand_stack, operator_stack)

            operator_stack.append(char)

        elif char == ')':
            opening_parenthesis_found = False
            while not opening_parenthesis_found:
                operator_stack_top = operator_stack[-1]
                if operator_stack_top == '(':
                    opening_parenthesis_found = True
                    operator_stack.pop()
                else:
                    process_operation(operand_stack, operator_stack)

    while operator_stack:
        process_operation(operand_stack, operator_stack)

    print(operand_stack.pop())


if __name__ == "__main__":
    infix_eval()
