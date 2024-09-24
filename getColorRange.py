import cv2
import numpy as np

# Load the image
image = cv2.imread("your image path")

height, width, channels = image.shape
# Define the maximum width and height for the window
max_width = 800  # Adjust this value as needed
max_height = 600  # Adjust this value as needed

# Calculate the aspect ratio
aspect_ratio = width / height

# Resize the image to fit within the screen dimensions
if width > max_width or height > max_height:
    if width / max_width > height / max_height:
        new_width = max_width
        new_height = int(max_width / aspect_ratio)
    else:
        new_height = max_height
        new_width = int(max_height * aspect_ratio)
    resized_image = cv2.resize(image, (new_width, new_height))
else:
    resized_image = image

hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

# Callback function for trackbars
def nothing(x):
    pass

# Create a window
cv2.namedWindow('Trackbars')

# Create trackbars for adjusting the HSV range
cv2.createTrackbar('Lower H', 'Trackbars', 0, 179, nothing)
cv2.createTrackbar('Lower S', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('Lower V', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('Upper H', 'Trackbars', 179, 179, nothing)
cv2.createTrackbar('Upper S', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('Upper V', 'Trackbars', 255, 255, nothing)

while True:
    # Get current positions of the trackbars
    lower_h = cv2.getTrackbarPos('Lower H', 'Trackbars')
    lower_s = cv2.getTrackbarPos('Lower S', 'Trackbars')
    lower_v = cv2.getTrackbarPos('Lower V', 'Trackbars')
    upper_h = cv2.getTrackbarPos('Upper H', 'Trackbars')
    upper_s = cv2.getTrackbarPos('Upper S', 'Trackbars')
    upper_v = cv2.getTrackbarPos('Upper V', 'Trackbars')

    # Define the lower and upper HSV range based on trackbar positions
    lower_blue = np.array([lower_h, lower_s, lower_v])
    upper_blue = np.array([upper_h, upper_s, upper_v])

    # Create a mask with the current HSV range
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply the mask to the original image
    result = cv2.bitwise_and(resized_image, resized_image, mask=mask)

    # Display the mask and the result
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
