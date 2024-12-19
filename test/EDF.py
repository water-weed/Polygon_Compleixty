from skimage.morphology import medial_axis
from skimage import io
import numpy as np
from scipy.spatial import distance_matrix
import heapq
import matplotlib.pyplot as plt
from PIL import Image
import cv2

# 读取二值图像（白色区域为形状）
image = Image.open('selection/horse-2.gif').convert('L') #greyscale
image = np.array(image)
_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
#binary_image = io.imread("./selection/apple-2.gif", as_gray=True) > 0.5

# 计算中轴及边界距离
skeleton, distance = medial_axis(binary_image, return_distance=True)
radius_function = distance * skeleton
fig, axes = plt.subplots(1, 4, figsize=(20, 5))
axes[0].imshow(image, cmap="gray")
axes[0].set_title("Original Shape")

axes[1].imshow(skeleton, cmap="gray")
axes[1].set_title("Medial Axis (Skeleton)")

axes[2].imshow(distance, cmap="viridis")
axes[2].set_title("Distance Transform")

axes[3].imshow(radius_function, cmap="viridis")
axes[3].set_title("Radius Function (MAT)")

plt.show()

# 获取中轴点的坐标
skeleton_coords = np.column_stack(np.nonzero(skeleton))

# 构建点之间的距离矩阵
dist_matrix = distance_matrix(skeleton_coords, skeleton_coords)

# 定义邻接关系（例如仅保留欧几里得距离<=sqrt(2)的边）
adjacency_matrix = dist_matrix <= np.sqrt(2)

# 初始化
edf_values = np.full(len(skeleton_coords), np.inf)
priority_queue = []

# 设置初始值为边界距离
for i, (x, y) in enumerate(skeleton_coords):
    edf_values[i] = distance[x, y]
    heapq.heappush(priority_queue, (edf_values[i], i))  # (值, 索引)

# 扩展草火传播
while priority_queue:
    current_value, current_idx = heapq.heappop(priority_queue)
    if current_value > edf_values[current_idx]:
        continue  # 已处理更优路径

    for neighbor_idx in np.where(adjacency_matrix[current_idx])[0]:
        weight = dist_matrix[current_idx, neighbor_idx]
        new_value = edf_values[current_idx] + weight
        if new_value < edf_values[neighbor_idx]:
            edf_values[neighbor_idx] = new_value
            heapq.heappush(priority_queue, (new_value, neighbor_idx))

# 创建与原图大小一致的数组
edf_image = np.zeros_like(binary_image, dtype=float)

# 将EDF值填入对应的中轴点
for (x, y), edf in zip(skeleton_coords, edf_values):
    edf_image[x, y] = edf

# 可视化
plt.imshow(edf_image, cmap='viridis')
plt.colorbar(label='EDF Value')
plt.show()



