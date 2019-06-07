"""
    image contrast
    执行该脚本前，请先执行picture_splist.py，以便于生成供该脚本使用的源文件
"""
import cv2
import numpy as np


def normalization(image, size=(64, 64)):
    """
        归一化
    """
    return cv2.resize(image, size)


def grayscale(image):
    """
        灰度化处理
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def get_hash(image):
    """
        获取信息指纹
    """
    # print(image.shape)
    average = np.mean(image)
    hash = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i][j] > average:
                hash.append(1)
            else:
                hash.append(0)
    return hash


def hammming_distance(hash1, hash2):
    length = len(hash1)
    if length != len(hash2):
        raise Exception("汉明距离：信息指纹长度不相等")

    count = 0
    for i in range(length):
        if hash1[i] != hash2[i]:
            count += 1
    return count


def classify_aHash(image1, image2):
    """
        平均哈希
    """
    image1 = normalization(image1, size=(32, 32))
    image2 = normalization(image2, size=(32, 32))
    gray1 = grayscale(image1)
    gray2 = grayscale(image2)
    # Test
    # cv2.imshow('gray_1', gray1)
    # cv2.imshow('gray_2', gray2)

    hash1 = get_hash(gray1)
    hash2 = get_hash(gray2)
    return hammming_distance(hash1, hash2)


def classify_aHash(image1, image2):
    """
        平均哈希
        计算平均值，误差很大
    """
    image1 = normalization(image1, size=(32, 32))
    image2 = normalization(image2, size=(32, 32))
    gray1 = grayscale(image1)
    gray2 = grayscale(image2)
    # Test
    # cv2.imshow('gray_1', gray1)
    # cv2.imshow('gray_2', gray2)

    hash1 = get_hash(gray1)
    hash2 = get_hash(gray2)
    return hammming_distance(hash1, hash2)


def classify_pHash(image1, image2):
    """
        感知哈希
        精确，但计算速度过慢
    """
    image1 = normalization(image1, size=(32, 32))
    image2 = normalization(image2, size=(32, 32))
    gray1 = grayscale(image1)
    gray2 = grayscale(image2)

    # 将灰度图转为浮点型，再进行dct变换
    dct1 = cv2.dct(np.float32(gray1))
    dct2 = cv2.dct(np.float32(gray2))
    # 缩小DCT，保留左上角8*8的像素
    dct1_roi = dct1[0:8, 0:8]
    dct2_roi = dct2[0:8, 0:8]

    hash1 = get_hash(dct1_roi)
    hash2 = get_hash(dct2_roi)
    return hammming_distance(hash1, hash2)


def image_contrast(image1, image2, hashmode='P'):
    if hashmode == 'A':
        hamm_dis = classify_aHash(image1, image2)
        # print('classify_aHash: ', hamm_dis)
        if hamm_dis > 10:
            return False
        return True
    elif hashmode == 'P':
        hamm_dis = classify_pHash(image1, image2)
        # print('classify_pHash: ', hamm_dis)
        if hamm_dis > 3:
            return False
        return True


def contrast_test():
    picture1 = './img/4.png'
    picture2 = './img/36.png'
    picture3 = './img/14.png'

    # 直接获取灰度图
    # img1 = cv2.imread(picture1, 0)
    img1 = cv2.imread(picture1)
    img2 = cv2.imread(picture2)
    img3 = cv2.imread(picture3)

    # Test
    # cv2.imshow('image_1', img1)
    # cv2.imshow('image_2', img2)
    # cv2.imshow('image_3', img3)

    result = image_contrast(img1, img2)
    print(result)
    result = image_contrast(img1, img3)
    print(result)

    # 延时毫秒数，0表示无穷大(相当于暂停)
    # 给imshow提供延时
    cv2.waitKey(0)


if __name__ == "__main__":
    contrast_test()
