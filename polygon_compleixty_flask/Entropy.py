import numpy as np
import matplotlib.pyplot as plt
import base64

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

def Entropy(vertex, file_key):
    result = {}
    points = [(v[0], v[1]) for v in vertex]
    curvatures = calculate_curvature(points)
    entropy = compute_entropy(curvatures)
    #print(f"Entropy:{entropy:.3f}")
    
    plt.figure()
    plt.hist(curvatures, bins=10, density=True, alpha=0.7)
    plt.title(f"Entropy of curvature = {entropy:.3f}")
    plt.xlabel("Curvature")
    plt.ylabel("Probability density")
    plt.tight_layout()
    #plt.show()
    save_path = "./entropy_fig/" + str(file_key)+".png" 
    plt.savefig(save_path)
    with open(save_path,'rb') as f:
        img_data = base64.b64encode(f.read()).decode('utf-8')
    img_data = "data:image/png;base64," + img_data

    result['complexity'] = str(entropy)
    result['img'] = img_data
    return result
