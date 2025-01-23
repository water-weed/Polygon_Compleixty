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

def Mat(url, file_key):
    image = Image.open(url).convert('L') #greyscale
    image = np.array(image)
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

    # calculate media axis and distance transform
    skeleton, distance = medial_axis(binary_image, return_distance=True)
    radius_function = distance * skeleton
    plt.figure()
    plt.imshow(radius_function, cmap="viridis")
    plt.colorbar(label='radius function(MAT)')
    #plt.show()
    save_path = "./mat_fig/" + str(file_key)+".png" 
    plt.savefig(save_path)
    with open(save_path,'rb') as f:
        img_data = base64.b64encode(f.read()).decode('utf-8')
    img_data = "data:image/png;base64," + img_data

    skeleton_distances = distance[skeleton]

    #complexity_entropy_distance
    total_distance = np.sum(skeleton_distances)
    probabilities_distance = skeleton_distances / total_distance
    entropy_distance = -np.sum(probabilities_distance * np.log(probabilities_distance))
    result={}
    result['complexity'] = entropy_distance
    result['img'] = img_data
    return result
