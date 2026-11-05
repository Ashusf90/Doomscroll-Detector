import streamlit as st
import streamlit.components.v1 as components
import streamlit_webrtc
import av
import cv2
import time
import threading

from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from app.detection.detector import PhoneDetector
from app.tracking.usage_tracker import UsageTracker
from app.alerts.alert_manager import AlertManager

st.set_page_config(
    page_title="Doomscroll Detector",
    page_icon="📵",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: radial-gradient(ellipse at 50% -20%, #292929, transparent 55%),
                linear-gradient(145deg, #080808, #111111, #080808);
    color: white;
}
.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}
header, footer {visibility: hidden;}

.hero, .metric-card {
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 12px 35px #00000055,
                inset 0 1px 0 #ffffff18;
}
.hero {margin-bottom: 25px;}
.hero h1 {font-size: 35px; font-weight: 800; color: white;}
.hero p, .stCaption {color: #999;}
.section-title {
    font-size: 18px;
    font-weight: 700;
    margin: 25px 0 15px;
}
.metric-card {min-height: 110px;}
.metric-label {
    color: #999;
    font-size: 11px;
    letter-spacing: 1px;
}
.metric-value {
    color: white;
    font-size: 27px;
    font-weight: 700;
    margin-top: 12px;
}
div.stButton > button {
    background: #eeeeee;
    color: #111111;
    border: 1px solid #eeeeee;
    border-radius: 10px;
    font-weight: 700;
    height: 44px;
}
div.stButton > button:hover {
    background: #cccccc;
    color: black;
}
div[data-testid="stAlert"] {
    background: #171717;
    border: 1px solid #333;
    border-radius: 12px;
}
hr {border-color: #333;}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_detector():
    return PhoneDetector()


class PhoneVideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.detector = load_detector()
        self.tracker = UsageTracker()
        self.lock = threading.Lock()
        self.detected = False
        self.seconds = 0
        self.sessions = 0

    def recv(self, frame):
        image = frame.to_ndarray(format="bgr24")
        image = cv2.flip(image, 1)

        image, detections = self.detector.detect(image)

        with self.lock:
            self.seconds = self.tracker.update(bool(detections))
            self.sessions = self.tracker.get_sessions()
            self.detected = bool(detections)

        return av.VideoFrame.from_ndarray(image, format="bgr24")


st.markdown("""
<div class="hero">
    <div style="color:#999;font-size:11px;letter-spacing:2px">
        COMPUTER VISION · DIGITAL WELLNESS
    </div>
    <h1>DOOMSCROLL DETECTOR.</h1>
    <p>Monitor phone usage. Understand your habits. Take back your time.</p>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="section-title">Monitoring settings</div>',
            unsafe_allow_html=True)

limit = st.slider("Usage alert threshold", 10, 300, 60,
                  format="%d seconds")


st.markdown('<div class="section-title">Overview</div>',
            unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
total_display = m1.empty()
sessions_display = m2.empty()
status_display = m3.empty()


def metric_card(placeholder, label, value):
    placeholder.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def update_dashboard(seconds, sessions):
    metric_card(total_display, "TOTAL DETECTED TIME", f"{seconds}s")
    metric_card(sessions_display, "DETECTION SESSIONS", str(sessions))

    if seconds >= limit:
        color, message = "#ff8585", "LIMIT REACHED"
    elif seconds >= limit * 0.75:
        color, message = "#cccccc", "APPROACHING LIMIT"
    else:
        color, message = "#ffffff", "WITHIN LIMIT"

    metric_card(
        status_display,
        "CURRENT STATUS",
        f'<span style="color:{color};font-size:20px">{message}</span>'
    )


st.markdown('<div class="section-title">Live webcam monitoring</div>',
            unsafe_allow_html=True)

ctx = webrtc_streamer(
    key="doomscroll-camera",
    video_processor_factory=PhoneVideoProcessor,
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    async_processing=True
)

alert_display = st.empty()

if ctx.video_processor:
    processor = ctx.video_processor

    while ctx.state.playing:
        with processor.lock:
            seconds = processor.seconds
            sessions = processor.sessions
            detected = processor.detected

        update_dashboard(seconds, sessions)

        message = AlertManager.get_alert(seconds, limit)

        if seconds >= limit:
            alert_display.error(message)
        elif seconds >= limit * 0.75:
            alert_display.warning(message)
        elif detected:
            alert_display.success("Phone detected. Monitoring usage.")
        else:
            alert_display.info("No phone detected.")

        time.sleep(1)

else:
    update_dashboard(0, 0)
    st.info("Start the webcam above to begin phone detection.")


st.markdown("""
<hr>
<div style="text-align:center;color:#888;font-size:11px;padding:15px">
DOOMSCROLL DETECTOR · PYTHON · YOLO · OPENCV
<br><br>
MONITOR YOUR HABITS. RECLAIM YOUR TIME.
</div>
""", unsafe_allow_html=True)
