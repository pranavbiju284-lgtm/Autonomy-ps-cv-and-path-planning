IVDC Autonomy 2026 – Induction Problem Statements

Solutions for the IVDC induction by Pranav Biju.

This repo covers:

PS 1 – Computer Vision: lane/road isolation on the provided road image (Part B)
PS 2 – Motion Planning: grid-based Dijkstra path planner with visualization (Part B)

Part A research PDFs are in docs/.

Repository structure
ps1_computer_vision/
    lane_detection.py      # lane isolation pipeline
    road.jpg               # provided test image
ps2_path_planning/
    planner.py             # Dijkstra on a 2D grid + visualization
docs/                      # Part A PDFs, result screenshots and plots
requirements.txt
README.md
Dependencies
Python 3.9 or newer
opencv-python
numpy
matplotlib

he provided road image and output a binary bitmap where the region between the lane boundaries is black and everything else is white.

Preprocessing: resize to 800x800, Gaussian blur (5x5) to reduce noise, convert to grayscale.
Colour filtering (HSV): the road is grey, so it has low saturation; the lane line is white, so it has high brightness and low saturation. Two cv2.inRange masks pick these out.
Edge detection: Canny edges on the grayscale image (used for display and analysis).
ROI: the top part of the image (the sky) is masked out so it cannot be mistaken for road.
Lane region: road and line masks are combined, cleaned with morphological opening (remove specks) and closing (fill dark patches), then the largest contour is kept and filled.
Smoothing: the filled region is blurred and re-thresholded to smooth the jagged boundary.
Final bitmap: the region is black (0) and the background is white (255). The white lane line pixels are excluded from the region so the line stays white.


Limitations:

HSV thresholds and the ROI row (370) were tuned for this one image. A different image, lighting, or camera angle would need re-tuning.
Grey roadside areas or shadows can be mistaken for road because the road mask relies on low saturation.
The method assumes one large road region; it does not detect individual lane lines with the Hough transform.
Bonus extensions (lighting changes, missing boundary, drivable-area cost map) are not attempted yet.
PS 2 – Grid-Based Path Planning Visualization

Goal: implement a search algorithm on a 2D grid and visualize how it explores the map.

Approach:

The map is a 15x15 NumPy array (0 = free, 1 = obstacle).
Dijkstra's algorithm is implemented from scratch using a priority queue (heapq), with a dist dictionary for the best known distance and a parent dictionary to reconstruct the path.
Movement is 4-directional (up, down, left, right) with a cost of 1 per move. With equal costs, Dijkstra explores the same way as BFS.
Cells are recorded in the order they are explored, and the final path is rebuilt by walking back through parent from the goal.

How to run:

bash
cd ps2_path_planning
python planner.py

Output: the number of explored cells and the path length are printed, and a plot is saved as dijkstra_result.png showing:

Element	Shown as
Free cells	white
Obstacles	black
Start	green dot
Goal	gold star
Explored cells	light-blue squares
Final path	red line


Limitations:

Only Dijkstra is implemented so far; no comparison with BFS or A*.
All cells cost the same, so variable movement costs and re-planning around a new obstacle (the bonus tasks) are not attempted yet.
The grid is hardcoded in the script.
Use of AI and external resources

I used the following as learning aids, in line with the induction guidelines:

Claude for research ,learning, help and debugging the code.

Youtube channels like veritasium helped a lot in its gmaps video, also many other videos .

References
OpenCV-Python tutorials: Changing Colorspaces, Smoothing Images, Canny Edge Detection, Contours. https://docs.opencv.org
YouTube: https://www.youtube.com/watch?v=kS-CGkiPetQ&t=444s

