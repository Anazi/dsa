"""
1️⃣ First Non-Repeating Character in a String
Problem

Given a string s, return the first character that appears exactly once.
If none exists, return None.

1️⃣ Intuition

You want:

Characters that occur once

And among those, the one that appears earliest

So you need two things at the same time:

    a. Count of characters

    b. Original order information

2️⃣ Why this is a Strings + Hashing problem

Strings alone → you can traverse characters

But checking frequency efficiently requires constant-time lookup

Hash maps give:

char → count

O(1) updates and reads

👉 Arrays alone fail unless the alphabet is strictly fixed (e.g., ASCII 26 lowercase letters).

aabcbcdee
{
    a: 2,
    b: 1+1,
    c: 1+1,
    d: 1,
    e: 1+1
}
"""

def non_repeating_char_in_a_string(s: str):
    char_counter = {}
    for char in s:
        if char in char_counter.keys():
            char_counter[char] += 1
        else:
            char_counter[char] = 1

    for k,v in char_counter.items():
        if v == 1:
            return k
        

t_str = aabcbcdee
print(f"non_repeating_char_in_a_string for string:{t_str} is `{non_repeating_char_in_a_string(t_str)}`")

