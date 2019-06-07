"""
    利用pillow模块[py3]
    来切割图片
"""
from PIL import Image
import os


def get_image(filename):
    return Image.open(filename)


def cut_image(image, row=1, col=1):
    width, height = image.size
    print('image: width,height = {},{}'.format(width, height))

    item_width = width // col
    item_height = height // row
    print('item: width,height = {},{}'.format(item_width, item_height))

    # 增加一些偏移量
    box_offset = (5, 5, -5, -5)
    box_list = []
    for i in range(0, row):
        for j in range(0, col):
            box = (j*item_width, i*item_height, (j+1)*item_width,
                   (i+1)*item_height)
            tmp = map(lambda x, y: x + y, box, box_offset)
            box = tuple(tmp)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list


def save_images(image_list):
    path_name = './img'
    if not os.path.exists(path_name):
        os.mkdir(path_name)
    index = 1
    for image in image_list:
        image.save(path_name + '/' + str(index) + '.png', 'PNG')
        index += 1


if __name__ == '__main__':
    filename = "llk_Q.png"
    image = get_image(filename)
    # image_list = cut_image(image, 7, 12)
    image_list = cut_image(image, 11, 19)
    save_images(image_list)
