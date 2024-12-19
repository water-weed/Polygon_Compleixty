import numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


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
        "compl": compl,
        "polygon_perimeter": polygon_perimeter,
        "polygon_area": polygon_area,
        "hull_perimeter": hull_perimeter,
        "hull_area": hull_area,
    }


def visualize_polygon(points):
    hull = ConvexHull(points)
    
    # Plot original polygon
    plt.plot(*zip(*(list(points) + [points[0]])), label="Polygon")
    
    # Plot convex hull
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'r--', label="Convex Hull")
    
    plt.legend()
    plt.show()


# Example usage:
points = np.array([(289.4166564941406, 199.13540649414062), (300.4166564941406, 248.13540649414062), (300.4166564941406, 248.13540649414062), 
                   (327.4166564941406, 205.13540649414062), (329.4166564941406, 147.13540649414062), (372.4166564941406, 177.13540649414062), 
                   (384.4166564941406, 217.13540649414062), (410.4166564941406, 237.13540649414062), (398.4166564941406, 296.1354064941406), 
                   (439.4166564941406, 300.1354064941406), (447.4166564941406, 302.1354064941406), (473.4166564941406, 288.1354064941406), 
                   (462.4166564941406, 375.1354064941406), (457.4166564941406, 412.1354064941406), (393.4166564941406, 429.1354064941406), 
                   (386.4166564941406, 419.1354064941406), (365.4166564941406, 393.1354064941406), (327.4166564941406, 403.1354064941406), 
                   (263.4166564941406, 459.1354064941406), (251.41665649414062, 467.1354064941406), (139.41665649414062, 465.1354064941406), 
                   (164.41665649414062, 439.1354064941406), (187.41665649414062, 429.1354064941406), (133.41665649414062, 435.1354064941406), 
                   (63.416656494140625, 423.1354064941406), (43.416656494140625, 409.1354064941406), (65.41665649414062, 350.1354064941406), 
                   (108.41665649414062, 362.1354064941406), (124.41665649414062, 304.1354064941406), (73.41665649414062, 305.1354064941406), 
                   (24.416656494140625, 296.1354064941406), (43.416656494140625, 245.13540649414062), (77.41665649414062, 230.13540649414062),
                   (115.41665649414062, 245.13540649414062), (158.41665649414062, 237.13540649414062), (146.41665649414062, 170.13540649414062), 
                   (215.41665649414062, 139.13540649414062), (229.41665649414062, 193.13540649414062), (239.41665649414062, 223.13540649414062)])
results = calculate_complexity(points)

print("Complexity Results:", results)
visualize_polygon(points)
