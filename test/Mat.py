import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import medial_axis
from skimage.draw import polygon
from skimage.measure import find_contours
from PIL import Image
import cv2

def compute_edf(binary_image, skeleton):
    # skeleton coords
    skeleton_coords = np.column_stack(np.where(skeleton))
    
    # bundary point
    contours = find_contours(binary_image, level=0.5)
    boundary_points = np.vstack(contours)  # 合并边界点为一个数组

    #plt.figure(figsize=(8, 8))
    #plt.imshow(binary_image, cmap="gray", origin="upper")
    #for contour in contours:
        #plt.plot(contour[:, 1], contour[:, 0], linewidth=2, color="red", label="Boundary")

    #plt.title("Binary Image with Extracted Boundary")
    #plt.legend(["Boundary"], loc="upper right")
    #plt.axis("off")
    #plt.show()
    
    #initialize
    edf_values = []
    
    for medial_point in skeleton_coords:
        # the distance between medial point to boundary curve
        distances = np.linalg.norm(boundary_points - medial_point, axis=1)
        
        # the second distance
        sorted_distances = np.sort(distances)[::-1]  
        second_largest = sorted_distances[1] if len(sorted_distances) > 1 else sorted_distances[0]
        
        # EDF
        edf_values.append(second_largest)
    
    return skeleton_coords, np.array(edf_values)

#EDF-std
def compute_edf_complexity(edf_values):
    mean_edf = np.mean(edf_values)
    std_edf = np.std(edf_values)
    max_edf = np.max(edf_values)
    hist, _ = np.histogram(edf_values, bins=20, density=True)
    p = hist / np.sum(hist)
    p = p[p > 0]  
    entropy = -np.sum(p * np.log2(p))
    
    return std_edf

def compute_wedf(skeleton_coords, distance_transform):
    wedf_values = []
    for coord in skeleton_coords:
        radius = distance_transform[coord[0], coord[1]]
        wedf_values.append(radius)
    return np.array(wedf_values)

def compute_erosion_thickness(skeleton_coords, distance_transform):
    et_values = []
    for coord in skeleton_coords:
        radius = distance_transform[coord[0], coord[1]]
        local_feature_size = radius  
        et_values.append(radius - local_feature_size)
    return np.array(et_values)

def compute_shape_tubularity(et_values, edf_values):
    return np.array([et / edf if edf != 0 else 0 for et, edf in zip(et_values, edf_values)])


#image = np.zeros((100, 100), dtype=bool)
image = Image.open('selection/file9.jpg').convert('L') #greyscale
image = np.array(image)
_, binary_img = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
#poly_row, poly_col = polygon([20, 80, 80, 50, 20], [30, 30, 70, 90, 70])
#image[poly_row, poly_col] = True

# skeleton and distance transform
skeleton, distance = medial_axis(binary_img, return_distance=True)

# radius function
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

#EDF
skeleton_coords, edf_values = compute_edf(binary_img,skeleton)
edf_complexity = compute_edf_complexity(edf_values)
print(edf_complexity)

wedf_values = compute_wedf(skeleton_coords, distance)
et_values = compute_erosion_thickness(skeleton_coords, distance)
st_values = compute_shape_tubularity(et_values, edf_values)


plt.figure(figsize=(8, 8))
plt.imshow(binary_img, cmap="gray")
plt.scatter(skeleton_coords[:, 1], skeleton_coords[:, 0], c=edf_values, cmap="viridis", s=10)
#plt.colorbar(label="Shape Tubularity (ST)")
#plt.title("Skeleton with Shape Tubularity")
plt.show()

