import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 读取图像并转换为二值图
img = Image.open('selection/apple-2.gif').convert('L')  # 读取并转换为灰度图
img = np.array(img)
_, binary_img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
original_area = np.sum(binary_img == 255)

def downsample_area(binary_img, grid_size):
    """
    将二值图像分成 grid_size x grid_size 的网格，计算每个网格内的面积占比
    :param binary_img: 二值化图像 (形状为白色，背景为黑色)
    :param grid_size: 网格的大小 (例如 128, 64, 32, 等)
    :return: 网格化后的面积占比图
    """
    img_h, img_w = binary_img.shape  # 获取图像的宽度和高度
    h_grid = img_h // grid_size  # 每个网格的高度
    w_grid = img_w // grid_size  # 每个网格的宽度

    # 创建一个空数组来存储每个网格的面积比例
    downsampled_area = np.zeros((grid_size, grid_size))

    # 遍历每个网格
    for i in range(grid_size):
        for j in range(grid_size):
            # 提取该网格的像素区域
            grid_region = binary_img[i * h_grid:(i + 1) * h_grid, j * w_grid:(j + 1) * w_grid]
            # 计算网格区域中白色像素的比例 (白色像素 = 255)
            area_fraction = np.sum(grid_region == 255) / (h_grid * w_grid)
            downsampled_area[i, j] = area_fraction  # 将该区域的占比存入结果矩阵中

    return downsampled_area

# 选择不同的网格分辨率
grid_sizes = [128, 64, 32, 16]

# 创建子图展示不同网格分辨率下的面积降采样结果
fig, axes = plt.subplots(1, len(grid_sizes), figsize=(15, 5))

for idx, grid_size in enumerate(grid_sizes):
    downsampled_areas = downsample_area(binary_img, grid_size)
    downsampled_area = np.sum(downsampled_areas) * (binary_img.size / downsampled_areas.size)
    complexity = 1 - (downsampled_area / original_area)
    axes[idx].imshow(downsampled_areas, cmap='gray')
    axes[idx].set_title(f'{grid_size}x{grid_size} Grid')
    print(f"{idx}:complexity:{complexity},original_area:{original_area},downsampled_area:{downsampled_area}")

plt.show()
