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
import base64

def Edf(url, file_key):
    image = Image.open(url).convert('L') #greyscale
    image = np.array(image)
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

    # calculate media axis and distance transform
    skeleton, distance = medial_axis(binary_image, return_distance=True)
    radius_function = distance * skeleton

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

    plt.figure()
    plt.imshow(edf_image, cmap='viridis')
    plt.colorbar(label='EDF Value')
    #plt.show()
    save_path = "./edf_fig/" + str(file_key)+".png" 
    plt.savefig(save_path)
    with open(save_path,'rb') as f:
        img_data = base64.b64encode(f.read()).decode('utf-8')
    img_data = "data:image/png;base64," + img_data

    #complexity_entropy_EDF
    total_EDF = np.sum(edf_values)
    probabilities_EDF = edf_values / total_EDF
    entropy_EDF = -np.sum(probabilities_EDF * np.log(probabilities_EDF))
    result={}
    result['complexity'] = entropy_EDF
    result['img'] = img_data
    return result



    