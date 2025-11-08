## **Vehicle Counter & Tracker**  
**Real-time car detection, tracking, and line-crossing analytics from video footage**

*Detect • Track • Count • Analyze*

This project analyzes road traffic videos to detect vehicles, track their movement, and count how many cross defined boundary lines. It also records entry and exit timestamps for each vehicle.

---

## **Tech Highlights**

| Feature | Description |
|-------|-----------|
| **Motion Detection** | Background subtraction with `cv2.absdiff` + Gaussian blur |
| **Object Tracking** | Custom centroid-based tracker with ID persistence |
| **Interactive Line Drawing** | Click-and-drag to define counting zones |
| **Entry/Exit Analytics** | Logs entry/exit time per car + duration |
| **CSV Export** | Full analytics table: `car_id`, `entry_line`, `exit_line`, `duration` |
| **Visual Feedback** | Bounding boxes, IDs, trails, line counters, FPS |

---

## System Architecture

```mermaid
flowchart LR
A[Video Input] 
B[Frame Preprocessing]
C[Motion Detection (Frame Differencing + Threshold + Dilate)]
D[Contour Extraction] 
E[Custom Object Tracker]
F[Assign IDs & Track Movement]
G[Line Crossing Logic + Count Vehicles]
H[Save Logs to CSV]
I[Visual Output + Counters]
```
## Usage

- Place your video as **intersection_video.mp4 in the root**.
- Run the script: bash python motion_detector.py
- Draw lines on the first frame using left-click + drag.
- Press ESC to start processing.
- **Press q to quit and save results**.
- Output: intersection_video_table.csv

## Future Enhancements

- Deep learning model (YOLOv8) for multi-class detection
- Web dashboard with Flask/FastAPI
- Heatmap visualization of traffic flow
- Multi-camera stitching & global counting
