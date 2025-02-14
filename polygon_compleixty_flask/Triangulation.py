from shapely.geometry import Polygon, LineString
from shapely.ops import triangulate
from foronoi import Voronoi,Visualizer
import matplotlib.pyplot as plt
import foronoi
import triangle
import base64

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
    bounding_poly = foronoi.Polygon([[0, 0],[700, 0],[700, 700],[0, 700]])
    voronoi = Voronoi(bounding_poly)
    voronoi.create_diagram(points)
    #Visualizer(voronoi) \
    #    .plot_sites(show_labels=False) \
    #    .plot_edges(show_labels=False) \
    #    .plot_vertices() \
    #    .show()

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
def plot_delaunay(delaunay_triangles,polygon_edges,file_key):
    plt.figure(figsize=(6,6))

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
    plt.axis('equal')
    #plt.gca().set_aspect('equal', adjustable='box') 

    save_path = "./triangulation_fig/" + str(file_key)+".png" 
    plt.savefig(save_path)
    return save_path
    #plt.show()

#Triangulation measure
def Triangulation(vertex, file_key):
    points = [(v[0], v[1]) for v in vertex]
    #print(points)
    polygon_edges = []
    result = {}

    #get polygon edges
    for i in range(len(points)-1):
        polygon_edges.append([points[i],points[i+1]])
    polygon_edges.append([points[len(points)-1], points[0]])
    #print(polygon_edges)

    # check simple polygon
    if is_simple_polygon(points):
        #print("Simple polygon")

        # Delaunay triangulation
        delaunay_triangles = compute_delaunay_with_edges(points,polygon_edges)

        # draw triangulation
        url = plot_delaunay(delaunay_triangles,polygon_edges,file_key)
        with open(url,'rb') as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')
        img_data = "data:image/png;base64," + img_data
        #print(img_data)
        result['img'] = img_data

        # Calculate t0
        t0_value = calculate_t0(delaunay_triangles, polygon_edges)
        result['complexity'] = str(t0_value)
        return result
        #print(f"t₀ : {t0_value}")

    else:
        print("Polygon is not a simple polygon!")
        return result

