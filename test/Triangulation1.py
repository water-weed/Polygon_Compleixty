from shapely.geometry import Polygon, LineString
from shapely.ops import triangulate
from foronoi import Voronoi,Visualizer
import matplotlib.pyplot as plt
import foronoi
import triangle

# check if polygon is simple polygon
def is_simple_polygon(polygon_edges):
    polygon = Polygon(polygon_edges)
    return polygon.is_simple

def triangulate_with_triangle(polygon):
    """
    Use Triangle to Constrained Delaunay Triangulation (CDT)
    """
    # Convert Shapely Polygon to Triangle input data
    points = list(polygon.exterior.coords)  # Vertex
    segments = [(i, (i + 1) % len(points)) for i in range(len(points) - 1)]  # boundary

    # Define Triangle input
    data = {
        'vertices': points,
        'segments': segments
    }

    # Use Triangle to Triangulation
    result = triangle.triangulate(data, 'p')  # 'p' parameter preserve polygon border

    # Extract triangulation triangles
    triangles = []
    for tri in result['triangles']:
        triangles.append([tuple(result['vertices'][i]) for i in tri])

    return triangles

# process triangle across boundary
def process_triangle(triangle, polygon):
    """
    Cut triangles across boundary, preserve the part which is in the polygon
    """
    triangle_polygon = Polygon(triangle)
    if polygon.contains(triangle_polygon):
        return [triangle_polygon]  # Totally in the polygon, directly return
    elif polygon.intersects(triangle_polygon):
        intersection = polygon.intersection(triangle_polygon)
        if isinstance(intersection, Polygon):
            triangles = triangulate_with_triangle(intersection)
            #return [Polygon(tri) for tri in triangles]  
            return intersection #preserve intersection part
            #return triangulate[intersection]
        elif isinstance(intersection, LineString):
            return []  # If intersection part is line, ignore it
    return []  # totally out of polygon, delete

# Use foronoi generate Delaunay triangulation
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

    # Extract Delaunay polygon
    for vertex in voronoi.vertices:  # Iterate each Voronoi vertex
        triangle_vertices = set()  # Store the vertices of the triangulation
        
        for point in voronoi.sites:
            if vertex in point.vertices():
                triangle_vertices.add(point.xy)

        # If three vertices are found, a triangle is formed
        if len(triangle_vertices) == 3:
            triangle = list(sorted(triangle_vertices))
            processed_triangles = process_triangle(triangle, polygon)
            #delaunay_triangles.extend([Polygon(triangle)])
            delaunay_triangles.extend(processed_triangles)

    # deduplication (avoiding duplicate triangles)
    delaunay_triangles = list(set(delaunay_triangles))

    return delaunay_triangles

# Calculate t0
def calculate_t0(triangles, polygon_edges):
    polygon_edge_set = set(tuple(sorted(edge)) for edge in polygon_edges)

    t0 = 0

    for triangle in triangles:
        # Extract three boundary
        edges = [
            tuple(sorted((triangle.exterior.coords[0], triangle.exterior.coords[1]))),
            tuple(sorted((triangle.exterior.coords[1], triangle.exterior.coords[2]))),
            tuple(sorted((triangle.exterior.coords[2], triangle.exterior.coords[0]))),
        ]

        # Check if it is free triangle
        if all(edge not in polygon_edge_set for edge in edges):
            t0 += 1

    return t0

# draw Delaunay triangulation
def plot_delaunay(delaunay_triangles,polygon_edges):
    plt.figure(figsize=(6, 6))

    # draw boundary
    for edge in polygon_edges:
        x = [edge[0][0], edge[1][0]]
        y = [edge[0][1], edge[1][1]]
        plt.plot(x, y, 'g-', linewidth=2, label="Polygon Edge")

    # draw Delaunay triangulation
    for triangle in delaunay_triangles:
        x, y = zip(*triangle.exterior.coords)
        plt.plot(x, y, 'b-', alpha=0.7)

    plt.title("Delaunay Triangulation")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')  
    plt.show()

#main
if __name__ == "__main__":
    # vertex
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

    #draw polygon
    fig, ax = plt.subplots()
    polygon = plt.Polygon(points, closed=True, edgecolor='black', alpha=0.7)
    ax.add_patch(polygon)
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 500)
    plt.gca().set_aspect('equal', adjustable='box')  # 确保多边形比例正确
    plt.show()

    #get polygon edges
    for i in range(len(points)-1):
        polygon_edges.append([points[i],points[i+1]])
    polygon_edges.append([points[len(points)-1], points[0]])
    #print(polygon_edges)

    # check simple polygon
    if is_simple_polygon(points):
        print("Simple polygon")

        # Delaunay triangulation
        delaunay_triangles = compute_delaunay_with_edges(points,polygon_edges)

        # draw triangulation
        plot_delaunay(delaunay_triangles,polygon_edges)

        # Calculate t0
        t0_value = calculate_t0(delaunay_triangles, polygon_edges)
        print(f"t₀ : {t0_value}")

    else:
        print("Polygon is not a simple polygon!")
