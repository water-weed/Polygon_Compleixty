import numpy as np
import matplotlib.pyplot as plt
import base64

def DownsamplingBoudary(boundary,file_key):
    result = {}
    final_complexity =0
    # original polygon boundary length
    original_distances = np.linalg.norm(boundary[1:] - boundary[:-1], axis=1)
    original_length = np.sum(original_distances)

    #downsample points
    downsample_points = [100, 50, 25, 8]

    # create a sub-image window, each number of sampling points corrsponds to a sub-image
    fig, axes = plt.subplots(1, len(downsample_points), figsize=(15, 5), sharex=True, sharey=True)

    for i, num_points in enumerate(downsample_points):
       #downsample boundary
       downsampled_boundary = downsample_direct(boundary, num_points)

       #downsample boundary length
       downsampled_distances = np.linalg.norm(downsampled_boundary[1:] - downsampled_boundary[:-1], axis=1)
       downsampled_length = np.sum(downsampled_distances)

       complexity = 1- (downsampled_length/original_length)
       result[str(num_points)] = {'complexity':complexity, 'original_length':original_length, 'downsampled_length':downsampled_length}
       #print(f"{num_points}:complexity:{complexity},original_length:{original_length},downsampled_length:{downsampled_length}")
       axes[i].plot(boundary[:, 0], boundary[:, 1], 'k--', label='Original Boundary')
       axes[i].plot(downsampled_boundary[:, 0], downsampled_boundary[:, 1], 'b-', label=f'{num_points} Points')
       axes[i].scatter(downsampled_boundary[:, 0], downsampled_boundary[:, 1], label=f'{num_points} Points')
       axes[i].set_title(f'{num_points} Points')
       axes[i].set_aspect('equal', adjustable='box')
       axes[i].legend()
       final_complexity = complexity
    
    result['complexity'] = final_complexity

    save_path = "./downsampling_boundary_fig/" + str(file_key)+".png"
    plt.tight_layout()
    plt.savefig(save_path)

    #convert image to Base64
    with open(save_path,'rb') as f:
        img_data = base64.b64encode(f.read()).decode('utf-8')
    img_data = "data:image/png;base64," + img_data
    #print(img_data)
    result['img'] = img_data
    return result
       
# Downsample by direct extraction
def downsample_direct(boundary, num_points):
    # Choose points with equal spacing
    indices = np.linspace(0, len(boundary) - 1, num_points, dtype=int)
    downsampled_boundary = boundary[indices]
    return downsampled_boundary



