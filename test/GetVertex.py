import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def GetVertex(url):
# Step 1: 读取图像
    img = Image.open(url).convert('L')  # 'L' 模式表示灰度图
    img = np.array(img)  # 转换为 NumPy 数组，用于 OpenCV 处理
    
    _, img_thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)

    # 使用形态学操作去除细小噪声和锯齿
    kernel = np.ones((3, 3), np.uint8)
    img_morph = cv2.morphologyEx(img_thresh, cv2.MORPH_OPEN, kernel)

    # 边缘检测
    edges = cv2.Canny(img_morph, 50, 150)

    # 找到轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 使用多边形逼近
    epsilon = 0.001 * cv2.arcLength(contours[0], True)
    approx = cv2.approxPolyDP(contours[0], epsilon, True)

    # 绘制多边形顶点
    img_poly = np.zeros_like(img)
    cv2.drawContours(img_poly, [approx], -1, (255, 255, 255), 2)

    # 显示结果
    plt.figure(figsize=(6, 6))
    plt.imshow(img_poly, cmap='gray')
    plt.title('Detected Complex Polygon')
    plt.show()

    # 打印顶点坐标
    polygon_vertices = approx[:, 0, :]
    print("Vertex")
    print(polygon_vertices)

    return polygon_vertices

#cv2.imshow("Gray Image", gray)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

"""# Step 2: 使用 Canny 边缘检测
edges = cv2.Canny(gray, 50, 150)

# Step 3: 找到轮廓
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Step 4: 多边形逼近 (找到多边形的顶点)
epsilon = 0.01 * cv2.arcLength(contours[0], True)  # 逼近精度
approx = cv2.approxPolyDP(contours[0], epsilon, True)  # 使用多边形逼近

# 获取顶点坐标
polygon_vertices = approx[:, 0, :]  # 获取所有顶点坐标

# 打印多边形顶点
print("Vertex：")
for point in polygon_vertices:
    print(point)

# 可视化结果
img_with_polygon = img.copy()
cv2.drawContours(img_with_polygon, [approx], 0, (0, 255, 0), 3)  # 绘制多边形轮廓

# 使用matplotlib展示图像
plt.figure(figsize=(6, 6))
plt.imshow(cv2.cvtColor(img_with_polygon, cv2.COLOR_BGR2RGB))
plt.title('Detected Polygon')
plt.show()"""

"""
使用霍夫变换检测直线
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
print(edges)

# Step 3: 使用霍夫变换检测直线
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=30, maxLineGap=10)
print(lines)

# 在图像上绘制直线
img_with_lines = img.copy()
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img_with_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 显示结果
plt.figure(figsize=(6, 6))
plt.imshow(cv2.cvtColor(img_with_lines, cv2.COLOR_BGR2RGB))
plt.title('Detected Lines with Hough Transform')
plt.show()"""

"""
# Step 2: 使用高斯模糊去噪
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Step 3: 使用自适应阈值
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Step 4: 找到轮廓
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Step 5: 使用多边形逼近
epsilon = 0.01 * cv2.arcLength(contours[0], True)
approx = cv2.approxPolyDP(contours[0], epsilon, True)

# 获取多边形顶点
polygon_vertices = approx[:, 0, :]

# 可视化结果
img_with_polygon = img.copy()
cv2.drawContours(img_with_polygon, [approx], 0, (0, 255, 0), 3)

plt.figure(figsize=(6, 6))
plt.imshow(cv2.cvtColor(img_with_polygon, cv2.COLOR_BGR2RGB))
plt.title('Detected Complex Polygon')
plt.show()
"""


