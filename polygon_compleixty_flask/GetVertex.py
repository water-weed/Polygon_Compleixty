import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def GetVertex(url):
# Step 1: read image
    img = Image.open(url).convert('L')  # The 'L' mode refers to a grayscale image
    img = np.array(img)  
    
    _, img_thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)

    # To remove small noise and jagged edges from an image
    kernel = np.ones((3, 3), np.uint8)
    img_morph = cv2.morphologyEx(img_thresh, cv2.MORPH_OPEN, kernel)

    # detect edge
    edges = cv2.Canny(img_morph, 50, 150)

    # detect boundary
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # polygon approximation
    epsilon = 0.001 * cv2.arcLength(contours[0], True)
    approx = cv2.approxPolyDP(contours[0], epsilon, True)

    polygon_vertices = approx[:, 0, :]
    # print(polygon_vertices)

    return polygon_vertices