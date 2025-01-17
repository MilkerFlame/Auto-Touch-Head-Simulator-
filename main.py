import time
import cv2 as cv
import pyautogui as autogui
import numpy as np

autogui.PAUSE = 0.1
autogui.FAILSAFE = True

def preprocess_image(img):
    # 转换为灰度图
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # 直方图均衡化
    equalized = cv.equalizeHist(gray)
    
    # 高斯模糊降噪
    blurred = cv.GaussianBlur(equalized, (5, 5), 0)
    
    return blurred

def getxy(path):
    # 屏幕截图保存的位置：
    autogui.screenshot().save("./picture/screenshot.png")

    # img存储屏幕截图
    img = cv.imread("./picture/screenshot.png")
    if img is None:
        raise Exception("无法加载屏幕截图")
        
    # 预处理截图
    img = preprocess_image(img)

    # 用于匹配的图像模板
    img_sunny = cv.imread("./picture/image.png")
    if img_sunny is None:
        raise Exception("无法加载模板图片")
        
    # 预处理模板
    img_sunny = preprocess_image(img_sunny)

    # 读取模板的宽度和高度
    length, high = img_sunny.shape  # 返回长与宽

    # 打印图片尺寸信息
    print(f"屏幕截图尺寸: {img.shape}")
    print(f"模板图片尺寸: {img_sunny.shape}")
    
    # 尝试多种匹配方法
    methods = [
        ('TM_CCOEFF_NORMED', cv.TM_CCOEFF_NORMED),
        ('TM_SQDIFF_NORMED', cv.TM_SQDIFF_NORMED),
        ('TM_CCORR_NORMED', cv.TM_CCORR_NORMED)
    ]
    
    best_match = {'method': '', 'max_val': 0, 'max_loc': (0,0)}
    
    for method_name, method in methods:
        result = cv.matchTemplate(img, img_sunny, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        
        # 对于SQDIFF方法，使用最小值
        if method == cv.TM_SQDIFF_NORMED:
            val = 1 - min_val
            loc = min_loc
        else:
            val = max_val
            loc = max_loc
            
        print(f"方法 {method_name} 匹配值: {val}")
        
        if val > best_match['max_val']:
            best_match = {
                'method': method_name,
                'max_val': val,
                'max_loc': loc
            }
    
    print(f"最佳匹配方法: {best_match['method']}, 匹配值: {best_match['max_val']}")
    
    # 设置匹配阈值
    threshold = 0.7  # 降低匹配阈值
    print(f"当前匹配值: {best_match['max_val']}, 阈值: {threshold}")
    if best_match['max_val'] < threshold:
        raise Exception(f"未找到匹配目标 (匹配值: {best_match['max_val']}, 需要: {threshold})")
        
    # 解析匹配区域的坐标
    upleft = best_match['max_loc']  # 使用最佳匹配位置

    # 计算中心坐标
    # 调整y坐标偏移量，因为截图可能包含窗口标题栏
    y_offset = 30  # 根据实际情况调整
    middle = (upleft[0] + length//2,
              upleft[1] + high//2 + y_offset)
    return middle

def auto_click(xy):
    autogui.click(xy[0], xy[1], button='left')  # 左键点击
    time.sleep(0.1)
    return 0

def routine(path, name):
    while True:
        try:
            # 获取匹配位置
            xy = getxy(path)
            
            # 如果找到匹配则点击
            print("Target found, clicking...")
            auto_click(xy)
            
            # 点击后等待1秒
            time.sleep(1)
            
        except Exception as e:
            # 未找到匹配时等待0.5秒后重试
            print("Target not found, waiting...")
            time.sleep(2)

routine("./picture/image.png","阳光")
