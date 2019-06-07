
import numpy


def connect_zero_corner(matrix, pos_src, pos_des):
    # 起点行，起点列，目标行，目标列
    s_r, s_c = pos_src
    d_r, d_c = pos_des
    # print(s_r, s_c)
    # print(d_r, d_c)

    # 横向判断
    if s_r == d_r:
        col_min = min(s_c, d_c)
        col_max = max(s_c, d_c)

        if numpy.all(matrix[s_r, col_min+1:col_max] == 0):
            return (s_r, s_c, d_r, d_c)
    # 纵向判断
    if s_c == d_c:
        row_min = min(s_r, d_r)
        row_max = max(s_r, d_r)

        if numpy.all(matrix[row_min+1:row_max, s_c] == 0):
            return (s_r, s_c, d_r, d_c)

    return False


def connect_one_corner(matrix, pos_src, pos_des):
    # 起点行，起点列，目标行，目标列
    s_r, s_c = pos_src
    d_r, d_c = pos_des
    # print(s_r, s_c)
    # print(d_r, d_c)

    if s_r == d_r or s_c == d_c:
        return False

    if matrix[s_r][d_c] == 0:
        col_min = min(s_c, d_c)
        col_max = max(s_c, d_c)
        row_min = min(s_r, d_r)
        row_max = max(s_r, d_r)

        if numpy.all(matrix[s_r, col_min+1:col_max] == 0) and\
                numpy.all(matrix[row_min+1:row_max, d_c] == 0):
            return (s_r, s_c, d_r, d_c)
    if matrix[d_r][s_c] == 0:
        col_min = min(s_c, d_c)
        col_max = max(s_c, d_c)
        row_min = min(s_r, d_r)
        row_max = max(s_r, d_r)

        if numpy.all(matrix[d_r, col_min+1:col_max] == 0) and\
                numpy.all(matrix[row_min+1:row_max, s_c] == 0):
            return (s_r, s_c, d_r, d_c)

    return False


def connect_two_corner(matrix, pos_src, pos_des):
    """
        将两个拐角的问题，切换为源坐标横纵方向上所有
        空点的任意元素 与 目标点之间的一拐角问题
    """
    row_max = len(matrix)
    col_max = len(matrix[0])

    s_r, s_c = pos_src
    d_r, d_c = pos_des

    # 向上
    if s_r != 0:
        for r in range(s_r - 1, -1, -1):
            if matrix[r][s_c] == 0:
                pos = connect_one_corner(matrix, (r, s_c), pos_des)
                if pos is not False:
                    return (s_r, s_c, d_r, d_c)
            else:
                break
    # 向下
    if s_r != row_max:
        for r in range(s_r + 1, row_max, 1):
            if matrix[r][s_c] == 0:
                pos = connect_one_corner(matrix, (r, s_c), pos_des)
                if pos is not False:
                    return (s_r, s_c, d_r, d_c)
            else:
                break
    # 向左
    if s_c != 0:
        for c in range(s_c - 1, -1, -1):
            if matrix[s_r][c] == 0:
                pos = connect_one_corner(matrix, (s_r, c), pos_des)
                if pos is not False:
                    return (s_r, s_c, d_r, d_c)
            else:
                break
    # 向右
    if s_c != col_max:
        for c in range(s_c + 1, col_max, 1):
            if matrix[s_r][c] == 0:
                pos = connect_one_corner(matrix, (s_r, c), pos_des)
                if pos is not False:
                    return (s_r, s_c, d_r, d_c)
            else:
                break

    return False


def connect_find(matrix):
    row_max = len(matrix)
    col_max = len(matrix[0])

    max_id = numpy.max(matrix)
    for id in range(1, max_id + 1):
        # 获取相当元素位置信息
        pos = numpy.where(matrix == id)
        position = map(lambda x, y: (x, y), pos[0], pos[1])
        position = list(position)

        # 循环判断两坐标点是否连通
        pos_count = len(position)
        for i in range(pos_count):
            for j in range(i + 1, pos_count):
                pos_src = position[i]
                pos_des = position[j]
                # print('{} -> {}'.format(pos_src, pos_des))

                # 直线连通的判断
                pos = connect_zero_corner(matrix, pos_src, pos_des)
                if pos is not False:
                    return pos

    for id in range(1, max_id + 1):
        # 获取相当元素位置信息
        pos = numpy.where(matrix == id)
        position = map(lambda x, y: (x, y), pos[0], pos[1])
        position = list(position)

        # 循环判断两坐标点是否连通
        pos_count = len(position)
        for i in range(pos_count):
            for j in range(i + 1, pos_count):
                pos_src = position[i]
                pos_des = position[j]
                # print('{} -> {}'.format(pos_src, pos_des))

                # 有一个拐角连通的判断
                pos = connect_one_corner(matrix, pos_src, pos_des)
                if pos is not False:
                    return pos

    for id in range(1, max_id + 1):
        # 获取相当元素位置信息
        pos = numpy.where(matrix == id)
        position = map(lambda x, y: (x, y), pos[0], pos[1])
        position = list(position)

        # 循环判断两坐标点是否连通
        pos_count = len(position)
        for i in range(pos_count):
            for j in range(i + 1, pos_count):
                pos_src = position[i]
                pos_des = position[j]
                # print('{} -> {}'.format(pos_src, pos_des))

                # 有两个拐角连通的判断
                pos = connect_two_corner(matrix, pos_src, pos_des)
                if pos is not False:
                    return pos

    return False


if __name__ == '__main__':
    col_max = 12
    row_max = 7

    graph = numpy.array([[1, 2, 3, 2, 4, 5, 6, 7, 8, 7, 1, 9],
                         [10, 8, 11, 12, 13, 6, 4, 4, 14, 5, 14, 15],
                         [3, 16, 16, 3, 13, 17, 17, 18, 9, 5, 19, 17],
                         [15, 9, 12, 3, 7, 6, 1, 7, 12, 16, 8, 13],
                         [20, 11, 14, 11, 12, 21, 15, 20, 13, 10, 19, 16],
                         [9, 20, 10, 18, 21, 18, 10, 5, 11, 1, 15, 4],
                         [21, 2, 2, 19, 6, 19, 18, 17, 14, 8, 20, 21]])

    graph_ex = numpy.zeros((row_max + 2, col_max + 2), int)
    graph_ex[1:(row_max + 1), 1:(col_max + 1)] = graph
    print(graph_ex)
    ret = connect_find(graph_ex)
    print(ret)
