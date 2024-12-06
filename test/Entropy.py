import numpy as np
import matplotlib.pyplot as plt

def calculate_curvature(points):
    curvatures = []
    for i in range(1, len(points) - 1):
        p_prev, p_curr, p_next = np.array(points[i - 1]), np.array(points[i]), np.array(points[i + 1])
        v1 = p_curr - p_prev
        v2 = p_next - p_curr
        angle = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
        angle = np.abs((angle + np.pi) % (2 * np.pi) - np.pi)  # 转为 [0, π]
        curvatures.append(angle)
    return np.array(curvatures)

def compute_histogram(curvatures, bins=10):
    hist, bin_edges = np.histogram(curvatures, bins=bins, density=True)  # 归一化分布
    return hist, bin_edges

def compute_entropy(curvatures, bins=10):
    hist, _ = np.histogram(curvatures, bins=bins, density=True)
    hist = hist[hist > 0]  # 过滤掉零值，避免 log(0)
    probabilities = hist / hist.sum()
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

if __name__ == "__main__":
    # 点集
    points = [(272.4166564941406, 193.13540649414062), (301.4166564941406, 289.1354064941406), 
              (295.4166564941406, 357.1354064941406), (344.4166564941406, 385.1354064941406), 
              (388.4166564941406, 378.1354064941406), (385.4166564941406, 271.1354064941406), 
              (432.4166564941406, 310.1354064941406), (439.4166564941406, 329.1354064941406), 
              (422.4166564941406, 383.1354064941406), (419.4166564941406, 409.1354064941406), 
              (408.4166564941406, 446.1354064941406), (318.4166564941406, 479.1354064941406), 
              (138.41665649414062, 306.1354064941406), (232.41665649414062, 255.13540649414062)]
    
    curvatures = calculate_curvature(points)
    entropy = compute_entropy(curvatures)

    print(f"曲线复杂度（熵）：{entropy:.3f}")
    
    plt.hist(curvatures, bins=10, density=True, alpha=0.7)
    plt.title(f"曲率分布\n熵 = {entropy:.3f}")
    plt.xlabel("曲率")
    plt.ylabel("概率密度")

    plt.tight_layout()
    plt.show()