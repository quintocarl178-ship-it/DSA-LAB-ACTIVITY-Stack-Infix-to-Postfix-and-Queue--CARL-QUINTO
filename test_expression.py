
"""ITECC04 Laboratory 4, Parts B and C: the converter and the evaluator.

Part B turns infix into postfix using the Shunting Yard algorithm.
Part C evaluates a postfix expression.

Both use your own stack. Import it, do not use a bare Python list. If your
ArrayStack is not finished, these functions cannot work, so finish Part A
first.

TOKENS ARE SEPARATED BY SPACES. "3 + 4" is valid input, "3+4" is not. This
is deliberate: writing a real tokeniser is a different exercise, and mixing
it in here hides the algorithm you are meant to be learning.
"""

from stack_array import ArrayStack

# Written for you. Higher number binds tighter.
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}

# Written for you. 2 ^ 3 ^ 2 means 2 ^ (3 ^ 2), not (2 ^ 3) ^ 2.
RIGHT_ASSOCIATIVE = {"^"}


def tokenize(expression):
    """Written for you. Splits on whitespace."""
    return expression.split()


def infix_to_postfix(expression):
    """Step 1. Convert infix to postfix. Return a space-separated string.

    Walk the tokens once. For each token, exactly one of these applies:

      operand      append it to the output, immediately
      operator     while the operator on top of the stack is not "(" and
                   outranks this one, pop it to the output. Then push this
                   one. An operator of EQUAL precedence also gets popped,
                   unless this operator is right associative.
      "("          push it. It is a fence, not an operator.
      ")"          pop to the output until "(" is on top, then discard the
                   "(". If the stack empties first, the parentheses are
                   unbalanced: raise ValueError.

    After the last token, pop whatever is left to the output. If a "(" comes
    off during that drain, the parentheses are unbalanced: raise ValueError.

    Return " ".join(output).
    """

    stack = ArrayStack()
    output = []

    for token in tokenize(expression):

        # Operand
        if token not in PRECEDENCE and token not in ("(", ")"):
            output.append(token)

        # Left parenthesis
        elif token == "(":
            stack.push(token)

        # Right parenthesis
        elif token == ")":
            while not stack.is_empty() and stack.peek() != "(":
                output.append(stack.pop())

            if stack.is_empty():
                raise ValueError("unbalanced parentheses")

            stack.pop()  # discard "("

        # Operator
        else:
            while (
                not stack.is_empty()
                and stack.peek() != "("
                and (
                    PRECEDENCE[stack.peek()] > PRECEDENCE[token]
                    or (
                        PRECEDENCE[stack.peek()] == PRECEDENCE[token]
                        and token not in RIGHT_ASSOCIATIVE
                    )
                )
            ):
                output.append(stack.pop())

            stack.push(token)

    # Drain the remaining operators
    while not stack.is_empty():
        top = stack.pop()

        if top == "(":
            raise ValueError("unbalanced parentheses")

        output.append(top)

    return " ".join(output)


def evaluate_postfix(expression):
    """Step 2. Evaluate a postfix expression. Return a float.

    Walk the tokens once, with a stack of values:

      operand      push float(token)
      operator     pop TWICE. The FIRST pop is the RIGHT operand, the second
                   is the left. Getting this backwards passes for + and *
                   and quietly fails for - and /, so it survives careless
                   testing.

    Guards:
      fewer than two values when an operator arrives -> ValueError
      more than one value left at the end            -> ValueError
      division or modulo by zero                     -> ZeroDivisionError

    Return the single remaining value.
    """

    stack = ArrayStack()

    for token in tokenize(expression):

        # Operator
        if token in PRECEDENCE:

            if stack.size() < 2:
                raise ValueError("not enough operands")

            # First pop = right operand
            right = stack.pop()

            # Second pop = left operand
            left = stack.pop()

            result = apply_operator(token, left, right)

            stack.push(result)

        # Operand
        else:
            try:
                value = float(token)
            except ValueError:
                raise ValueError(f"invalid token: {token}")

            stack.push(value)

    # There must be exactly one value left
    if stack.size() != 1:
        raise ValueError("malformed postfix expression")

    return stack.pop()


def apply_operator(operator, left, right):
    """Step 3. Return the result of `left operator right`.

    Handle + - * / % ^. Raise ZeroDivisionError with a message for / and %
    when right is 0. Raise ValueError for any operator you do not know.
    """

    if operator == "+":
        return left + right

    elif operator == "-":
        return left - right

    elif operator == "*":
        return left * right

    elif operator == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero")
        return left / right

    elif operator == "%":
        if right == 0:
            raise ZeroDivisionError("modulo by zero")
        return left % right

    elif operator == "^":
        return left ** right

    else:
        raise ValueError(f"unknown operator: {operator}")


def convert_and_evaluate(expression):
    """Written for you. Used by the test file and by the classwork demo."""
    postfix = infix_to_postfix(expression)
    return postfix, evaluate_postfix(postfix)


if __name__ == "__main__":
    # Once Steps 1 to 3 are written, this prints the worked example from the
    # lecture. Until then it reports which step is still missing.
    try:
        postfix, value = convert_and_evaluate("3 + 4 * 2")
        print("infix   : 3 + 4 * 2")
        print("postfix :", postfix)
        print("value   :", value)
    except NotImplementedError as unfinished:
        print("Not written yet ->", unfinished)
