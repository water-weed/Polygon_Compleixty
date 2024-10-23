import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def scan_convert_image(image_path, padding=16):
    """
    Convert the image to a 256x256 binary image and add padding
    """
    img = Image.open(image_path).convert('L')  
    img = np.array(img)
    
    # Resize the image to 256x256 and add padding.
    img_resized = cv2.resize(img, (256 - 2 * padding, 256 - 2 * padding), interpolation=cv2.INTER_NEAREST)
    
    # Add padding around all sides.
    img_padded = np.pad(img_resized, pad_width=padding, mode='constant', constant_values=0)
    
    # Binarization processing.
    _, binary_img = cv2.threshold(img_padded, 128, 255, cv2.THRESH_BINARY)
    
    return binary_img

def downsample_image_with_fixed_grid(binary_img, grid_size, threshold=0.1):
    """
    Downsample the binary image using a fixed-size grid (e.g., 2x2 pixels) while keeping the image size unchanged.
    :param binary_img: The input binary image.
    :param grid_size:  The fixed size of the grid (each grid is grid_size x grid_size pixels).
    :param threshold: The threshold for the proportion of white pixels within the grid.
    """
    img_h, img_w = binary_img.shape
    downsampled_img = np.zeros_like(binary_img)

    total_occupied_pixels = 0

    # Iterate through each grid.
    for i in range(0, img_h, grid_size):
        for j in range(0, img_w, grid_size):
            # Extract the pixel region of the current grid.
            grid_region = binary_img[i:i + grid_size, j:j + grid_size]

            white_pixel_ratio = np.sum(grid_region == 255) / grid_region.size

            # If the proportion of white pixels is greater than the set threshold, the shape is considered to occupy the grid.
            if white_pixel_ratio > threshold:
                downsampled_img[i:i + grid_size, j:j + grid_size] = 255
                total_occupied_pixels += np.sum(grid_region == 255)  # 计算白色像素数量

    # Calculate the total number of white pixels in the original image.
    original_occupied_pixels = np.sum(binary_img == 255)
    
    # area ratio
    if original_occupied_pixels > 0:
        area_ratio = total_occupied_pixels / original_occupied_pixels
    else:
        area_ratio = 0  

    return downsampled_img, area_ratio,total_occupied_pixels,original_occupied_pixels

def DownsampingArea(url):
    binary_img = scan_convert_image(url)

    # grid size
    grid_sizes = [2, 4, 8, 16]  

    result = {}
    final_complexity = 0
    for grid_size in grid_sizes:
        downsampled_img, area_ratio,total_occupied_pixels,original_occupied_pixels = downsample_image_with_fixed_grid(binary_img, grid_size, threshold=0.5)
        #print(f'网格大小 {grid_size}x{grid_size} 像素的区域面积比: {area_ratio}')
        print(type(total_occupied_pixels))
        result[str(grid_size)] = {'complexity': 1-area_ratio,
                                  'total_occupied_pixels':int(total_occupied_pixels), 
                                  'original_occupied_pixels': int(original_occupied_pixels),
                                  #'downsampled_img':downsampled_img
                                  }
        final_complexity = 1- area_ratio
    result['complexity'] = final_complexity
    return result
        