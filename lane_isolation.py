# Lane detection: road region = black, everything else = white
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Read image and preprocess
img = cv2.imread("road.jpg")
img = cv2.resize(img, (800, 800))
blur = cv2.GaussianBlur(img, (5, 5), 0)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

# 2. Colour filtering
hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
road = cv2.inRange(hsv, (0, 0, 10), (180, 85, 235))   # grey road: low saturation
white = cv2.inRange(hsv, (0, 0, 220), (180, 40, 255))  # white lane line

# 3. Edge detection (for display)
edges = cv2.Canny(gray, 50, 150)

# 4. ROI: ignore the sky (top part of the image)
roi = np.zeros_like(gray)
roi[370:, :] = 255
road = cv2.bitwise_and(road, roi)
white = cv2.bitwise_and(white, roi)

# 5. Lane region: join road + line, clean up, keep the biggest blob
region = cv2.bitwise_or(road, white)
kernel = np.ones((9, 9), np.uint8)
region = cv2.morphologyEx(region, cv2.MORPH_OPEN, kernel)
big_kernel = np.ones((25, 25), np.uint8)
region = cv2.morphologyEx(region, cv2.MORPH_CLOSE, big_kernel)   # fill dark patches
contours, _ = cv2.findContours(region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
biggest = max(contours, key=cv2.contourArea)
region = np.zeros_like(gray)
cv2.drawContours(region, [biggest], -1, 255, cv2.FILLED)   # fill the real road outline
region = cv2.GaussianBlur(region, (31, 31), 0)             # smooth the jagged edge
region = np.where(region > 127, 255, 0).astype(np.uint8)

# 6. Keep the white lane line white (it is a boundary marking)
region[white > 0] = 0

# 7. Final bitmap: lane = black (0), background = white (255)
bitmap = np.where(region > 0, 0, 255).astype(np.uint8)
cv2.imwrite("lane_bitmap.png", bitmap)

# Show the steps
overlay = img.copy()
outline, _ = cv2.findContours(region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(overlay, outline, -1, (0, 0, 255), 3)
steps = [("Original", cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), ("Grayscale", gray),
         ("Road threshold", road), ("White line", white),
         ("Edges", edges), ("Lane region", region),
         ("Boundary", cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)), ("Final bitmap", bitmap)]
for i, (title, im) in enumerate(steps):
    plt.subplot(2, 4, i + 1)
    plt.imshow(im, cmap="gray")
    plt.title(title)
    plt.axis("off")
plt.savefig("pipeline_steps.png")
plt.show()
