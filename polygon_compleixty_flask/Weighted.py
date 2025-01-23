import numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon



def is_convex_vertex(p1, p2, p3):
    """Check if the vertex formed by p1, p2, and p3 is convex."""
    # Compute the cross product of vectors (p2-p1) and (p3-p2)
    v1 = np.array(p2) - np.array(p1)
    v2 = np.array(p3) - np.array(p2)
    cross_product = np.cross(v1, v2)
    return cross_product >= 0  # Convex if cross product is non-negative


def calculate_complexity(points):
    # Create the polygon and its convex hull
    polygon = Polygon(points)
    hull = ConvexHull(points)
    hull_polygon = Polygon(points[hull.vertices])
    
    # Calculate amplitude (ampl)
    polygon_perimeter = polygon.length
    hull_perimeter = hull_polygon.length
    ampl = (polygon_perimeter - hull_perimeter) / polygon_perimeter
    
    # Calculate convexity (conv)
    polygon_area = polygon.area
    hull_area = hull_polygon.area
    conv = (hull_area - polygon_area) / hull_area
    
    # Calculate frequency (freq) based on notches
    num_vertices = len(points)
    num_notches = sum(
        not is_convex_vertex(points[i - 1], points[i], points[(i + 1) % num_vertices])
        for i in range(num_vertices)
    )
    notches_norm = num_notches / (num_vertices - 3) 
    freq = 16 * (notches_norm - 0.5) ** 4 - 8 * (notches_norm - 0.5) ** 2 + 1
    
    # Compute overall complexity (compl)
    compl = 0.8 * ampl * freq + 0.2 * conv
    
    return {
        "ampl": ampl,
        "conv": conv,
        "freq": freq,
        "complexity": compl,
        "polygon_perimeter": polygon_perimeter,
        "polygon_area": polygon_area,
        "hull_perimeter": hull_perimeter,
        "hull_area": hull_area,
    }

def Weighted(vertex):
    results = {}
    point = [(v[0], v[1]) for v in vertex]
    points = np.array(point)
    #print(points)
    results = calculate_complexity(points)
    #print(results)
    return results

