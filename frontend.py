import streamlit as st
import cv2
import time
import pandas as pd

from app.detection.detector import PhoneDetector
from app.tracking.usage_tracker import UsageTracker
from app.alerts.alert_manager import AlertManager

st.set_page_config(
    page_title="Doomscroll Detector",
    page_icon="◼",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 50% -20%, #292929 0%, transparent 55%),
        linear-gradient(145deg, #080808, #111111 55%, #080808);
    color: #f5f5f5;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 2.5rem;
    padding-bottom: 2rem;
}

header, footer {
    visibility: hidden;
}

/* GLASS HEADER */
.hero {
    position: relative;
    overflow: hidden;
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(28px) saturate(140%);
    -webkit-backdrop-filter: blur(28px) saturate(140%);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 24px;
    padding: 34px;
    margin-bottom: 30px;
    box-shadow: 0 18px 55px rgba(0,0,0,0.35),
                inset 0 1px 0 rgba(255,255,255,0.10);
}

.hero:before {
    content: "";
    position: absolute;
    top: 0;
    left: 8%;
    width: 84%;
    height: 1px;
    background: linear-gradient(90deg, transparent, #ffffff55, transparent);
}

.eyebrow {
    color: #a5a5a5;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.hero h1 {
    font-size: 37px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #ffffff;
    margin: 0;
}

.hero p {
    color: #aaaaaa;
    font-size: 14px;
    margin-top: 10px;
}

/* SECTION HEADINGS */
.section-title {
    font-size: 17px;
    font-weight: 700;
    color: #eeeeee;
    margin: 26px 0 15px;
}

/* FROSTED GLASS METRICS */
.metric-card {
    position: relative;
    overflow: hidden;
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(24px) saturate(130%);
    -webkit-backdrop-filter: blur(24px) saturate(130%);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 19px;
    padding: 23px;
    min-height: 120px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.22),
                inset 0 1px 0 rgba(255,255,255,0.08);
    transition: all 0.25s ease;
}

.metric-card:hover {
    background: rgba(255,255,255,0.085);
    border-color: rgba(255,255,255,0.25);
    transform: translateY(-3px);
}

.metric-label {
    color: #a5a5a5;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
}

.metric-value {
    color: #ffffff;
    font-size: 29px;
    font-weight: 700;
    margin-top: 12px;
}

/* GLASS BUTTONS */
div.stButton > button {
    background: rgba(255,255,255,0.10);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 12px;
    height: 45px;
    font-weight: 650;
    transition: all 0.25s ease;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.12);
}

div.stButton > button:hover {
    background: rgba(255,255,255,0.19);
    color: #ffffff;
    border-color: rgba(255,255,255,0.4);
    box-shadow: 0 8px 25px rgba(255,255,255,0.06);
}

/* SLIDER */
div[data-testid="stSlider"] label {
    color: #cccccc;
}

div[data-testid="stSlider"] [role="slider"] {
    background: #ffffff;
}

/* ALERTS */
div[data-testid="stAlert"] {
    background: rgba(255,255,255,0.065);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 13px;
    color: #eeeeee;
}

/* CAMERA */
div[data-testid="stImage"] img {
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 18px;
    box-shadow: 0 15px 45px rgba(0,0,0,0.35);
}

/* SLIDER AND TEXT */
.stCaption {
    color: #929292;
}

hr {
    border-color: rgba(255,255,255,0.12);
}

</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_detector():
    return PhoneDetector()


if "running" not in st.session_state:
    st.session_state.running = False

if "tracker" not in st.session_state:
    st.session_state.tracker = UsageTracker()

tracker = st.session_state.tracker
detector = load_detector()


# HEADER
st.markdown("""
<div class="hero">
    <div class="eyebrow">COMPUTER VISION · DIGITAL WELLNESS</div>
    <h1>DOOMSCROLL DETECTOR<span style="color:#999">.</span></h1>
    <p>Monitor phone usage. Understand your habits. Take back your time.</p>
</div>
""", unsafe_allow_html=True)


