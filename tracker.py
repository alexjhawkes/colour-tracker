import cv2
import numpy as np

# --- Color ranges in HSV format ---
# You can switch between presets by changing ACTIVE_COLOR below
COLOR_PRESETS = {
    "red": {
        "lower1": np.array([0, 120, 70]),
        "upper1": np.array([10, 255, 255]),
        "lower2": np.array([170, 120, 70]),  # red wraps around in HSV
        "upper2": np.array([180, 255, 255]),
        "display": (0, 0, 255),
    },
    "blue": {
        "lower1": np.array([100, 150, 70]),
        "upper1": np.array([130, 255, 255]),
        "lower2": None,
        "upper2": None,
        "display": (255, 0, 0),
    },
    "green": {
        "lower1": np.array([40, 70, 70]),
        "upper1": np.array([80, 255, 255]),
        "lower2": None,
        "upper2": None,
        "display": (0, 255, 0),
    },
    "yellow": {
        "lower1": np.array([20, 100, 100]),
        "upper1": np.array([35, 255, 255]),
        "lower2": None,
        "upper2": None,
        "display": (0, 255, 255),
    },
}

# --- Change this to "blue", "green", or "yellow" ---
ACTIVE_COLOR = "red"


def build_mask(hsv_frame, color):
    mask = cv2.inRange(hsv_frame, color["lower1"], color["upper1"])
    if color["lower2"] is not None:
        mask2 = cv2.inRange(hsv_frame, color["lower2"], color["upper2"])
        mask = cv2.bitwise_or(mask, mask2)
    # Clean up noise with morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    return mask


def find_largest_contour(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    return max(contours, key=cv2.contourArea)


def main():
    color = COLOR_PRESETS[ACTIVE_COLOR]
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print(f"Tracking color: {ACTIVE_COLOR.upper()}")
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame from webcam.")
            break

        frame = cv2.flip(frame, 1)  # mirror like a selfie camera
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = build_mask(hsv, color)

        contour = find_largest_contour(mask)
        if contour is not None and cv2.contourArea(contour) > 500:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            cx, cy = int(x), int(y)
            radius = int(radius)

            # Draw tracking circle and center dot
            cv2.circle(frame, (cx, cy), radius, color["display"], 3)
            cv2.circle(frame, (cx, cy), 5, color["display"], -1)

            # Show coordinates
            label = f"{ACTIVE_COLOR.upper()} ({cx}, {cy})"
            cv2.putText(frame, label, (cx - radius, cy - radius - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color["display"], 2)

        # Show instructions on screen
        cv2.putText(frame, f"Tracking: {ACTIVE_COLOR.upper()}  |  Press Q to quit",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Color Tracker", frame)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
