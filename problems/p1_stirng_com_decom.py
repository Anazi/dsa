"""
Problem Statement
We are given a string like:

"aaabbbccd"

We need to:

- Compress it into character + count format:
"aaabbbccd" → "a3b3c2d1"

- Decompress it back to the original string:
"a3b3c2d1" → "aaabbbccd"
"""


class StringCompressionDecompression:
    """
        Why This Is Best Solution
            Linear Scan: We only go through the string once.

            No unnecessary extra space except output.

            Handles multi-digit counts (e.g., if aaaaaaaa... 100 times → a100).
    """

    def __init__(self):
        pass

    def compress_string(self, input_string) -> str:

        result = []

        i = 0
        while i < len(input_string):
            count = 1
            # Count consecutive same characters
            while i + 1 < len(input_string) and input_string[i] == input_string[i + 1]:
                count += 1
                i += 1
            # Append character and its count
            result.append(input_string[i] + str(count))
            i += 1
        return ''.join(result)

    def decompress_string(self, input_string):
        """
        Input string: "a12"
            You start after 'a':
            - At i=1:
                s[i] = '1'
                count = 0 * 10 + 1 = 1
            - Move i=2:
                s[i] = '2'
                count = 1 * 10 + 2 = 12
        """
        result = []

        i = 0
        while i < len(input_string):
            char = input_string[i]

            count = 0
            while i + 1 < len(input_string) and input_string[i + 1].isdigit():
                count = count * 10 + int(input_string[i + 1])
                i += 1

            result.append(char * count)
            i += 1
        return ''.join(result)


com_decom_obj = StringCompressionDecompression()
original = "aaaaaaabbbbbbbbbccddddddddddddddddddd"  #"aaaaaaabbbbbbbbbccddddddddddddddddddd"
compressed = com_decom_obj.compress_string(original)
print("Compressed:", compressed)  # Output: a3b3c2d1 || a7b9c2d19
decompressed = com_decom_obj.decompress_string(compressed)
print("Decompressed:", decompressed)  # Output: aaabbbccd || aaaaaaabbbbbbbbbccddddddddddddddddddd


"""
    ⚡ How to Solve Quickly in Interview
        Compression:
            Walk through string, count consecutive same chars.
            
            Append char + count.
        
        Decompression:
            Read character.
            
            Read digits after it (multi-digit possible).
            
            Expand character.
    
    ============
    
    🎓 How to Master This Type
        Practice string traversal carefully.
        
        Remember the pattern:
        "[char][number] → expand"
        
        Watch for edge cases:
        
        Single character.
        
        Large counts (more than 9).
"""