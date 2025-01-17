import time
import cv2 as cv
import pyautogui as autogui

autogui.PAUSE = 0.1
autogui.FAILSAFE = True

# path是模板路径


def getxy(path):
    # 屏幕截图保存的位置：
    autogui.screenshot().save("./picture/screenshot.png")

    # img存储屏幕截图
    img = cv.imread("./picture/screenshot.png")

    # 用于匹配的图像模板
    img_sunny = cv.imread("./picture/sunny.jpg")

    # 读取模板的宽度和高度
    length, high = img_sunny.shape  # 返回长与宽

    # 进行模板匹配  三个参数依次为图像 模板 检测方法
    result = cv.matchTemplate(img, img_sunny, cv.TM_CCOEFF_NORMED)

    # 解析匹配区域的坐标
    upleft = cv.minMaxLoc(result[2])  # result是一个数组 有四个值 第三个值是左上角坐标

    # 计算匹配区域右下角坐标
    lowerright = (upleft[0]+length, upleft[1]+high)

    # 计算中心坐标
    middle = (int((lowerright[0]+upleft[0])/2),
              int((lowerright[1]+upleft[1])/2))
    return middle


def auto_click(xy):
    autogui.click(xy[0], xy[1], button='left')  # 左键点击
    time.sleep(0.1)
    return 0


def routine(path, name):

    # 封装
    xy = getxy(path)
    printf("click is executing . . .")
    auto_click(xy)

routine("./picture/sunny","阳光")