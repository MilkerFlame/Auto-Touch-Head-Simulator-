import time
import cv2
import pyautogui

img1 = './picture/image1.png'
img2 = './picture/image2.png'


def get_xy1_xy2():
    is_found1, is_found2 = True, True

    # 打开表情 记录并返回表情位置
    try:
        xy1 = pyautogui.locateOnScreen(img1, confidence=0.75)

        if xy1 is not None:
            print('xy1 is found')
            pyautogui.leftClick(xy[0], xy[1])
        else:
            print("xy1 can not be found . . .")
    except pyautogui.ImageNotFoundException:
        print("没找到xy1. . .")
        is_found1 = False

        
    print("停止0.2s")
    time.sleep(0.2)

    # 记录并返回摸头表情位置
    try:
        xy2 = pyautogui.locateOnScreen(img2, confidence=0.75)
        if xy2 is not None:
            print('xy2 is found')
            pyautogui.leftClick(xy2[0], xy2[1])
        else:
            print("xy2 can not be found")
    except pyautogui.ImageNotFoundException:
        print("没找到xy2. . .")
        is_found2 = False
    if (is_found1 and is_found2):
        return xy1, xy2
    elif (is_found1):
        print("你没有携带摸头表情")
    else:
        print("你不在决斗场中")
        return 0


def start(xy1, xy2):
    # 开始摸头!!!
    pyautogui.leftClick(xy[0], xy[1])
    time.sleep(0.1)
    pyautogui.leftClick(xy2[0], xy2[1])
    return 0


def routine():
    # 封装OK
    try:
        xy1, xy2 = get_xy1_xy2()
    except TypeError:
        return 1
    start(xy1, xy2)
    return 0


while True:
    key = input("输入OK开始摸头 输入EXIT以结束进程")
    if key == 'OK':
        while True:
            if (routine() == 1):
                break
    elif key == 'EXIT':
        print("无法退出-火影不是避风港,怕阴别来决斗场")
    else:
        print("输入错误")
