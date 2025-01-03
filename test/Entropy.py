import numpy as np
import matplotlib.pyplot as plt

def calculate_curvature(points):
    curvatures = []
    for i in range(1, len(points) - 1):
        p_prev, p_curr, p_next = np.array(points[i - 1]), np.array(points[i]), np.array(points[i + 1])
        v1 = p_curr - p_prev
        v2 = p_next - p_curr
        angle = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0]) #get angle
        angle = np.abs((angle + np.pi) % (2 * np.pi) - np.pi)  #[0,pi]
        curvatures.append(angle)
    return np.array(curvatures)

def compute_histogram(curvatures, bins=10):
    hist, bin_edges = np.histogram(curvatures, bins=bins, density=True)  
    return hist, bin_edges

def compute_entropy(curvatures, bins=10):
    hist, _ = np.histogram(curvatures, bins=bins, density=True)
    hist = hist[hist > 0]  # Filter out zero values ​​to avoid log(0)
    probabilities = hist / hist.sum()
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

if __name__ == "__main__":
    points = [(284.546875, 209.796875), (309.546875, 273.796875), (300.546875, 374.796875), (205.546875, 425.796875), (145.546875, 426.796875), (87.546875, 373.796875), (145.546875, 373.796875), (182.546875, 385.796875), (212.546875, 367.796875), (145.546875, 334.796875), (100.546875, 344.796875), (50.546875, 333.796875), (126.546875, 206.796875), (178.546875, 250.796875), (218.546875, 284.796875), (230.546875, 240.796875), (199.546875, 178.796875), (245.546875, 168.796875)]
    
    curvatures = calculate_curvature(points)
    entropy = compute_entropy(curvatures)

    print(f"Entropy:{entropy:.3f}")
    
    plt.hist(curvatures, bins=10, density=True, alpha=0.7)
    plt.title(f"Entropy of curvature = {entropy:.3f}")
    plt.xlabel("Curvature")
    plt.ylabel("Probability density")

    plt.tight_layout()
    plt.show()