from skimage.morphology import medial_axis
from skimage import io
import numpy as np
from scipy.spatial import distance_matrix
import heapq
import matplotlib.pyplot as plt
from PIL import Image
import cv2
from scipy.spatial import cKDTree
from collections import defaultdict


image = Image.open('selection/file0.jpg').convert('L') #greyscale
image = np.array(image)
_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

# calculate media axis and distance transform
skeleton, distance = medial_axis(binary_image, return_distance=True)
radius_function = distance * skeleton
fig, axes = plt.subplots(1, 4, figsize=(20, 5))
axes[0].imshow(image, cmap="gray")
axes[0].set_title("Original Shape")

axes[1].imshow(skeleton, cmap="gray")
axes[1].set_title("Medial Axis (Skeleton)")

axes[2].imshow(distance, cmap="viridis")
axes[2].set_title("Distance Transform")

axes[3].imshow(radius_function, cmap="viridis")
axes[3].set_title("Radius Function (MAT)")

plt.show()

skeleton_coords = np.column_stack(np.nonzero(skeleton))
skeleton_distances = distance[skeleton]

# construct KD tree 
tree = cKDTree(skeleton_coords)

# neighborhood radius
neighbor_radius = np.sqrt(2)

# search neighborhood node
pairs = tree.query_pairs(neighbor_radius)
edges = [(i, j, np.linalg.norm(skeleton_coords[i] - skeleton_coords[j])) for i, j in pairs]

# initialize neighborhood list
adjacency_list = defaultdict(list)
for i, j, weight in edges:
    adjacency_list[i].append((j, weight))
    adjacency_list[j].append((i, weight))

# find degree 1 node
endpoints = [i for i, neighbors in adjacency_list.items() if len(neighbors) == 1]

# initialize EDF value
num_points = len(skeleton_coords)
edf_values = np.full(num_points, np.inf)
for idx in endpoints:
    edf_values[idx] = skeleton_distances[idx]

# construct priority list
priority_queue = [(edf_values[i], i) for i in endpoints]
heapq.heapify(priority_queue)

# grass fire
while priority_queue:
    current_value, current_idx = heapq.heappop(priority_queue)

    # if current value > edf valuse, means its be logged
    if current_value > edf_values[current_idx]:
        continue

    # update neighborhood node
    for neighbor_idx, weight in adjacency_list[current_idx]:
        new_value = edf_values[current_idx] + weight
        if new_value < edf_values[neighbor_idx]:
            edf_values[neighbor_idx] = new_value
            heapq.heappush(priority_queue, (new_value, neighbor_idx))

edf_image = np.zeros_like(binary_image, dtype=float)

for i, (x, y) in enumerate(skeleton_coords):
    edf_image[x, y] = edf_values[i]


import matplotlib.pyplot as plt
plt.imshow(edf_image, cmap='viridis')
plt.colorbar(label='EDF Value')
plt.show()

#complexity_entropy_distance
total_distance = np.sum(skeleton_distances)
probabilities_distance = skeleton_distances / total_distance
entropy_distance = -np.sum(probabilities_distance * np.log(probabilities_distance))
print(f"Distance_complexity:{entropy_distance}")

#complexity_entropy_EDF
total_EDF = np.sum(edf_values)
probabilities_EDF = edf_values / total_EDF
entropy_EDF = -np.sum(probabilities_EDF * np.log(probabilities_EDF))
print(f"EDF_complexity:{entropy_EDF}")