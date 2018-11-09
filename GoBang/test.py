import imp
import traceback
import sys
import os
import numpy as np
import Go

# # a=[1,2,3,4,5,6,7]
# # print(a[:4:1])
#
# # offset = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1))
# # print(offset[0][1])
#
# idx = [[0, 0, 1, 2],[2, 3, 4, 5]]
# # idx[0] = [0, 0, 1, 2]
# # idx[1] = [2, 3, 4, 5]
#
# idx = list(zip(idx[0], idx[1]))
# print((1,4)in idx)
# for i in range(8):
#     print(i)
#
# for i in range(8):
#     if i<5:
#         if i<2:
#             print(i)
#         else:
#             break

# type = {'five': 0, 'alive4': 0}
# type['alive4']+=1
# print(type['alive4'])
chessboard = np.zeros((15, 15), dtype=np.int)
agent = Go.AI(15, -1, 5)
# x = int(input())
#
# while x != 100:
#     y = int(input())
#     value = int(input())
#     chessboard[x, y] = value
#     x = int(input())
matrix=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, -1, -1, -1, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, -1, 1, 1, 0, -1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, -1, -1, 1, -1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, -1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, -1, 0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

for i in range(15):
    for j in range(15):
        chessboard[i,j]=matrix[i][j]

agent.go(np.copy(chessboard))
print(chessboard)
print()
print(agent.candidate_list)