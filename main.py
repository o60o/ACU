import streamlit as st
import feedparser
import pandas as pd
import requests
import socket
from datetime import datetime

# =========================
# ⚙️ إعداد الصفحة
# =========================
st.set_page_config(
    page_title="ACU Intelligence System",
    layout="wide",
    page_icon="🧠"
)

# =========================
# 🎬 CSS سينمائي احترافي
# =========================
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle, #010101, #000000);
    color: #00ffcc;
    font-family: 'Courier New', monospace;
}

/* Grid استخباراتي */
.stApp::before {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background-image:
        linear-gradient(rgba(0,255,204,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,204,0.05) 1px, transparent 1px);
    background-size: 40px 40px;
    z-index: 0;
}

/* العناوين */
h1, h2, h3 {
    text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
}

/* Cursor */
h1::after {
    content: "|";
    animation: blink 1s infinite;
}
@keyframes blink {
    50% {opacity:0;}
}

/* كارد */
.block {
    background: rgba(0,255,204,0.05);
    border: 1px solid #00ffcc;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px #00ffcc;
    transition: 0.3s;
}
.block:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px #00ffcc;
}

/* أزرار */
.stButton>button {
    background: black;
    color: #00ffcc;
    border: 1px solid #00ffcc;
    box-shadow: 0 0 10px #00ffcc;
}
.stButton>button:hover {
    background: #00ffcc;
    color: black;
}

/* إدخال */
.stTextInput input {
    background: black;
    color: #00ffcc;
    border: 1px solid #00ffcc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #000;
    border-right: 1px solid #00ffcc;
}

/* Scan lines */
body::after {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background: repeating-linear-gradient(
        transparent,
        transparent 2px,
        rgba(0,255,204,0.03) 3px
    );
    pointer-events: none;
}

</style>
""", unsafe_allow_html=True)

# =========================
# ⚡ Cache
# =========================
@st.cache_data(ttl=600)
def get_feed(url):
    return feedparser.parse(url)

@st.cache_data(ttl=600)
def ip_lookup(target):
    return requests.get(f"http://ip-api.com/json/{target}").json()

# =========================
# 🧠 تحليل تهديد
# =========================
def threat_score(text):
    keywords = ["ransomware", "attack", "breach", "exploit", "malware"]
    score = sum(1 for k in keywords if k in text.lower())
    return min(score * 20, 100)

# =========================
# 🌐 DNS
# =========================
def resolve(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

# =========================
# 🧠 UI
# =========================
st.title("🧠 ACU Intelligence System")
st.write("---")

menu = st.sidebar.selectbox("📊 التحكم", [
    "Threat Feed",
    "IP Analyzer",
    "Domain Intelligence",
    "Dashboard"
])

# =========================
# 🔹 Threat Feed
# =========================
if menu == "Threat Feed":

    st.subheader("📡 Live Threat Intelligence")

    feeds = {
        "HackerNews": "https://feeds.feedburner.com/TheHackersNews",
        "Bleeping": "https://www.bleepingcomputer.com/feed/"
    }

    data = []

    for name, url in feeds.items():
        feed = get_feed(url)

        for e in feed.entries[:8]:
            score = threat_score(e.title + e.summary)

            data.append({
                "Source": name,
                "Title": e.title,
                "Threat": score,
                "Link": e.link
            })

    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True)

    high = df[df["Threat"] > 60]
    if not high.empty:
        st.error(f"🚨 {len(high)} HIGH THREATS DETECTED")

# =========================
# 🔹 IP Analyzer
# =========================
elif menu == "IP Analyzer":

    st.subheader("🌐 IP Intelligence")

    target = st.text_input("Enter IP or Domain")

    if st.button("Analyze"):

        res = ip_lookup(target)

        if res.get("status") == "success":

            st.success("Analysis Complete")

            st.json(res)

            st.map(pd.DataFrame({
                "lat": [res["lat"]],
                "lon": [res["lon"]]
            }))

# =========================
# 🔹 Domain
# =========================
elif menu == "Domain Intelligence":

    st.subheader("🔎 Domain Intelligence")

    domain = st.text_input("Enter Domain")

    if st.button("Resolve"):

        ip = resolve(domain)

        if ip:
            st.success(f"Resolved IP: {ip}")
        else:
            st.error("Failed")

# =========================
# 🔹 Dashboard
# =========================
elif menu == "Dashboard":

    st.subheader("📊 System Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Sources", "2")
    c2.metric("Scanned", "120+")
    c3.metric("Threats", "5")

    st.info("🟢 SYSTEM ACTIVE")
