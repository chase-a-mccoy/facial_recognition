from PIL import Image
import numpy as np
from functions import *
import matplotlib.pyplot as plt

image_list = [x.strip().replace("\"", "") for x in open("image_sources.txt", "r").readlines() if x[0] == "\""] # reads in image strings into an array
face_measurements = [] # list to hold a list of each face's measurements, the last one will be the target face

for image_string in image_list:
    face_to_run_edge_detection = Image.open(image_string).convert("L") # image to run algorithm on, in grayscale
    face_to_display_detected_edges = Image.open(image_string) # image just to display edges with blue pixels on each edge point

    edge_matrix = np.zeros((face_to_run_edge_detection.size[0], face_to_run_edge_detection.size[1])) # an array of zeros the size of the image

    smoothing_range = 3 # how many pixels next to each pixel we look at to "smooth" the edge detection and avoid outliers
    for i in range(smoothing_range, face_to_run_edge_detection.size[0] - 2 * smoothing_range): # loops through each pixel
        for j in range(smoothing_range, face_to_run_edge_detection.size[1] - 2 * smoothing_range):

            pixBlock = average_color(i, j, face_to_run_edge_detection, smoothing_range) # average color of nearby pixels
            pixBlockSide = average_color(i + smoothing_range, j, face_to_run_edge_detection, smoothing_range) # average color of pixel block to the right
            pixBlockDown = average_color(i, j + smoothing_range, face_to_run_edge_detection, smoothing_range) # average color of pixel block below

            if abs(pixBlock - pixBlockSide) > 15: # difference in grayscale color value of 15
                face_to_display_detected_edges.putpixel((i + int(smoothing_range / 2),j), (0,0,255)) # puts a blue pixel on the edge
                edge_matrix[i + int(smoothing_range / 2),j] = 1 # changes the relevant 0 in edge_matrix to a 1
            if abs(pixBlock - pixBlockDown) > 10: # same as above, slightly more sensitive because chins can be tricky to detect
                face_to_display_detected_edges.putpixel((i,j + int(smoothing_range / 2)), (0,0,255))
                edge_matrix[i,j + int(smoothing_range / 2)] = 1

    [fLength, fhWidth, fhHeight, lHeight] = get_proportions(edge_matrix) # get face measurements

    # mainly used for bug testing, displays the marked edges and each face measurement
    '''
    if image_string == "testimage1.jpg":
        plt.imshow(edge_matrix)
        plt.show()
        face_to_display_detected_edges.show()
    '''

    face_measurements.append([fLength, fhWidth, fhHeight, lHeight]) # add this face's measurements to the list of measurements

print(face_measurements)
index_best_match = closest_match(face_measurements)
print("The number of the image with the best match (starting at 1): " + str(index_best_match + 1))