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
            print(f"[if] for char:{ch}, stack in if condition: {stack}")
        else:
            temp = []
            # Pop until "("
            while stack and stack[-1] != "(":
                temp.append(stack.pop())
            print(f"[else] for char:{ch}, temp after while loop: {temp}")
            print(f"[else] for char:{ch}, stack after while loop: {stack}")
            stack.pop()  # remove "("
            # Push reversed substring back
            for x in temp:
                stack.append(x)
            print(f"[else] Final Stack for char: {ch}: {stack}")

    return "".join(stack)


# Test
print("Reverse parentheses:", reverse_parentheses("abc(def)ghi"), "\n\n\n")  # "abcfedghi"
print("Reverse parentheses:", reverse_parentheses("(u(love)i)"), "\n\n\n")  # "iloveu"
print("Reverse parentheses:", reverse_parentheses("a(bc(de)f)g"), "\n\n\n")  # "afedcbg"
