def average_color (x, y, image, smoothing_range):
    """
    Purpose: find the average color of a region of pixels in the image. This is used to "smooth" the detected edges,
             by avoiding outlier pixels that would be marked as an edge otherwise.
    Inputs: x: x location of center pixel
            y: y location of center pixel
            image: PIL Image to run on
            smoothing_range: how many pixels to each side (left right up down) of the center pixel to evaluate
            its color value to include in the average of that region of the image
    Output: average color (grayscale, 0-255) of the block of pixels with side length 2 * smoothing_range + 1, centered
            on the given pixel.
    """

    colorSum = 0
    for i in range(-1 * smoothing_range, smoothing_range + 1):
        for j in range(-1 * smoothing_range, smoothing_range + 1):
            colorSum += image.getpixel((x+i,y+j)) # adds each pixel's gray scale value to sum

    return colorSum / ((2 * smoothing_range + 1) ** 2) # divides sum by number of pixels to get average


def forehead_point (edge_matrix):
    """
    Purpose: find the point of the forehead that is centered and just below the hairline
    Inputs: edge_matrix, a zero array mirroring the original image with all edge pixels changed to 1
    Output: [x location of the point, y location of the point]
    """

    startingPoint = int(edge_matrix.shape[1] / 3)

    while edge_matrix[int(edge_matrix.shape[0] / 2), startingPoint] != 1:
        edge_matrix[int(edge_matrix.shape[0] / 2), startingPoint] = 2
        startingPoint -= 1

    return [int(edge_matrix.shape[0] / 2), startingPoint]

def chin_point (edge_matrix):
    """
    Purpose: find the bottom point of the chin
    Inputs: edge_matrix, a zero array mirroring the original image with all edge pixels changed to 1
    Output: [x location of the point, y location of the point]
    """

    startingPoint = int(edge_matrix.shape[1] - 1)

    while edge_matrix[int(edge_matrix.shape[0] / 2), startingPoint] != 1:
        edge_matrix[int(edge_matrix.shape[0] / 2), startingPoint] = 2
        startingPoint -= 1

    return [int(edge_matrix.shape[0] / 2), startingPoint]


def forehead_width (edge_matrix):
    """
    Purpose: find the width of the forehead
    Inputs: edge_matrix, a zero array mirroring the original image with all edge pixels changed to 1
    Output: width of the forehead
    """

    #step 1: find middle forehead
    faceLength = chin_point(edge_matrix)[1] - forehead_point(edge_matrix)[1]
    midForehead = [forehead_point(edge_matrix)[0], forehead_point(edge_matrix)[1] + int(faceLength / 6)]

    #step 2: find forehead width
    rightSideForehead = midForehead[0]
    leftSideForehead = midForehead[0]
    while edge_matrix[rightSideForehead, midForehead[1]] != 1 and edge_matrix[rightSideForehead, midForehead[1] + int(faceLength / 30)] != 1 and edge_matrix[rightSideForehead, midForehead[1] - int(faceLength / 22)] != 1:
        edge_matrix[rightSideForehead, midForehead[1]] = 2
        rightSideForehead += 1
    while edge_matrix[leftSideForehead, midForehead[1]] != 1 and edge_matrix[leftSideForehead, midForehead[1] + int(faceLength / 30)] != 1 and edge_matrix[leftSideForehead, midForehead[1] - int(faceLength / 22)] != 1:
        edge_matrix[leftSideForehead, midForehead[1]] = 2
        leftSideForehead -= 1

    return rightSideForehead - leftSideForehead


def forehead_height (edge_matrix):
    """
    Purpose: find the height of the forehead
    Inputs: edge_matrix, a zero array mirroring the original image with all edge pixels changed to 1
    Output: height of the forehead
    """

    #step 1: find middle forehead
    faceLength = chin_point(edge_matrix)[1] - forehead_point(edge_matrix)[1]
    midForehead = [forehead_point(edge_matrix)[0], forehead_point(edge_matrix)[1] + int(faceLength / 6)]

    #step 2: find right eyebrow and distance from hairline
    aboveRightEyebrow = [midForehead[0] + int(forehead_width(edge_matrix) / 4), midForehead[1]]
    hairline = aboveRightEyebrow[1]
    eyebrow = aboveRightEyebrow[1]

    while edge_matrix[midForehead[0] + int(forehead_width(edge_matrix) / 4), hairline] != 1 and edge_matrix[midForehead[0] + int(forehead_width(edge_matrix) / 10) + int(forehead_width(edge_matrix) / 4), hairline] != 1 and edge_matrix[midForehead[0] - int(forehead_width(edge_matrix) / 10)+ int(forehead_width(edge_matrix) / 4), hairline] != 1:
        edge_matrix[midForehead[0] + int(forehead_width(edge_matrix) / 4), hairline] = 2
        hairline -= 1
    while edge_matrix[midForehead[0] + int(forehead_width(edge_matrix) / 4), eyebrow] != 1:
        edge_matrix[midForehead[0] + int(forehead_width(edge_matrix) / 4), eyebrow] = 2
        eyebrow += 1

    return eyebrow - hairline

def lip_height (edge_matrix):
    """
    Purpose: find the height of the lips from the chin
    Inputs: edge_matrix, a zero array mirroring the original image with all edge pixels changed to 1
    Output: height of the lips from the chin
    """

    faceLength = chin_point(edge_matrix)[1] - forehead_point(edge_matrix)[1]
    lips = chin_point(edge_matrix)[1] - int(faceLength / 10)

    while edge_matrix[chin_point(edge_matrix)[0], lips] == 1:
        edge_matrix[chin_point(edge_matrix)[0], lips] = 2
        lips -= 1

    while edge_matrix[chin_point(edge_matrix)[0], lips] != 1 or edge_matrix[chin_point(edge_matrix)[0] + int(forehead_width(edge_matrix) / 6), lips] != 1 or edge_matrix[chin_point(edge_matrix)[0] - int(forehead_width(edge_matrix) / 6), lips] != 1:
        edge_matrix[chin_point(edge_matrix)[0], lips] = 2
        lips -= 1

    return chin_point(edge_matrix)[1] - lips

def get_proportions (edge_matrix):
    """
    Purpose: normalize all the face measurements to the longest measurement
    Inputs: edge_matrix, a zero array mirroring the original image with all edge pixels changed to 1
    Output: a list of each face measurement normalized to the longest measurement
    """

    faceLength = chin_point(edge_matrix)[1] - forehead_point(edge_matrix)[1]
    max_val = max(faceLength, forehead_width(edge_matrix), forehead_height(edge_matrix), lip_height(edge_matrix))
    return [faceLength/max_val, forehead_width(edge_matrix)/max_val, forehead_height(edge_matrix)/max_val, lip_height(edge_matrix)/max_val]


def closest_match (measurements):
    """
    Purpose: find the best match to the target face measurements
    Inputs: measurements, a list of lists with each containing the measurements of one face. The last list is the
            target measurements.
    Output: the index of the list with the best match to the target list
    """

    # Uses basic distance formula to calculate closest match. Ideally, I'd like to use linear
    # or logistic regression but since this project tries to minimise libraries, this will do.

    distance = [0] * (len(measurements) - 1)
    for i in range(len(measurements) - 1):
        for j in range(len(measurements[0])):
            distance[i] += (measurements[-1][j] - measurements[i][j]) ** 2
        distance[i] = distance[i] ** (1/2)

    print("How close each face is to being completely identical: " + str(distance))
    return distance.index(min(distance))
