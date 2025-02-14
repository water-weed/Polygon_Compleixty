import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import cv2
from shapely.geometry import Polygon
import triangle as tr  # 约束三角剖分库

# 读取图像并提取轮廓
def extract_polygon_from_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No contours found in image.")
    polygon = contours[0].squeeze()
    if polygon.ndim != 2 or polygon.shape[1] != 2:
        raise ValueError("Extracted polygon has an invalid shape.")
    return np.array(polygon, dtype=np.float64)

# 绘制三角剖分（调整样式使其类似示例图）
def plot_triangulation(points, triangles, title, polygon_outline=None):
    plt.figure(figsize=(6,6))
    plt.triplot(points[:, 0], points[:, 1], triangles, color='blue', lw=1.0, alpha=0.7)
    if polygon_outline is not None:
        plt.plot(polygon_outline[:, 0], polygon_outline[:, 1], color='blue', lw=2)
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis('equal')
    plt.grid(True)

# 读取输入图片
image_path = "./selection/file20.jpg"  # 替换为你的图像路径
polygon_points = extract_polygon_from_image(image_path)

if polygon_points.size == 0:
    raise ValueError("Extracted polygon points are empty. Check input image.")

# 1. Delaunay 三角剖分
tri = Delaunay(polygon_points)
plot_triangulation(polygon_points, tri.simplices, "Delaunay Triangulation", polygon_outline=polygon_points)

# 2. 约束三角剖分（使用 Triangle 库）
polygon_dict = {
    'vertices': polygon_points,
    'segments': [[i, (i+1)%len(polygon_points)] for i in range(len(polygon_points))]  # 定义边界
}
triangulated = tr.triangulate(polygon_dict, 'p')
if 'triangles' in triangulated:
    plot_triangulation(triangulated['vertices'], triangulated['triangles'], "Constrained Triangulation", polygon_outline=polygon_points)
else:
    print("Triangle triangulation failed: No valid triangles.")

# 显示图像
plt.show()
