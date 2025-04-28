"""
    Given a Polish (prefix) notation expression like:
        * + 2 3 4
    Evaluate it.

    Polish Notation Rules:
        Operators come before operands.

    For example, * + 2 3 4 means:
        * (2 + 3) 4
        → (2+3) = 5 → 5×4 = 20
"""


class PolishNotationEval:
    """
    💡Key Observations
        - Operators come first, operands come later.
        - Need to process from right to left (because first you need operands, then operator applies).
        - Use a stack to evaluate.

    🎯 Why This Is Best Solution
        - Reverse traversal correctly handles Polish notation.
        - Stack gives immediate access to operands.
        - Very clean, O(N) time, O(N) space.
    """

    def __init__(self):
        pass

    def evaluate_polish(self, tokens):
        stack = []

        for token in reversed(tokens):
            print(f'token ongoing: {token}, stack: {stack}')
            #   Because the token is reversed, numbers will go first in stack (else condition)
            if token in {"+", "-", "*", "/"}:
                # Pop two operands for the operator from the "STACK", so they will always be the right numbers
                a = stack.pop()
                b = stack.pop()

                print(f"token: {token}, a={a}, b={b}, r_tokens: {reversed(tokens)}")
                # Apply operator
                if token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "*":
                    stack.append(a * b)
                else:
                    stack.append(a / b)

            else:
                # Token is a number, push onto stack
                stack.append(int(token))
        return stack[0]


t_tokens1 = ["-", "/", "10", "+", "1", "1", "*", "1", "2"]
t_tokens = ['*', '+', '2', '3', '4']
polish_eval_obj = PolishNotationEval()
polish_val = polish_eval_obj.evaluate_polish(t_tokens)
print(f"polish evaluation t_tokens: {polish_eval_obj.evaluate_polish(t_tokens)}\n\n\n============\n\n")
print(f"polish evaluation t_tokens1: {polish_eval_obj.evaluate_polish(t_tokens1)}\n\n\n")

"""
    🧠 How to Identify Such Problems
        Signs:        
            - "Prefix Expression" or "Polish Notation" keyword.        
            - Operator appears before operands.
        
        Examples:
            * + 1 2 3            
            + * 2 3 * 4 5
    
    ⚡ How to Solve Quickly in Interview
        If prefix / Polish → read Right to Left.
        
        - Use a stack:
            - If number → push.            
            - If operator → pop two numbers, apply operator, push result.
        
        Final answer will be single element on stack.
    
    🎓 How to Master This Type
        Polish/Prefix → RIGHT to LEFT + Stack
        
        Postfix/Reverse Polish → LEFT to RIGHT + Stack
        
        
        Type	Traverse Direction	Stack Usage
        Polish (prefix)	Right → Left	Push numbers, apply operators immediately
        Reverse Polish (postfix)	Left → Right	Push numbers, apply operators immediately
"""
