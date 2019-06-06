
import numpy


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