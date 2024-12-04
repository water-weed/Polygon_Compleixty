import numpy as np
import cv2
from PIL import Image

# 读取图像并二值化
img = Image.open('./selection/spring-2.gif').convert('L')  # 转为灰度图
img = np.array(img)

_, binary_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
binary_img = np.array([[0,1,0,0],
                       [1,0,1,1],
                       [0,1,0,1],
                       [0,0,0,1]])

# 计算实际的边界变化次数
#row_changes = np.sum(np.abs(np.diff(binary_img, axis=1)) > 0)  # 行方向变化
#col_changes = np.sum(np.abs(np.diff(binary_img, axis=0)) > 0)  # 列方向变化
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

print(f"图像尺寸: {rows}x{cols}")
print(f"总边界长度: {total_changes}")
print(f"最大边界变化次数: {max_changes}")
print(f"归一化复杂度（基于面积）: {complexity:.4f}")
