import cv2
import numpy as np

def extraction(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter for noise reduction
    blur = cv2.bilateralFilter(gray, 11, 90, 90)

    # Apply adaptive thresholding
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and aspect ratio
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]
    contours = [cnt for cnt in contours if aspect_ratio_check(cnt)]

    # Initialize plate variable
    plate = None

    # Iterate through contours
    for cnt in contours:
        # Approximate polygonal curves
        epsilon = 0.05 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Check if contour has 4 edges (likely a plate)
        if len(approx) == 4:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(cnt)
            plate = image[y:y + h, x:x + w]

            # Apply perspective transformation
            plate = perspective_transform(plate, approx.reshape(-1, 2))
            break

    return plate

def aspect_ratio_check(cnt):
    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = w / float(h)
    return 2.5 < aspect_ratio < 6.5

def perspective_transform(image, pts):
    # Define destination points for perspective transformation
    width, height = 300, 100
    dst_pts = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")

    # Compute perspective transform matrix
    M = cv2.getPerspectiveTransform(pts, dst_pts)

    # Apply perspective transform
    warped = cv2.warpPerspective(image, M, (width, height))

    return warped
