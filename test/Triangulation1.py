from shapely.geometry import Polygon, LineString
from shapely.ops import triangulate
from foronoi import Voronoi,Visualizer
import matplotlib.pyplot as plt
import foronoi
import triangle

# 检查多边形是否为简单多边形
def is_simple_polygon(polygon_edges):
    polygon = Polygon(polygon_edges)
    return polygon.is_simple

def triangulate_with_triangle(polygon):
    """
    使用 Triangle 库对多边形进行约束 Delaunay 三角剖分。
    """
    # 转换 Shapely Polygon 为 Triangle 输入格式
    points = list(polygon.exterior.coords)  # 顶点
    segments = [(i, (i + 1) % len(points)) for i in range(len(points) - 1)]  # 边界

    # 定义 Triangle 输入
    data = {
        'vertices': points,
        'segments': segments
    }

    # 调用 Triangle 库进行三角剖分
    result = triangle.triangulate(data, 'p')  # 'p' 参数保留边界

    # 提取剖分后的三角形
    triangles = []
    for tri in result['triangles']:
        triangles.append([tuple(result['vertices'][i]) for i in tri])

    return triangles

# 处理跨越边界的三角形
def process_triangle(triangle, polygon):
    """
    切割跨越边界的三角形，保留合法部分。
    """
    triangle_polygon = Polygon(triangle)
    if polygon.contains(triangle_polygon):
        return [triangle_polygon]  # 完全在多边形内，直接保留
    elif polygon.intersects(triangle_polygon):
        intersection = polygon.intersection(triangle_polygon)
        if isinstance(intersection, Polygon):
            triangles = triangulate_with_triangle(intersection)
            #return [Polygon(tri) for tri in triangles]  # 保留交集部分
            return intersection 
            #return triangulate[intersection]
        elif isinstance(intersection, LineString):
            return []  # 如果交集是线，忽略
    return []  # 完全在多边形外，删除

# 使用 foronoi 生成 Delaunay 三角剖分
def compute_delaunay_with_edges(points, polygon_edges):
    bounding_poly = foronoi.Polygon([[0, 0],[500, 0],[500, 500],[0, 500]])
    voronoi = Voronoi(bounding_poly)
    voronoi.create_diagram(points)
    Visualizer(voronoi) \
        .plot_sites(show_labels=False) \
        .plot_edges(show_labels=False) \
        .plot_vertices() \
        .show()

    delaunay_triangles = []
    polygon = Polygon([edge[0] for edge in polygon_edges])

    # 提取 Delaunay 三角形
    for vertex in voronoi.vertices:  # 遍历每个 Voronoi 顶点
        triangle_vertices = set()  # 存储三角剖分的顶点
        
        for point in voronoi.sites:
            if vertex in point.vertices():
                triangle_vertices.add(point.xy)

        # 如果找到三个顶点，形成一个三角形
        if len(triangle_vertices) == 3:
            triangle = list(sorted(triangle_vertices))
            processed_triangles = process_triangle(triangle, polygon)
            #delaunay_triangles.extend([Polygon(triangle)])
            delaunay_triangles.extend(processed_triangles)

    # 去重（避免重复三角形）
    delaunay_triangles = list(set(delaunay_triangles))

    return delaunay_triangles

# 计算 t₀
def calculate_t0(triangles, polygon_edges):
    polygon_edge_set = set(tuple(sorted(edge)) for edge in polygon_edges)

    t0 = 0

    for triangle in triangles:
        # 提取三角形的三条边
        edges = [
            tuple(sorted((triangle.exterior.coords[0], triangle.exterior.coords[1]))),
            tuple(sorted((triangle.exterior.coords[1], triangle.exterior.coords[2]))),
            tuple(sorted((triangle.exterior.coords[2], triangle.exterior.coords[0]))),
        ]

        # 检查是否所有边都是自由边
        if all(edge not in polygon_edge_set for edge in edges):
            t0 += 1

    return t0

# 绘制 Delaunay 三角剖分
def plot_delaunay(delaunay_triangles,polygon_edges):
    plt.figure(figsize=(6, 6))

    # 绘制多边形边界
    for edge in polygon_edges:
        x = [edge[0][0], edge[1][0]]
        y = [edge[0][1], edge[1][1]]
        plt.plot(x, y, 'g-', linewidth=2, label="Polygon Edge")

    # 绘制 Delaunay 三角剖分
    for triangle in delaunay_triangles:
        x, y = zip(*triangle.exterior.coords)
        plt.plot(x, y, 'b-', alpha=0.7)

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
    points = [(239.41665649414062, 155.16665649414062), (283.4166564941406, 191.16665649414062),
              (317.4166564941406, 161.16665649414062), (347.4166564941406, 121.16665649414062), 
              (366.4166564941406, 185.16665649414062), (386.4166564941406, 243.16665649414062), 
              (427.4166564941406, 240.16665649414062), (431.4166564941406, 237.16665649414062), 
              (453.4166564941406, 292.1666564941406), (449.4166564941406, 344.1666564941406), 
              (448.4166564941406, 418.1666564941406), (370.4166564941406, 451.1666564941406), 
              (341.4166564941406, 452.1666564941406), (339.4166564941406, 397.1666564941406), 
              (353.4166564941406, 383.1666564941406), (319.4166564941406, 352.1666564941406), 
              (309.4166564941406, 361.1666564941406), (268.4166564941406, 425.1666564941406), 
              (259.4166564941406, 455.1666564941406), (207.41665649414062, 469.1666564941406), 
              (183.41665649414062, 454.1666564941406), (142.41665649414062, 411.1666564941406), 
              (137.41665649414062, 353.1666564941406), (183.41665649414062, 318.1666564941406), 
              (217.41665649414062, 325.1666564941406), (280.4166564941406, 299.1666564941406), 
              (215.41665649414062, 263.1666564941406), (165.41665649414062, 291.1666564941406), 
              (115.41665649414062, 289.1666564941406), (97.41665649414062, 223.16665649414062), 
              (123.41665649414062, 178.16665649414062), (166.41665649414062, 162.16665649414062), 
              (189.41665649414062, 200.16665649414062), (217.41665649414062, 189.16665649414062), 
              (221.41665649414062, 159.16665649414062)]
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
    #print(polygon_edges)

    # 检查多边形是否简单
    if is_simple_polygon(points):
        print("多边形是简单多边形")

        # 生成 Delaunay 三角剖分
        delaunay_triangles = compute_delaunay_with_edges(points,polygon_edges)

        # 绘制三角剖分
        plot_delaunay(delaunay_triangles,polygon_edges)

        # 计算 t₀
        t0_value = calculate_t0(delaunay_triangles, polygon_edges)
        print(f"t₀ 值为: {t0_value}")

    else:
        print("多边形不是简单多边形，请修复输入！")
