s = [1, 2, 3, '4', 5, 6]

while s:
    a = s[-1]
    s = s[:-1]
    try:
        print(a + 1)
    except TypeError:
        print('error!')
        continue
    finally:
        print('me too')
