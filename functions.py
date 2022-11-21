def make_dict(a):
    list = dict(a)
    for i in a:
        list[i] = dict(a[i])
        for j in list[i]:
            list[i][j] = dict(a[i][j])
    return list
 