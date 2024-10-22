import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from GetVertex import GetVertex

# Function to calculate equal distance sampling along boundary
def downsample_boundary(boundary, num_points):
    # Compute the cumulative distances between consecutive points
    distances = np.cumsum([0] + [np.linalg.norm(boundary[i] - boundary[i-1]) for i in range(1, len(boundary))])
    total_length = distances[-1]
    
    # Generate equally spaced sample points along the total length
    sample_distances = np.linspace(0, total_length, num_points)
    
    # Interpolate to find the new sample points
    downsampled_boundary = []
    for d in sample_distances:
        # Find where the distance d fits in the cumulative distance array
        idx = np.searchsorted(distances, d)
        
        # Linear interpolation between two points on the boundary
        t = (d - distances[idx-1]) / (distances[idx] - distances[idx-1])
        new_point = (1 - t) * boundary[idx-1] + t * boundary[idx]
        downsampled_boundary.append(new_point)
    
    return np.array(downsampled_boundary)


"""t = np.linspace(0, 2*np.pi, 500)
x = np.cos(t)
y = np.sin(t)
boundary = np.vstack((x, y)).T"""
boundary = GetVertex("selection/device2-2.gif")
#print(boundary)
print(len(boundary))
original_distances = np.linalg.norm(boundary[1:] - boundary[:-1], axis=1)
original_length = np.sum(original_distances)

downsample_points = [100, 50, 25, 8]

fig, axes = plt.subplots(1, len(downsample_points), figsize=(15, 5), sharex=True, sharey=True)

# Plotting the original boundary and the downsampled results
for i, num_points in enumerate(downsample_points):
    downsampled_boundary = downsample_boundary(boundary, num_points)
    downsampled_distances = np.linalg.norm(downsampled_boundary[1:] - downsampled_boundary[:-1], axis=1)
    downsampled_length = np.sum(downsampled_distances)
    complexity = 1- (downsampled_length/original_length)
    print(f"{num_points}:complexity:{complexity},original_length:{original_length},downsampled_length:{downsampled_length}")
    axes[i].plot(boundary[:, 0], boundary[:, 1], 'k--', label='Original Boundary (500 points)')
    axes[i].scatter(downsampled_boundary[:, 0], downsampled_boundary[:, 1], label=f'{num_points} Points')
    axes[i].set_title(f'{num_points} Points')
    axes[i].set_aspect('equal', adjustable='box')
    axes[i].legend()

# Add a global title
plt.suptitle('Direct Extraction Downsampling with Different Numbers of Points', fontsize=16)
plt.tight_layout()
plt.show()


