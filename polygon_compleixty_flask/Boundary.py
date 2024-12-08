import numpy as np
import cv2
from PIL import Image

def Boundary(url):
    img = Image.open(url).convert('L')  
    img = np.array(img)

    _, binary_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # row change (up and down)
    row_changes = np.sum(binary_img[:-1, :] != binary_img[1:, :])

    # column change（left and right）
    col_changes = np.sum(binary_img[:, :-1] != binary_img[:, 1:])

    total_changes = 2*(row_changes + col_changes)  # total changes

    # width and length
    rows, cols = binary_img.shape

    # max changes
    max_changes = 2 * (rows * (cols - 1) + cols * (rows - 1))

    complexity = total_changes / max_changes

    result = {}
    result['complexity'] = str(complexity)
    result['total_changes'] = str(total_changes)
    result['max_changes'] = str(max_changes)
    result['size_width'] = str(rows)
    result['size_length'] = str(cols)
    #print(result)
    return result
