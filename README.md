#  Doomscroll Detector

### AI-Powered Smartphone Detection & Digital Wellness Monitor

Doomscroll Detector is a real-time computer vision application that detects smartphone presence through a webcam, tracks phone detection duration, and encourages users to take breaks through configurable alerts.

Built using **Python, YOLO, OpenCV, and Streamlit**, this project explores practical applications of Computer Vision and AI for digital wellness.

##  Key Features

-  **Real-Time Phone Detection** – Detect smartphones using YOLO.
-  **Live Webcam Monitoring** – Process webcam frames using OpenCV.
-  **Usage Tracking** – Measure continuous phone detection duration.
-  **Smart Alerts** – Receive warnings when detection time reaches the configured threshold.
-  **Usage Analytics** – Visualize daily detected phone usage.
-  **Session History** – Record completed detection sessions.
-  **CSV Export** – Download usage reports for further analysis.
-  **Modern Dashboard** – Minimal black and dark-grey UI with Apple-inspired glassmorphism effects.

##  Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| YOLO (Ultralytics) | Smartphone detection |
| OpenCV | Webcam and image processing |
| Streamlit | Interactive web interface |
| Pandas | Data processing and analytics |
| NumPy | Numerical operations |

##  How It Works

1. The webcam captures live video.
2. YOLO analyzes video frames and identifies smartphones.
3. OpenCV displays bounding boxes around detected phones.
4. The usage tracker measures continuous detection duration.
5. The alert manager generates warnings based on the configured time limit.
6. Completed detection sessions are stored locally.
7. Streamlit displays usage statistics and session history.

**Important:** The current version detects smartphone presence and estimates detection duration. It does not directly recognize scrolling activity or determine user intent.

## 📂 Project Structure

```text
Doomscroll-Detector/
│
├── app/
│   ├── detection/
│   │   ├── __init__.py
│   │   └── detector.py
│   │
│   ├── tracking/
│   │   ├── __init__.py
│   │   └── usage_tracker.py
│   │
│   ├── alerts/
│   │   ├── __init__.py
│   │   └── alert_manager.py
│   │
│   └── __init__.py
│
├── data/
│   └── usage_history.json
│
├── models/
├── frontend.py
├── requirements.txt
├── .gitignore
└── README.md
```

##  Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ashusf90/Doomscroll-Detector.git
cd Doomscroll-Detector
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate the environment:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows**
```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run frontend.py
```

Open the application in your browser:

`http://localhost:8501`

### 5. Start monitoring

1. Allow webcam access.
2. Configure the phone detection time limit.
3. Click **START MONITORING**.
4. Hold a smartphone in front of the webcam.
5. View detection results, usage duration, and alerts.

The YOLO model weights are downloaded automatically on the first run.

##  Usage Analytics

The application maintains completed detection sessions in:

`data/usage_history.json`

The dashboard provides:
- Total detected phone duration
- Number of detection sessions
- Daily usage chart
- Session history
- Downloadable CSV reports

##  Privacy

- Webcam processing runs locally in the current application.
- Usage history is stored locally.
- No cloud database or user account is required.

##  Future Improvements

- Browser-based camera support for cloud deployment.
- Improved smartphone detection accuracy.
- Daily and weekly usage insights.
- Customizable break reminders.
- Advanced phone-use tracking.
- Persistent cloud-based analytics.

##  Author

**Ashu Gupta**

B.Tech – Computer Science and Engineering (AI)

Live Link:  https://doomscroll-detector-a6xueptirftsoz6ezdk7hz.streamlit.app/
GitHub: [Ashusf90](https://github.com/Ashusf90)

**Project Repository:** [Doomscroll Detector](https://github.com/Ashusf90/Doomscroll-Detector)

---

⭐ If you find this project interesting, consider giving the repository a star!

*Built with Python, YOLO, OpenCV, and Streamlit.*
