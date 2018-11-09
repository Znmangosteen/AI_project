matrix=[[0 for i in range(15)]for i in range(15)]
print(matrix)
x = int(input())

while x != 100:
    y = int(input())
    value = int(input())
    matrix[x, y] = value
    x = int(input())

#
# class A:
#     def c