# Color-Based Object Tracker

A real-time computer vision app that tracks colored objects using your webcam.

Built with Python and OpenCV.

## What it does

- Opens your webcam and detects a colored object in real time
- Draws a circle around the object and shows its coordinates
- Displays a "mask" window showing exactly what the program sees
- Supports red, blue, green, and yellow out of the box

## Demo

Point your webcam at a **red** object (like a red cup or pen lid) and watch it get tracked live!

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/YOUR_USERNAME/color-tracker.git
   cd color-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the tracker**
   ```bash
   python tracker.py
   ```

5. **Press `Q` to quit**

## Change the tracked color

Open `tracker.py` and change this line near the top:

```python
ACTIVE_COLOR = "red"  # options: "red", "blue", "green", "yellow"
```

## How it works

1. Each webcam frame is converted from BGR to **HSV color space** — HSV separates color (hue) from brightness, making color detection more reliable under different lighting.
2. A **color mask** is created by filtering pixels within the target color's HSV range.
3. **Morphological operations** (erode + dilate) clean up noise in the mask.
4. **Contours** are detected in the mask and the largest one is assumed to be the tracked object.
5. A **minimum enclosing circle** is drawn around that contour on the live feed.

## Tech stack

- Python 3
- OpenCV (`cv2`)
- NumPy

## Skills demonstrated

- Real-time video processing
- HSV color space filtering
- Contour detection
- Computer vision fundamentals with OpenCV
