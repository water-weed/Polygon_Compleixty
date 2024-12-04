import numpy as np
import cv2
from PIL import Image

def Boundary(url):
    img = Image.open(url).convert('L')  # 转为灰度图
    img = np.array(img)

    _, binary_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # 行方向的变化（上下）
    row_changes = np.sum(binary_img[:-1, :] != binary_img[1:, :])

    # 列方向的变化（左右）
    col_changes = np.sum(binary_img[:, :-1] != binary_img[:, 1:])

    total_changes = 2*(row_changes + col_changes)  # 总变化次数

    # 获取图像的宽度和高度
    rows, cols = binary_img.shape

    # 计算最大边界变化次数（面积归一化公式）
    max_changes = 2 * (rows * (cols - 1) + cols * (rows - 1))

    # 归一化复杂度
    complexity = total_changes / max_changes

    result = {}
    result['complexity'] = str(complexity)
    result['total_changes'] = str(total_changes)
    result['max_changes'] = str(max_changes)
    result['size_width'] = str(rows)
    result['size_length'] = str(cols)
    print(result)
    return result
