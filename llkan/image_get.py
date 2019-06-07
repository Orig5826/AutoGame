"""
    # 调试参数
    DEBUG_SWITCH  # 1.开启 0.关闭

    # 游戏参数相关说明：
    item_count 项目数
    item_size 每项尺寸
    area_start 游戏区左上角相对于窗口左上角的坐标
"""
import win32api
import win32gui
import win32con

import PIL.ImageGrab

import numpy
import os

from image_contrast import image_contrast

# 调试开关
DEBUG_SWITCH = 0    # 1.开启 0.关闭


"""
# ---------- 连连看 v4.1 初级 ----------
# 项目数：每行，每列
item_count = (12, 7)
# 每项尺寸：宽，高
item_size = (40, 50)
# 游戏区左上角相对于窗口左上角的坐标：left，top
area_start = (164, 162)

# ---------- 连连看 v4.1 特高 ----------
# 项目数：每行，每列
item_count = (18, 10)
# 每项尺寸：宽，高
item_size = (40, 50)
# 游戏区左上角相对于窗口左上角的坐标：left，top
area_start = (41, 64)
"""

# ---------- QQ游戏 - 连连看角色版 ----------
# 项目数：每行，每列
item_count = (19, 11)
# 每项尺寸：宽，高
item_size = (31, 35)
# 游戏区左上角相对于窗口左上角的坐标：left，top
area_start = (14, 181)


def error_exit(des):
    print(des)
    exit(-1)


def get_screen_size():
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    print('屏幕分辨率:\n\twidth,height = {0},{1}'.format(
        screen_width, screen_height))
    return (screen_width, screen_height)


def get_windows(window_title):
    # 获取窗口
    hwnd = win32gui.FindWindow(win32con.NULL, window_title)
    if hwnd == 0:
        error_exit('"%s" not found' % window_title)

    # 前置 + 激活
    win32gui.SetForegroundWindow(hwnd)
    win32gui.SetActiveWindow(hwnd)

    # 获取屏幕分辨率
    screen_width, screen_height = get_screen_size()

    window_left, window_top, window_right, window_bottom =\
        win32gui.GetWindowRect(hwnd)
    print('游戏窗口坐标:\n\tleft,top = {0},{1}\n\tright,bottom = \
{2},{3}'.format(window_left, window_top,
                window_right, window_bottom))

    if min(window_left, window_top) < 0\
            or window_right > screen_width\
            or window_bottom > screen_height:
        error_exit('window is at wrong position')

    """
    window_width = window_right - window_left
    window_height = window_bottom - window_top
    print('----- 程序窗口尺寸 -----')
    print('窗口尺寸:\nwidth,height = {0},{1}'.format(
        window_width, window_height))
    """
    # 获取左上角坐标
    return (window_left, window_top)


def get_game_area(win_left, win_top):
    game_area_left = win_left + area_start[0]
    game_area_top = win_top + area_start[1]
    game_area_right = game_area_left + item_count[0] * item_size[0]
    game_area_bottom = game_area_top + item_count[1] * item_size[1]
    print('游戏区坐标:\n\tleft,top = {0},{1}\n\tright,bottom = \
{2},{3}'.format(game_area_left,
                game_area_top,
                game_area_right,
                game_area_bottom))
    return (game_area_left, game_area_top, game_area_right, game_area_bottom)


def grab_game_area(left, top, right, bottom):
    game_area_image = PIL.ImageGrab.grab((left, top, right, bottom))
    if DEBUG_SWITCH == 1:
        game_area_image.save('llk_.png', 'PNG')
    # game_area_image.show()
    return game_area_image


def get_item_image(image, left, top, right, bottom):
    if DEBUG_SWITCH == 1:
        # 调试阶段，可以恢复为全部，方便调试
        item_image = image.crop((left, top, right, bottom))
    else:
        # 去掉边缘，防止因为边界花边造成对判断的影响
        item_image = image.crop((left + 2, top + 2, right - 2, bottom - 2))
    # item_image.show()
    return item_image


def game_area_image_to_item_images(gram_area_image):
    row_max = item_count[1]
    col_max = item_count[0]

    item_width = item_size[0]
    item_height = item_size[1]

    # 记录每个单独的图像
    item_images = {}
    for row in range(row_max):
        item_images[row] = {}
        for col in range(col_max):
            item_left = col * item_width
            item_top = row * item_height
            item_right = item_left + item_width
            item_bottom = item_top + item_height

            item_image = get_item_image(gram_area_image,
                                        item_left, item_top,
                                        item_right, item_bottom)

            if DEBUG_SWITCH == 1:
                if not os.path.exists('./img'):
                    os.mkdir('./img')
                item_image.save(
                    './img/{}.png'.format(row*col_max + col + 1), 'PNG')

            item_images[row][col] = item_image

    return item_images


def is_empty_item(image):
    im = image
    # 针对 "练练看 v4.1"
    # 我手动去掉了背景，要不然这些影响，我目前还处理不了
    center = im.resize(size=(int(im.width / 4.0), int(im.height / 4.0)
                             ),
                       box=(int(im.width / 4.0), int(im.height / 4.0),
                            int(im.width / 4.0 * 3.0),
                            int(im.height / 4.0 * 3.0)
                            )
                       )

    for color in center.getdata():
        # 因为当前背景被我配置为了纯黑色
        # if color != (0, 0, 0):
        if color != (48, 76, 112):
            return False
    return True


def same_item(image_a, image_b):
    numpy_array_a = numpy.array(image_a)
    numpy_array_b = numpy.array(image_b)
    return image_contrast(numpy_array_a, numpy_array_b)


def images_to_matrix(images):
    row_max = item_count[1]
    col_max = item_count[0]

    item_width = item_size[0]
    item_height = item_size[1]

    # 记录独立的图像
    image_record = []
    item_matirx = numpy.zeros((row_max, col_max), int)
    for row in range(row_max):
        for col in range(col_max):
            # 当前图像
            cur_image = images[row][col]

            same_flag = False
            if not is_empty_item(images[row][col]):
                for index in range(len(image_record)):
                    if same_item(image_record[index], cur_image):
                        id = index + 1
                        item_matirx[row][col] = id
                        same_flag = True
                        break

                # 若没有找到相似
                if not same_flag:
                    image_record.append(cur_image)
                    id = len(image_record)
                    item_matirx[row][col] = id

    # print(item_matirx)
    return item_matirx


if __name__ == '__main__':
    # 获取窗口左上角坐标
    win_start = get_windows('连连看 v4.1')
    # 获取游戏区坐标
    game_area = get_game_area(*win_start)
    # 获取游戏区域图像
    game_area_image = grab_game_area(*game_area)
    # 将一张图像切割为多个项目图
    images = game_area_image_to_item_images(game_area_image)
    # 将多个项目图像转换为矩阵
    matrix = images_to_matrix(images)
