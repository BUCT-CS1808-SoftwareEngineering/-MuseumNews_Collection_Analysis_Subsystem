def subStr(a, b):
    len1 = len(a)
    len2 = len(b)
    flag = 0
    for i in range(len1 - len2 + 1):
        if a[i:i + len2] == b:
            flag = i + len2
            break
    return a[:flag]