# SETTINGS
left, right = st.columns([2, 1])

with left:
    st.markdown('<div class="section-title">Monitoring settings</div>',
                unsafe_allow_html=True)
    limit = st.slider("Usage alert threshold", 10, 300, 60,
                      format="%d seconds")

with right:
    st.markdown('<div class="section-title">Session controls</div>',
                unsafe_allow_html=True)
    if st.button("↻  Reset statistics", use_container_width=True):
        tracker.reset()
        st.rerun()


# DASHBOARD
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


def update_dashboard(seconds):
    metric_card(total_display, "TOTAL DETECTED TIME", f"{seconds}s")
    metric_card(sessions_display, "DETECTION SESSIONS",
                str(tracker.get_sessions()))

    if seconds >= limit:
        color, message = "#ff8585", "LIMIT REACHED"
    elif seconds >= limit * 0.75:
        color, message = "#d5d5d5", "APPROACHING LIMIT"
    else:
        color, message = "#ffffff", "WITHIN LIMIT"

    status_display.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">CURRENT STATUS</div>
        <div class="metric-value" style="font-size:21px;color:{color}">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)


update_dashboard(tracker.get_total())


# CAMERA
st.markdown('<div class="section-title">Live monitoring</div>',
            unsafe_allow_html=True)

control_col, info_col = st.columns([1, 2])

with control_col:
    if st.button(
        "STOP MONITORING" if st.session_state.running
        else "START MONITORING",
        use_container_width=True
    ):
        st.session_state.running = not st.session_state.running
        st.rerun()

with info_col:
    st.caption("Keep your phone visible to the webcam for real-time detection.")

video = st.empty()
alert_display = st.empty()


if st.session_state.running:
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        st.error("Camera unavailable. Check macOS camera permissions.")
        st.session_state.running = False
    else:
        try:
            while st.session_state.running:
                success, frame = camera.read()

                if not success:
                    st.error("Unable to read camera frame.")
                    break

                frame = cv2.flip(frame, 1)
                frame, detections = detector.detect(frame)

                seconds = tracker.update(bool(detections))
                alert = AlertManager.get_alert(seconds, limit)

                update_dashboard(seconds)

                if seconds >= limit:
                    alert_display.error(alert)
                elif seconds >= limit * 0.75:
                    alert_display.warning(alert)
                else:
                    alert_display.success(alert)

                video.image(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                    channels="RGB",
                    use_container_width=True
                )

                time.sleep(0.03)

        finally:
            camera.release()



# USAGE ANALYTICS
st.markdown('<div class="section-title">Usage analytics</div>',
            unsafe_allow_html=True)

history = tracker.get_history()

if history:
    df = pd.DataFrame(history)
    df["date"] = pd.to_datetime(df["date"])

    daily = (
        df.groupby("date")["duration"]
        .sum()
        .reset_index()
    )
    daily["minutes"] = daily["duration"] / 60

    st.markdown("#### Daily detected phone usage")
    st.bar_chart(daily.set_index("date")["minutes"],
                 y_label="Minutes")

    st.markdown("#### Detection session history")
    display_df = df.copy()
    display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
    display_df["duration"] = display_df["duration"].round(1)
    display_df.columns = ["Date", "Start time", "Duration (seconds)"]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv_data = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="↓ Download Usage Report",
        data=csv_data,
        file_name="doomscroll_usage_report.csv",
        mime="text/csv",
        use_container_width=True
    )
else:
    st.info("No completed detection sessions yet. Start monitoring to build your usage history.")

st.markdown("""
<hr>
<div style="text-align:center;color:#858585;font-size:11px;padding:18px;
letter-spacing:1px">
DOOMSCROLL DETECTOR · BUILT WITH PYTHON, YOLO & OPENCV
<br><br>
MONITOR YOUR HABITS. RECLAIM YOUR TIME.
</div>
""", unsafe_allow_html=True)
