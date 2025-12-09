"""
Reverse substrings inside parentheses:

'abc(def)ghi'  → 'abcfedghi'
'a(bc(de)f)g' → 'afedcbg'

Use stack:
- Push characters.
- When ')' found: pop until '(' and reverse that substring.
"""


def reverse_parentheses(s):
    stack = []

    for ch in s:
        if ch != ")":
            stack.append(ch)
            print(f"for char:{ch}, stack in if condition: {stack}")
        else:
            temp = []  # stores the reversed substring and anything after it
            # Pop until "("
            while stack and stack[-1] != "(":
                temp.append(stack.pop())
            print(f"for char:{ch}, temp after while loop: {temp}")
            print(f"for char:{ch}, stack outside while loop: {stack}")
            stack.pop()  # remove "("
            # Push reversed substring back
            for x in temp:
                stack.append(x)

    return "".join(stack)


# Test
print("Reverse parentheses:", reverse_parentheses("abc(def)ghi"), "\n\n\n")  # "iloveu"
print("Reverse parentheses:", reverse_parentheses("(u(love)i)"), "\n\n\n")  # "iloveu"
print("Reverse parentheses:", reverse_parentheses("a(bc(de)f)g"), "\n\n\n")  # "afedcbg"
