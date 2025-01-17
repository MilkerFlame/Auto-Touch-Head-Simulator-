import time
import cv2
import pyautogui


def findandclick():
    # 寻找表情
    try:
        xy = pyautogui.locateOnScreen('./picture/emoj.png', confidence=0.8)

        if xy is not None:
            print('找到了1')
            # 找到了
            pyautogui.leftClick(xy[0],xy[1])
            xy2 = pyautogui.locateOnScreen('./picture/mt.png', confidence=0.8)
            if xy2 is not None:
                print('找到了2')
                pyautogui.leftClick(xy2[0],xy2[1])
            else:
                print("没找到2")
        else:
            print("没找到1")
    except pyautogui.ImageNotFoundException:
        print("图片未找到，等待1秒后重试")

    return 1


while True:
    time.sleep(1)
    findandclick()
