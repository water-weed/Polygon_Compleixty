import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def scan_convert_image(image_path, padding=16):
    """
    将图像转换为 256x256 的二值图像并加上 padding.
    """
    img = Image.open(image_path).convert('L')  # 转为灰度图
    img = np.array(img)
    
    # 调整图像大小为 256x256，并添加填充
    img_resized = cv2.resize(img, (256 - 2 * padding, 256 - 2 * padding), interpolation=cv2.INTER_NEAREST)
    
    # 在四周添加填充
    img_padded = np.pad(img_resized, pad_width=padding, mode='constant', constant_values=0)
    
    # 二值化处理
    _, binary_img = cv2.threshold(img_padded, 128, 255, cv2.THRESH_BINARY)
    
    return binary_img

def downsample_image_with_fixed_grid(binary_img, grid_size, threshold=0.1):
    """
    按固定大小的网格（例如 2x2 像素）对图像进行降采样，保持图像大小不变。
    :param binary_img: 输入二值化图像
    :param grid_size: 固定网格的大小（每个网格是 grid_size x grid_size 像素）
    :param threshold: 网格中白色像素比例的阈值
    :return: 降采样后的图像以及降采样后所占据的面积比
    """
    img_h, img_w = binary_img.shape
    downsampled_img = np.zeros_like(binary_img)

    total_occupied_pixels = 0

    # 遍历每个网格
    for i in range(0, img_h, grid_size):
        for j in range(0, img_w, grid_size):
            # 提取当前网格中的像素区域
            grid_region = binary_img[i:i + grid_size, j:j + grid_size]

            # 计算该网格中的白色像素比例
            white_pixel_ratio = np.sum(grid_region == 255) / grid_region.size

            # 如果白色像素比例大于设定阈值，则认为该网格中形状占据
            if white_pixel_ratio > threshold:
                downsampled_img[i:i + grid_size, j:j + grid_size] = 255
                total_occupied_pixels += np.sum(grid_region == 255)  # 计算白色像素数量

    # 计算原始图像的白色像素总数
    original_occupied_pixels = np.sum(binary_img == 255)
    
    # 计算面积比
    if original_occupied_pixels > 0:
        area_ratio = total_occupied_pixels / original_occupied_pixels
    else:
        area_ratio = 0  # 避免除以零的情况

    return downsampled_img, area_ratio

# 示例：读取图像并进行按固定网格大小的降采样
binary_img = scan_convert_image('./selection/deer-2.gif')

# 使用不同的固定网格大小进行降采样
grid_sizes = [2, 4, 8, 16]  # 每个网格的大小是 2x2、4x4、8x8、16x16 像素
for grid_size in grid_sizes:
    downsampled_img, area_ratio = downsample_image_with_fixed_grid(binary_img, grid_size, threshold=0.5)
    print(f'网格大小 {grid_size}x{grid_size} 像素的区域面积比: {area_ratio}')

    # 显示降采样后的图像
    plt.figure()
    plt.imshow(downsampled_img, cmap='gray')
    plt.title(f'Downsampled with grid size {grid_size}x{grid_size}')
    plt.show()
