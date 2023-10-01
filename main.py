import cv2
import numpy as np

image_path = './goat.jpg'
points_remaining = 120
bounding_points = []
b_amt = 255
g_amt = 255
radius = 20


def update_display():
    image_copy = np.copy(image)

    if len(bounding_points) >= 2:
        cv2.polylines(image_copy, [np.array(bounding_points)],
                      isClosed=True, color=(b_amt, g_amt, 255), thickness=2)

        cv2.putText(image_copy, f'Points Remaining: {points_remaining}', (
            10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Boundy", image_copy)


def draw_polygon(event, x, y, flags, param):
    global points_remaining, b_amt, g_amt

    if event == cv2.EVENT_LBUTTONDOWN and points_remaining >= 10:
        bounding_points.append((x,  y))
        print(bounding_points)
        points_remaining -= 10
        b_amt -= 255 / 12
        g_amt -= 255 / 12

    elif event == cv2.EVENT_RBUTTONDOWN:
        prior_len = len(bounding_points)
        # Right-click to remove points within a certain radius
        bounding_points[:] = [p for p in bounding_points if np.linalg.norm(
            np.array(p) - np.array((x, y))) > radius]

        post_len = len(bounding_points)

        if post_len < prior_len:
            points_remaining += 10
            b_amt += 255 / 12
            g_amt += 255 / 12

    update_display()


def undo_last_point():
    global points_remaining, b_amt, g_amt, bounding_points
    if len(bounding_points) >= 0:
        bounding_points.pop()
        points_remaining += 10
        b_amt += 255 / 12
        g_amt += 255 / 12


# Load the image
image = cv2.imread(image_path)
cv2.namedWindow('Boundy')
cv2.setMouseCallback('Boundy', draw_polygon)


# Main loop
while True:
    # Display the image
    cv2.imshow('Boundy', image)
    update_display()

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Press 'q' to quit
        break
    elif key == ord('u'):
        undo_last_point()
        update_display()

# Release resources and close the window
cv2.destroyAllWindows()
