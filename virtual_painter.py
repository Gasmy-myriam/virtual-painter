import cv2
import mediapipe as mp
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Canvas for drawing
canvas = None

# Previous drawing positions
xp, yp = 0, 0

# Smoothed coordinates (to reduce jitter)
smooth_x, smooth_y = 0, 0
smooth_factor = 0.2  # Lower value = smoother movement

# Default drawing color (Blue)
draw_color = (255, 0, 0)
color_name = "BLUE"

while True:
    # Capture frame from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror the image

    # Initialize canvas once
    if canvas is None:
        canvas = np.zeros_like(img)

    # ===================== UI BUTTONS =====================
    # Draw color selection buttons
    cv2.rectangle(img, (0, 0), (100, 50), (255, 0, 0), -1)   # Blue
    cv2.rectangle(img, (100, 0), (200, 50), (0, 255, 0), -1) # Green
    cv2.rectangle(img, (200, 0), (300, 50), (0, 0, 255), -1) # Red
    cv2.rectangle(img, (300, 0), (400, 50), (0, 0, 0), -1)   # Eraser

    # Add labels to buttons
    cv2.putText(img, "BLUE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv2.putText(img, "GREEN", (110, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)
    cv2.putText(img, "RED", (220, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv2.putText(img, "ERASER", (305, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

    # Convert image to RGB (required by MediaPipe)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    mode = "DRAW"

    # ===================== HAND DETECTION =====================
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            h, w, c = img.shape

            # Get index finger tip coordinates
            x1 = int(handLms.landmark[8].x * w)
            y1 = int(handLms.landmark[8].y * h)

            # Get middle finger tip coordinates
            x2 = int(handLms.landmark[12].x * w)
            y2 = int(handLms.landmark[12].y * h)

            # ===================== SELECTION MODE =====================
            # If index finger is above middle finger → selection mode
            if y1 < y2:
                mode = "SELECT"
                xp, yp = 0, 0  # Reset previous points

                # Check if finger is in top bar (button area)
                if y1 < 50:
                    if x1 < 100:
                        draw_color = (255, 0, 0)
                        color_name = "BLUE"
                    elif x1 < 200:
                        draw_color = (0, 255, 0)
                        color_name = "GREEN"
                    elif x1 < 300:
                        draw_color = (0, 0, 255)
                        color_name = "RED"
                    elif x1 < 400:
                        draw_color = (0, 0, 0)
                        color_name = "ERASER"

            # ===================== DRAW MODE =====================
            else:
                mode = "DRAW"

                # Apply smoothing to reduce jitter
                smooth_x = int(smooth_x + (x1 - smooth_x) * smooth_factor)
                smooth_y = int(smooth_y + (y1 - smooth_y) * smooth_factor)

                # Draw cursor circle
                cv2.circle(img, (smooth_x, smooth_y), 8, draw_color, cv2.FILLED)

                # Initialize previous position
                if xp == 0 and yp == 0:
                    xp, yp = smooth_x, smooth_y

                # Adjust thickness (larger for eraser)
                thickness = 6 if draw_color != (0,0,0) else 30

                # Interpolate points for smoother lines
                for i in range(1, 5):
                    ix = int(xp + (smooth_x - xp) * i / 5)
                    iy = int(yp + (smooth_y - yp) * i / 5)
                    cv2.line(canvas, (xp, yp), (ix, iy), draw_color, thickness)

                # Update previous position
                xp, yp = smooth_x, smooth_y

            # Draw hand landmarks
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    # ===================== MERGE CANVAS =====================
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, inv)
    img = cv2.bitwise_or(img, canvas)

    # ===================== UI TEXT =====================
    cv2.putText(img, f"Mode: {mode}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.putText(img, f"Color: {color_name}", (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    # Display output
    cv2.imshow("Virtual Painter PRO", img)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()