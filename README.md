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
graph TD
    A[Video Input] --> B[Frame Preprocessing]
    B --> C{Motion Detection}
    C --> D[Contour Extraction]
    D --> E[Bounding Boxes]
    E --> F[Tracker.update()]
    F --> G[ID Assignment]
    G --> H[Line Interaction Check]
    H --> I{Entry or Exit?}
    I -->|Entry| J[Log Entry Time]
    I -->|Exit| K[Log Exit Time + Duration]
    J & K --> L[Pandas DataFrame]
    L --> M[CSV Export]
    E --> N[Visualization Layer]
    N --> O[OpenCV Display]
```

---

## Usage

- Place your video as **intersection_video.mp4 in the root**.
- Run the script: bash python motion_detector.py
- Draw lines on the first frame using left-click + drag.
- Press ESC to start processing.
- **Press q to quit and save results**.
- Output: intersection_video_table.csv

---

## Future Enhancements

- Deep learning model (YOLOv8) for multi-class detection
- Web dashboard with Flask/FastAPI
- Heatmap visualization of traffic flow
- Multi-camera stitching & global counting
