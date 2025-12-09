"""
Given a string of brackets, determine if parentheses are valid.

Stack rules:
- Push opening.
- On closing, check if it matches top of stack.
"""


def is_valid_parentheses(s):
    stack = []
    match = {")": "(", "]": "[", "}": "{"}

    for ch in s:
        if ch in "([{":
            stack.append(ch)
        else:
            if not stack or stack[-1] != match[ch]:
                return False
            print(f"stack in else: {stack}")
            stack.pop()

    return len(stack) == 0


# Test
print("Is valid parentheses:", is_valid_parentheses("()[]{}"))  # True
print("Is valid parentheses:", is_valid_parentheses("([)]"))  # False
print("Is valid parentheses:", is_valid_parentheses("{[()]}"))  # True
