import numpy as np
import matplotlib.pyplot as plt
from GetVertex import GetVertex

# Example boundary (a circle for simplicity)
"""t = np.linspace(0, 2*np.pi, 500)
x = np.cos(t)
y = np.sin(t)
boundary = np.vstack((x, y)).T
"""
boundary = GetVertex("./selection/apple-2.gif")
#print(boundary)
print(len(boundary))
original_distances = np.linalg.norm(boundary[1:] - boundary[:-1], axis=1)
original_length = np.sum(original_distances)

# Downsample by direct extraction
def downsample_direct(boundary, num_points):
    # Choose points with equal spacing
    indices = np.linspace(0, len(boundary) - 1, num_points, dtype=int)
    downsampled_boundary = boundary[indices]
    return downsampled_boundary

downsample_points = [100, 50, 25, 8]

fig, axes = plt.subplots(1, len(downsample_points), figsize=(15, 5), sharex=True, sharey=True)

# Plotting the original boundary and the downsampled results
for i, num_points in enumerate(downsample_points):
    downsampled_boundary = downsample_direct(boundary, num_points)
    downsampled_distances = np.linalg.norm(downsampled_boundary[1:] - downsampled_boundary[:-1], axis=1)
    downsampled_length = np.sum(downsampled_distances)
    complexity = 1- (downsampled_length/original_length)
    print(f"{num_points}:complexity:{complexity},original_length:{original_length},downsampled_length:{downsampled_length}")
    axes[i].plot(boundary[:, 0], boundary[:, 1], 'k--', label='Original Boundary (500 points)')
    axes[i].plot(downsampled_boundary[:, 0], downsampled_boundary[:, 1], 'b-', label=f'{num_points} Points')
    axes[i].scatter(downsampled_boundary[:, 0], downsampled_boundary[:, 1], label=f'{num_points} Points')
    axes[i].set_title(f'{num_points} Points')
    axes[i].set_aspect('equal', adjustable='box')
    axes[i].legend()

# Add a global title
plt.suptitle('Direct Extraction Downsampling with Different Numbers of Points', fontsize=16)
plt.tight_layout()
plt.show()

