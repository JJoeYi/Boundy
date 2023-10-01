import cv2
import numpy as np

# Global variable to store polygon points
points = []

# Initialize variables
image_path = './goat-easy.jpg'  # Replace with your image path
radius = 10  # Click radius for point removal

# Flag to indicate right-click is held down
right_click_held = False

# Function to update the displayed image


def update_display(image_copy):
    # Draw the polygon
    if len(points) >= 2:
        cv2.polylines(image_copy, [np.array(points)],
                      isClosed=True, color=(0, 255, 0), thickness=2)

    cv2.imshow("Edit Polygon", image_copy)

# Function to handle mouse events


def mouse_callback(event, x, y, flags, param):
    global points, right_click_held

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

    elif event == cv2.EVENT_RBUTTONDOWN:
        right_click_held = True

    elif event == cv2.EVENT_MOUSEMOVE and right_click_held:
        # While holding down right-click, continuously remove points within a certain radius
        points = [p for p in points if np.linalg.norm(
            np.array(p) - np.array((x, y))) > radius]

    elif event == cv2.EVENT_RBUTTONUP:
        right_click_held = False

    update_display(np.copy(image))


# Load the image
image = cv2.imread(image_path)
cv2.namedWindow("Edit Polygon")
cv2.setMouseCallback("Edit Polygon", mouse_callback)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, threshold1=30, threshold2=100)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(
    edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize the polygon with an empty list
approx = []

# Iterate through the detected contours and approximate with polygons
for contour in contours:
    epsilon = 0.03 * cv2.arcLength(contour, True)
    temp_approx = cv2.approxPolyDP(contour, epsilon, True)

    # Extend the 'approx' list with the points from the current approximation
    for coord in temp_approx:
        approx.append(coord[0])

# Update the global 'points' variable with the polygon coordinates
points = approx

# Find the convex hull of the points
convex_hull = cv2.convexHull(np.array(points), clockwise=True)

# Convert the convex hull points to a list of coordinates
convex_hull_points = [tuple(coord[0]) for coord in convex_hull]

# Update the 'points' variable with the sorted convex hull points
points = convex_hull_points

# Initialize the display with the original image
update_display(np.copy(image))

while True:
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):  # Press 'q' to quit
        break

cv2.destroyAllWindows()
