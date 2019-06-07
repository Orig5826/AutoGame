"""
    image contrast
    执行该脚本前，请先执行picture_splist.py，以便于生成供该脚本使用的源文件
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt


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


def classify_gray_hist(image1, image2, size=(256, 256)):
    """
        灰度直方图
        1. 灰度计算直方图，使用第一个通道
    """
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 可以比较下直方图
    plt.plot(range(256), hist1, 'r')
    plt.plot(range(256), hist2, 'b')
    plt.show()
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                (1 - abs(hist1[i]-hist2[i])/max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree/len(hist1)
    return degree


def calculate(image1, image2):
    """
        计算单通道的直方图的相似值
    """
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                (1 - abs(hist1[i]-hist2[i])/max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree/len(hist1)
    return degree


def classify_hist_with_split(image1, image2, size=(256, 256)):
    """
        通过得到每个通道的直方图来计算相似度
        将图像resize后，分离为三个通道，再计算每个通道的相似值
    """
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)

    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data/3
    return sub_data


def image_contrast(image1, image2, hashmode='H'):
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
    elif hashmode == 'H':
        degree = classify_hist_with_split(image1, image2, (32, 32))
        # print('hist_degree: ', degree)
        if degree > 0.95:
            return True
    elif hashmode == 'ht':
        # gray hist test
        classify_gray_hist(image1, image2)
    return False


def contrast_test():
    picture1 = './img/9.png'
    picture2 = './img/23.png'
    picture3 = './img/58.png'

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
