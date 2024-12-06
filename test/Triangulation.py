from shapely.geometry import Polygon
from foronoi import Voronoi,Visualizer
import matplotlib.pyplot as plt
import foronoi

# 检查多边形是否为简单多边形
def is_simple_polygon(polygon_edges):
    polygon = Polygon(polygon_edges)
    return polygon.is_simple

# 使用 foronoi 生成 Delaunay 三角剖分
def compute_delaunay_with_edges(points):
    bounding_poly = foronoi.Polygon([[0, 0],[500, 0],[500, 500],[0, 500]])
    voronoi = Voronoi(bounding_poly)
    voronoi.create_diagram(points)
    Visualizer(voronoi) \
        .plot_sites(show_labels=False) \
        .plot_edges(show_labels=False) \
        .plot_vertices() \
        .show()

    delaunay_triangles = []
    delaunay_edges = []

    # 提取 Delaunay 三角形
    for vertex in voronoi.vertices:  # 遍历每个 Voronoi 顶点
        triangle_vertices = set()  # 存储三角剖分的顶点
        
        for point in voronoi.sites:
            if vertex in point.vertices():
                triangle_vertices.add(point.xy)

        # 如果找到三个顶点，形成一个三角形
        if len(triangle_vertices) == 3:
            delaunay_triangles.append(tuple(sorted(triangle_vertices)))
            edge_vertices = list(triangle_vertices)
            delaunay_edges.append(tuple([
                tuple(sorted((edge_vertices[0], edge_vertices[1]))),
                tuple(sorted((edge_vertices[1], edge_vertices[2]))),
                tuple(sorted((edge_vertices[2], edge_vertices[0])))]
            ))

    # 去重（避免重复三角形）
    delaunay_triangles = list(set(delaunay_triangles))
    delaunay_edges = list(set(delaunay_edges))

    return delaunay_triangles, delaunay_edges

# 计算 t₀
def calculate_t0(triangles, polygon_edges):
    polygon_edge_set = set(
        tuple(sorted([(x1, y1), (x2, y2)]))
        for (x1, y1), (x2, y2) in polygon_edges
    )

    t0 = 0

    for triangle in triangles:
        edges = [
            tuple(sorted([(triangle[0], triangle[1])])),
            tuple(sorted([(triangle[1], triangle[2])])),
            tuple(sorted([(triangle[2], triangle[0])])),
        ]
        if all(edge[0] not in polygon_edge_set for edge in edges):
            t0 += 1
    return t0

# 绘制 Delaunay 三角剖分
def plot_delaunay(delaunay_triangles):
    plt.figure(figsize=(6, 6))

    # 遍历每个三角形
    for triangle in delaunay_triangles:
        # 提取三角形的顶点坐标
        x = [triangle[0][0], triangle[1][0], triangle[2][0], triangle[0][0]]
        y = [triangle[0][1], triangle[1][1], triangle[2][1], triangle[0][1]]

        # 绘制三角形
        plt.plot(x, y, 'k-', alpha=0.7)  # 边界线

    # 配置图形
    plt.title("Delaunay Triangulation")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')  # 保证比例尺一致
    plt.show()

# 测试示例
if __name__ == "__main__":
    # 点集
    points = [(281.4166564941406, 192.13540649414062), (280.4166564941406, 338.1354064941406), 
              (142.41665649414062, 318.1354064941406), (133.41665649414062, 207.13540649414062), 
              (182.41665649414062, 206.13540649414062), (193.41665649414062, 255.13540649414062), 
              (236.41665649414062, 255.13540649414062)]
    polygon_edges = []

    fig, ax = plt.subplots()

    # 创建多边形并添加到图中
    polygon = plt.Polygon(points, closed=True, edgecolor='black', alpha=0.7)
    ax.add_patch(polygon)

    # 调整坐标范围以适应多边形
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 500)

    # 显示绘图
    plt.gca().set_aspect('equal', adjustable='box')  # 确保多边形比例正确
    plt.show()

    for i in range(len(points)-1):
        polygon_edges.append([points[i],points[i+1]])
    polygon_edges.append([points[len(points)-1], points[0]])
    print(polygon_edges)

    # 检查多边形是否简单
    if is_simple_polygon(points):
        print("多边形是简单多边形")

        # 生成 Delaunay 三角剖分
        delaunay_triangles, delaunay_edges = compute_delaunay_with_edges(points)

        # 绘制三角剖分
        plot_delaunay(delaunay_triangles)

        # 计算 t₀
        t0_value = calculate_t0(delaunay_triangles, polygon_edges)
        print(f"t₀ 值为: {t0_value}")

    else:
        print("多边形不是简单多边形，请修复输入！")
