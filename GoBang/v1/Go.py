import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


class AI(object):
    dir_set = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1))
    value_set = [1, 100000, 10000, 5000, 1000, 500, 400, 100, 90, 50, 10, 9, 5, 2]

    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []

    def go(self, chessboard):
        self.candidate_list.clear()

        # =====================================
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        # pos_idx = random.randint(0, len(idx) - 1)
        # new_pos = idx[pos_idx]
        serch_range = []

        for p in idx:
            for i in range(8):
                x = p[0] + self.dir_set[i][0]
                y = p[1] + self.dir_set[i][1]

                if (x > -1) and (x < self.chessboard_size) and (y > -1) and (y < self.chessboard_size):
                    if chessboard[x][y] != COLOR_NONE:
                        serch_range.append(p)
                        break

                x += self.dir_set[i][0]
                y += self.dir_set[i][1]
                if (x > -1) and (x < self.chessboard_size) and (y > -1) and (y < self.chessboard_size):
                    if chessboard[x][y] != COLOR_NONE:
                        serch_range.append(p)
                        break
        att_best_value = 0
        def_best_value = 0
        best_att_point = []
        best_def_point = []

        for p in serch_range:
            current_value = self.getValueAt(chessboard, p, self.color)
            if current_value > att_best_value:
                att_best_value = current_value
                best_att_point = p

            current_value = self.getValueAt(chessboard, p, -self.color)
            if current_value > def_best_value:
                def_best_value = current_value
                best_def_point = p

        if att_best_value >= def_best_value:
            best_point = best_att_point
        else:
            best_point = best_def_point
        if serch_range.__len__() == 0:
            best_point = ((int)(self.chessboard_size / 2), (int)(self.chessboard_size / 2))

        # =====================================
        assert chessboard[best_point[0], best_point[1]] == COLOR_NONE
        self.candidate_list.append(best_point)

    def getValueAt(self, chessboard, point, current_color):
        value = 0

        type = {'five': 0, 'alive4': 0, 'death4': 0, 'death3': 0, 'death2': 0, 'lowdeath4': 0, 'alive3': 0, 'alive2': 0,
                'lowalive2': 0, 'tiao3': 0, 'NOTHREAT': 0}

        # 四个方向
        for dir in range(4):
            count = 1
            left_stop = 1
            right_stop = 1
            # 左右各搜四步
            for i in range(4):
                offset = i + 1
                if self.getGoAt(chessboard, point, 2 * dir, offset) == current_color:
                    left_stop += 1
                    count += 1
                else:
                    break
            for i in range(4):
                offset = i + 1
                if self.getGoAt(chessboard, point, 2 * dir + 1, offset) == current_color:
                    right_stop += 1
                    count += 1
                else:
                    break

            # 搜棋形 返回的棋-1 1 0 2
            if count >= 5:
                type['five'] += 1
            elif count == 4:
                left = self.getGoAt(chessboard, point, 2 * dir, left_stop)
                right = self.getGoAt(chessboard, point, 2 * dir + 1, right_stop)
                if left == COLOR_NONE and right == COLOR_NONE:
                    type['alive4'] += 1
                elif left != COLOR_NONE and right != COLOR_NONE:
                    type['NOTHREAT'] += 1
                elif left == COLOR_NONE or right == COLOR_NONE:
                    type['death4'] += 1
            elif count == 3:
                left = self.getGoAt(chessboard, point, 2 * dir, left_stop)
                right = self.getGoAt(chessboard, point, 2 * dir + 1, right_stop)
                left_2 = self.getGoAt(chessboard, point, 2 * dir, left_stop + 1)
                right_2 = self.getGoAt(chessboard, point, 2 * dir + 1, right_stop + 1)

                if left == COLOR_NONE and right == COLOR_NONE:
                    if (left_2 == -current_color or left_2 == 2) and (right_2 == -current_color or right_2 == 2):
                        type['death3'] += 1
                    elif left_2 == current_color or right_2 == current_color:
                        type['lowdeath4'] += 1
                    elif left_2 == COLOR_NONE or right_2 == COLOR_NONE:
                        type['alive3'] += 1
                elif (left == -current_color or left == 2) and (right == -current_color or right == 2):
                    type['NOTHREAT'] += 1
                elif left == COLOR_NONE or right == COLOR_NONE:
                    if left == -current_color or left == 2:
                        if right_2 == -current_color or right_2 == 2:
                            type['NOTHREAT'] += 1
                        elif right_2 == COLOR_NONE:
                            type['death3'] += 1
                        elif right_2 == current_color:
                            type['lowdeath4'] += 1
                    if right == -current_color or right == 2:
                        if left_2 == -current_color or left_2 == 2:
                            type['NOTHREAT'] += 1
                        elif left_2 == COLOR_NONE:
                            type['death3'] += 1
                        elif left_2 == current_color:
                            type['lowdeath4'] += 1
            elif count == 2:
                left = self.getGoAt(chessboard, point, 2 * dir, left_stop)
                right = self.getGoAt(chessboard, point, 2 * dir + 1, right_stop)
                left_2 = self.getGoAt(chessboard, point, 2 * dir, left_stop + 1)
                right_2 = self.getGoAt(chessboard, point, 2 * dir + 1, right_stop + 1)
                left_3 = self.getGoAt(chessboard, point, 2 * dir, left_stop + 2)
                right_3 = self.getGoAt(chessboard, point, 2 * dir + 1, right_stop + 2)

                if left == COLOR_NONE and right == COLOR_NONE:
                    if (right_2 == COLOR_NONE and right_3 == current_color) or (
                            left_2 == COLOR_NONE and left_3 == current_color):
                        type['death3'] += 1
                    elif left_2 == COLOR_NONE and right_2 == COLOR_NONE:
                        type['alive2'] += 1
                    elif (right_2 == current_color and right_3 == -current_color) or (
                            left_2 == current_color and left_3 == -current_color):
                        type['death3'] += 1
                    elif (right_2 == current_color and right_3 == current_color) or (
                            left_2 == current_color and left_3 == current_color):
                        type['death4'] += 1
                    elif (right_2 == current_color and right_3 == COLOR_NONE) or (
                            left_2 == current_color and left_3 == COLOR_NONE):
                        type['tiao3'] += 1
                elif (left == 2 or left == -current_color) and (right == 2 or right == -current_color):
                    type['NOTHREAT'] += 1
                elif left == COLOR_NONE or right == COLOR_NONE:
                    if left == -current_color:
                        if right_2 == -current_color or right_3 == -current_color:
                            type['NOTHREAT'] += 1
                        elif right_2 == COLOR_NONE and right_3 == COLOR_NONE:
                            type['death2'] += 1
                        elif right_2 == current_color and right_3 == current_color:
                            type['lowdeath4'] += 1
                        elif right_2 == current_color or right_3 == current_color:
                            type['death3'] += 1

                    elif right == -current_color:
                        if left_2 == -current_color or left_3 == -current_color:
                            type['NOTHREAT'] += 1
                        elif left_2 == COLOR_NONE and left_3 == COLOR_NONE:
                            type['death2'] += 1
                        elif left_2 == current_color and left_3 == current_color:
                            type['lowdeath4'] += 1
                        elif left_2 == current_color or left_3 == current_color:
                            type['death3'] += 1
            elif count == 1:
                left = self.getGoAt(chessboard, point, 2 * dir, left_stop)
                right = self.getGoAt(chessboard, point, 2 * dir + 1, right_stop)
                left_2 = self.getGoAt(chessboard, point, 2 * dir, left_stop + 1)
                right_2 = self.getGoAt(chessboard, point, 2 * dir + 1, right_stop + 1)
                left_3 = self.getGoAt(chessboard, point, 2 * dir, left_stop + 2)
                right_3 = self.getGoAt(chessboard, point, 2 * dir + 1, right_stop + 2)
                left_4 = self.getGoAt(chessboard, point, 2 * dir, left_stop + 3)
                right_4 = self.getGoAt(chessboard, point, 2 * dir + 1, right_stop + 3)

                if left == COLOR_NONE and left_2 == current_color and left_3 == current_color and left_4 == current_color:
                    type['lowdeath4'] += 1
                elif right == COLOR_NONE and right_2 == current_color and right_3 == current_color and right_4 == current_color:
                    type['lowdeath4'] += 1

                elif left == COLOR_NONE and left_2 == current_color and left_3 == current_color and left_4 == COLOR_NONE and right == COLOR_NONE:
                    type['tiao3'] += 1
                elif right == COLOR_NONE and right_2 == current_color and right_3 == current_color and right_4 == COLOR_NONE and left == COLOR_NONE:
                    type['tiao3'] += 1

                elif left == COLOR_NONE and left_2 == current_color and left_3 == current_color and left_4 == -current_color and right == COLOR_NONE:
                    type['death3'] += 1
                elif right == COLOR_NONE and right_2 == current_color and right_3 == current_color and right_4 - current_color and left == COLOR_NONE:
                    type['death3'] += 1

                elif left == COLOR_NONE and left_2 == COLOR_NONE and left_3 == current_color and left_4 == current_color:
                    type['death3'] += 1
                elif right == COLOR_NONE and right_2 == COLOR_NONE and right_3 == current_color and right_4 == current_color:
                    type['death3'] += 1

                elif left == COLOR_NONE and left_2 == current_color and left_3 == COLOR_NONE and left_4 == current_color:
                    type['death3'] += 1
                elif right == COLOR_NONE and right_2 == current_color and right_3 == COLOR_NONE and right_4 == current_color:
                    type['death3'] += 1

                elif left == COLOR_NONE and left_2 == current_color and left_3 == COLOR_NONE and left_4 == COLOR_NONE and right == COLOR_NONE:
                    type['lowalive2'] += 1
                elif right == COLOR_NONE and right_2 == current_color and right_3 == COLOR_NONE and right_4 == COLOR_NONE and left == COLOR_NONE:
                    type['lowalive2'] += 1

                elif left == COLOR_NONE and left_2 == COLOR_NONE and left_3 == current_color and left_4 == COLOR_NONE and right == COLOR_NONE:
                    type['lowalive2'] += 1
                elif right == COLOR_NONE and right_2 == COLOR_NONE and right_3 == current_color and right_4 == COLOR_NONE and left == COLOR_NONE:
                    type['lowalive2'] += 1

                else:
                    type['NOTHREAT'] += 1

            # 判断value
            if type['five'] >= 1:
                value += self.value_set[1]
            elif type['alive4'] >= 1 or type['death4'] >= 2 or (type['death4'] >= 1 and type['alive3'] >= 1) or (
                    type['death4'] >= 1 and type['tiao3'] >= 1):
                value += self.value_set[2]
            elif type['alive3'] >= 2:
                value += self.value_set[3]
            elif type['death3'] >= 1 and type['alive3'] >= 1:
                value += self.value_set[4]
            elif type['death4'] >= 1:
                value += self.value_set[5]
            elif type['lowdeath4'] >= 1:
                value += self.value_set[6]
            elif type['alive3'] >= 1:
                value += self.value_set[7]
            elif type['tiao3'] >= 1:
                value += self.value_set[8]
            elif type['alive2'] >= 2:
                value += self.value_set[9]
            elif type['alive2'] >= 1:
                value += self.value_set[10]
            elif type['lowalive2'] >= 1:
                value += self.value_set[11]
            elif type['death3'] >= 1:
                value += self.value_set[12]
            elif type['death2'] >= 1:
                value += self.value_set[13]
            else:
                value += self.value_set[0]

        return value

    def getGoAt(self, chessboard, point, dir, offset):
        x = point[0]
        y = point[1]

        x += self.dir_set[dir][0] * offset
        y += self.dir_set[dir][1] * offset
        if (x > -1) and (x < self.chessboard_size) and (y > -1) and (y < self.chessboard_size):
            return chessboard[x][y]
        else:
            return 2
