"""
    该自动连连看脚本
    默认是针对不随着进度变化的界面操作的（省时间）
    若需要针对动态游戏，则将@1处相关代码去注释即可
"""
from image_get import *
from graph_path import connect_find
import pyautogui
import time


def auto_game_init(windows_title):
    # 获取窗口左上角坐标
    win_start = get_windows(windows_title)
    # 获取游戏区坐标
    game_area = get_game_area(*win_start)
    return game_area


def get_game_matrix(game_area):
    # 获取游戏区域图像
    game_area_image = grab_game_area(*game_area)
    # 将一张图像切割为多个项目图
    images = game_area_image_to_item_images(game_area_image)
    # 将多个项目图像转换为矩阵
    matrix = images_to_matrix(images)
    return matrix


def execute_one_step(one_step, game_area,
                     item_width, item_height):
    from_row, from_col, to_row, to_col = one_step
    game_area_left, game_area_top, right, bottom = game_area

    from_x = game_area_left + (from_col + 0.5) * item_width
    from_y = game_area_top + (from_row + 0.5) * item_height

    to_x = game_area_left + (to_col + 0.5) * item_width
    to_y = game_area_top + (to_row + 0.5) * item_height

    pyautogui.moveTo(from_x, from_y)
    pyautogui.click()

    pyautogui.moveTo(to_x, to_y)
    pyautogui.click()


if __name__ == '__main__':
    game_area = auto_game_init('连连看 v4.1')
    while True:
        matrix = get_game_matrix(game_area)

        # 扩展外围
        col_max = item_count[0]
        row_max = item_count[1]
        matrix_ex = numpy.zeros((row_max + 2, col_max + 2), int)
        matrix_ex[1:(row_max + 1), 1:(col_max + 1)] = matrix

        while True:
            # 寻找可以连通的图标
            # 返回起点坐标和目标坐标

            print('------------------------------------------')
            print(matrix_ex, end='\n\n')
            one_step_ex = connect_find(matrix_ex)
            if not one_step_ex:
                print('----- 当前已没有可选择的路径 -----')
                time.sleep(0.25)
                break
                # exit(-1)

            # 执行实际操作
            one_step = tuple(map(lambda x: x - 1, one_step_ex))
            # 执行该步骤
            execute_one_step(
                one_step, game_area, *item_size)

            # 执行成功后，更新matrix
            from_row, from_col, to_row, to_col = one_step_ex
            matrix_ex[from_row][from_col] = 0
            matrix_ex[to_row][to_col] = 0

            if numpy.all(matrix_ex == 0):
                error_exit('----- 通关完成 -----')
                exit(0)

            # @1 执行成功一步之后，延时一会儿
            # 重新截图，方便处理动态变化的图像

            # time.sleep(0.25)
            # break
