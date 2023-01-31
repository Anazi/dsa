def reverse_triangle(levels: int):
    if levels == 0:
        return ''

    print('*'*levels)

    return reverse_triangle(levels=levels - 1)


print(reverse_triangle(levels=5))


def triangle(levels: int):
    if levels == 0:
        return ''

    triangle(levels=levels - 1)

    print('*' * levels)
    return ''


print(triangle(levels=5))
