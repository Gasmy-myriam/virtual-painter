# 🎨 Virtual Painter using Hand Tracking

A real-time **gesture-controlled virtual drawing application** built using **Python, OpenCV, and MediaPipe**.  
This project allows users to draw in the air using only their hand movements — no mouse, no touch required.


---

## 💡 Features

- ✋ Real-time hand tracking using MediaPipe
- 🎨 Gesture-based color selection (Blue, Green, Red, Eraser)
- ✍️ Smooth air-writing with anti-shake filtering
- 🧽 Eraser mode with adjustable thickness
- 🧠 Intelligent gesture detection (Draw / Select modes)
- ⚡ Optimized for real-time performance

---

## 🧠 How It Works

- The webcam captures video in real-time.
- MediaPipe detects **21 hand landmarks**.
- The system tracks the **index finger tip** to draw.
- Gesture logic:
  - **1 finger** → Drawing mode
  - **2 fingers** → Selection mode
- A smoothing algorithm reduces jitter for better writing experience.
- Drawing is rendered on a separate canvas and merged with the video stream.

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy

---



```bash
git clone https://github.com/your-username/virtual-painter-hand-tracking.git
cd virtual-painter-hand-tracking
