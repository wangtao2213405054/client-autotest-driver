
data = dict(
    test=123,
    test1=23
)

data1 = data.pop('test2', None)

print(data1, data)
