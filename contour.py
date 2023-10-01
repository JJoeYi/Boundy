import cv2
import numpy as np

# Function to perform edge detection and polygon approximation


def process_image(image_path):
    # Load the input image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection
    edges = cv2.Canny(gray, threshold1=30, threshold2=100)

    # Find contours
    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a copy of the original image to draw on
    result_image = np.copy(image)

    # Iterate through detected contours and approximate with polygons
    for contour in contours:
        epsilon = 0.03 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        print(approx)
        cv2.drawContours(result_image, [approx], -1, (0, 255, 0), 2)

    # Display the original image and the result
    cv2.imshow('Original Image', image)
    cv2.imshow('Result with Polygons', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Main function
if __name__ == "__main__":
    image_path = './goat-easy.jpg'  # Replace with your image path
    process_image(image_path)
