import numpy as np

def DownsamplingBoudary(boundary):
    result = {}
    final_complexity =0
    original_distances = np.linalg.norm(boundary[1:] - boundary[:-1], axis=1)
    original_length = np.sum(original_distances)

    downsample_points = [100, 50, 25, 8]
    for i, num_points in enumerate(downsample_points):
       downsampled_boundary = downsample_direct(boundary, num_points)
       downsampled_distances = np.linalg.norm(downsampled_boundary[1:] - downsampled_boundary[:-1], axis=1)
       downsampled_length = np.sum(downsampled_distances)
       complexity = 1- (downsampled_length/original_length)
       result[str(num_points)] = {'complexity':complexity, 'original_length':original_length, 'downsampled_length':downsampled_length}
       print(f"{num_points}:complexity:{complexity},original_length:{original_length},downsampled_length:{downsampled_length}")
       final_complexity = complexity
    
    result['complexity'] = final_complexity
    return result
       
# Downsample by direct extraction
def downsample_direct(boundary, num_points):
    # Choose points with equal spacing
    indices = np.linspace(0, len(boundary) - 1, num_points, dtype=int)
    downsampled_boundary = boundary[indices]
    return downsampled_boundary



