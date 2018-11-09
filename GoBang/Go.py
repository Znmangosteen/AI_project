import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


class AI(object):
    # my_value_set = [1, 10454, 4731, 2447, 1731, 1547, 656, 453, 256, 120, 42, 5]
    # his_value_set = [1, 9610, 3606, 1961, 1225, 1143, 500, 416, 242, 75, 26, 8]
    my_value_set = [1, 104540, 47310, 2447, 1731, 1547, 656, 453, 256, 120, 42, 5]
    his_value_set = [1, 96100, 36060, 1961, 1225, 1143, 500, 416, 242, 75, 26, 8]

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
        best_value = 0
        best_point = []
        total_value2 = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)

        for p in idx:
            total_value = 0
            current_value = self.getValueAt(chessboard, p, self.color)
            total_value2[p[0], p[1]] += current_value
            total_value += current_value

            current_value = self.getValueAt(chessboard, p, -self.color)
            total_value2[p[0], p[1]] += current_value
            total_value += current_value

            if total_value > best_value:
                best_value = total_value
                best_point = p

        if serch_range.__len__() == 0:
            best_point = ((int)(self.chessboard_size / 2), (int)(self.chessboard_size / 2))

        if best_point == []:
            pos_idx = random.randint(0, len(idx) - 1)
            best_point = idx[pos_idx]

        self.candidate_list.append(best_point)

        for p in serch_range:
            serch_range.remove(p)
            self.findMin(chessboard, p, 1, idx)

            serch_range.append(p)

        # =====================================
        assert chessboard[best_point[0], best_point[1]] == COLOR_NONE
        self.candidate_list.append(best_point)

    def getValueAt(self, chessboard, point, current_color):
        value = 0

        type = self.getType(chessboard, point, current_color)

        # 判断value
        if current_color == self.color:
            value_set = self.my_value_set
        else:
            value_set = self.his_value_set

        value += type['five'] * value_set[1]
        value += type['alive4'] * value_set[2]
        if type['death4'] + type['lowdeath4'] >= 2 or (
                type['death4'] + type['lowdeath4'] >= 1 and type['alive3'] + type['tiao3'] >= 1):
            value += value_set[2] - 3000
        else:
            value += type['death4'] * value_set[3]
            value += type['lowdeath4'] * value_set[3]
        if type['alive3'] + type['tiao3'] >= 2:
            value += 15000
        value += type['alive3'] * value_set[4]
        value += type['tiao3'] * value_set[5]
        value += type['death3'] * value_set[6]
        value += type['alive2'] * value_set[7]
        value += type['lowalive2'] * value_set[8]
        value += type['death2'] * value_set[9]
        value += type['alive1'] * value_set[10]
        value += type['death1'] * value_set[11]
        return value

    def getType(self, chessboard, point, current_color):
        type = {'five': 0, 'alive4': 0, 'death4': 0, 'death3': 0, 'death2': 0, 'lowdeath4': 0, 'alive3': 0, 'alive2': 0,
                'lowalive2': 0, 'tiao3': 0, 'alive1': 0, 'death1': 0, 'NOTHREAT': 0}

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
                    elif (right_2 == current_color and (right_3 == -current_color or right_3 == 2)) or (
                            left_2 == current_color and (left_3 == -current_color or left_3 == 2)):
                        type['death3'] += 1
                    elif (right_2 == current_color and right_3 == current_color) or (
                            left_2 == current_color and left_3 == current_color):
                        type['death4'] += 1
                    elif (right_2 == current_color and right_3 == COLOR_NONE) or (
                            left_2 == current_color and left_3 == COLOR_NONE):
                        type['tiao3'] += 1
                    else:
                        type['death2'] += 1
                elif (left == 2 or left == -current_color) and (right == 2 or right == -current_color):
                    type['NOTHREAT'] += 1
                elif left == COLOR_NONE or right == COLOR_NONE:
                    if left == -current_color or left == 2:
                        if right_2 == -current_color or right_2 == 2 or right_3 == -current_color or right_3 == 2:
                            type['NOTHREAT'] += 1
                        elif right_2 == COLOR_NONE and right_3 == COLOR_NONE:
                            type['death2'] += 1
                        elif right_2 == current_color and right_3 == current_color:
                            type['lowdeath4'] += 1
                        elif right_2 == current_color or right_3 == current_color:
                            type['death3'] += 1

                    elif right == -current_color or right == 2:
                        if left_2 == -current_color or left_2 == 2 or left_3 == -current_color or left_3 == 2:
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

                elif left == COLOR_NONE and left_2 == COLOR_NONE and left_3 == COLOR_NONE and left_4 == COLOR_NONE and (
                        right == -current_color or right == 2):
                    type['death1'] += 1
                elif right == COLOR_NONE and right_2 == COLOR_NONE and right_3 == COLOR_NONE and right_4 == COLOR_NONE and (
                        left == -current_color or left == 2):
                    type['death1'] += 1

                elif left == COLOR_NONE and left_2 == COLOR_NONE and left_3 == COLOR_NONE and right == COLOR_NONE:
                    type['alive1'] += 1
                elif right == COLOR_NONE and right_2 == COLOR_NONE and right_3 == COLOR_NONE and left == COLOR_NONE:
                    type['alive1'] += 1

                elif left == COLOR_NONE and left_2 == COLOR_NONE and right_2 == COLOR_NONE and right == COLOR_NONE:
                    type['alive1'] += 1

                else:
                    type['NOTHREAT'] += 1
        return type

    def getGoAt(self, chessboard, point, dir, offset):
        x = point[0]
        y = point[1]

        x += self.dir_set[dir][0] * offset
        y += self.dir_set[dir][1] * offset
        if (x > -1) and (x < self.chessboard_size) and (y > -1) and (y < self.chessboard_size):
            return chessboard[x][y]
        else:
            return 2

    def findMin(self, chessboard, point, depth, empty: list):
        endType = self.getType(chessboard, point, self.color)
        if (endType['five'] > 0):
            return 100000
        elif depth > 8:
            return 0

        chessboard[point[0], point[1]] = self.color
        value = 1000000

        for p in empty:

            if self.goDeep(chessboard, point):
                empty.remove(p)
                next_level_value = self.finMax(chessboard, point, depth + 1, empty)
                if next_level_value == -1000000:
                    chessboard[point[0], point[1]] = 0
                    return next_level_value
                value = min(value, next_level_value)
                empty.append(p)

        chessboard[point[0], point[1]] = 0
        return value

    def finMax(self, chessboard, point, depth, empty):
        endType = self.getType(chessboard, point, -self.color)
        if (endType['five'] > 0):
            return 100000
        elif depth > 8:
            return 0

        chessboard[point[0], point[1]] = -self.color
        value = -1000000

        for p in empty:

            if self.goDeep(chessboard, point):
                empty.remove(p)
                next_level_value = self.findMin(chessboard, point, depth + 1, empty)
                if next_level_value == 1000000:
                    chessboard[point[0], point[1]] = 0
                    return next_level_value
                value = min(value, next_level_value)
                empty.append(p)

        chessboard[point[0], point[1]] = 0
        return value

    def goDeep(self, chessboard, point):
        current_type = self.getType(chessboard, point, self.color)
        current_type2 = self.getType(chessboard, point, -self.color)
        if (current_type['five'] + current_type['alive4'] + current_type['death4'] + current_type['lowdeath4'] +
                current_type['alive3'] + current_type['tiao3'] +
                current_type2['five'] + current_type2['alive4'] + current_type2['death4'] + current_type2['lowdeath4'] +
                current_type2['alive3'] + current_type2['tiao3']):
            return True
        else:
            return False
