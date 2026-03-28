import streamlit as st
import feedparser
import pandas as pd
import requests
import socket

st.set_page_config(page_title="ACU Intelligence System", layout="wide", page_icon="🧠")

# =========================
# 🎬 CSS HUD سينمائي متقدم
# =========================
st.markdown("""
<style>
/* =====================
   🌌 Base & Background
===================== */
.stApp {
    background: #0b0b0b;
    color: #00ffff;
    font-family: 'Share Tech Mono', monospace;
    overflow: hidden;
    position: relative;
}

/* =====================
   🔹 Grid HUD
===================== */
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

/* =====================
   🕹️ HUD Panels
===================== */
.hud {
    position: relative;
    border: 1px solid #00ffff;
    border-radius: 5px;
    padding: 10px;
    backdrop-filter: blur(5px);
    box-shadow: 0 0 20px #00ffff;
    margin-bottom: 10px;
}

/* =====================
   ⚙️ Circular Radars
===================== */
.radar {
    position: relative;
    width: 80px;
    height: 80px;
    border: 2px solid #00ffff;
    border-radius: 50%;
    margin-bottom: 5px;
    animation: rotateRadar 4s linear infinite;
}
.radar::after {
    content: '';
    position: absolute;
    width: 2px;
    height: 80px;
    background: #00ffff;
    top: 0;
    left: 50%;
    transform-origin: bottom;
}
@keyframes rotateRadar {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* =====================
   🔢 Numbers & Data
===================== */
.data-line {
    border-bottom: 1px dashed #00ffff;
    padding: 2px;
    font-size: 12px;
}

/* =====================
   💡 Scanlines
===================== */
.scanline {
    position: fixed;
    width: 100%;
    height: 2px;
    background: rgba(0,255,204,0.1);
    animation: scanMove 3s linear infinite;
    top:0; left:0;
    z-index:1;
}
@keyframes scanMove {
    0% { top: -2px; }
    100% { top: 100%; }
}

/* =====================
   ⚡ Glow Effects
===================== */
.hud::before {
    content: '';
    position: absolute;
    top:-5px; left:-5px; right:-5px; bottom:-5px;
    border: 1px solid #00ffff;
    opacity: 0.3;
    filter: blur(4px);
}
</style>
""", unsafe_allow_html=True)

# =====================
# 🌌 HUD HTML داخل Streamlit
# =====================
st.markdown("""
<div class="scanline"></div>

<div class="hud">
    <div class="radar"></div>
    <div class="data-line">Threat: 85%</div>
    <div class="data-line">Nodes: 1,256</div>
    <div class="data-line">IP: 192.168.1.1</div>
</div>

<div class="hud">
    <div class="data-line">SYSTEM STATUS: ACTIVE</div>
    <div class="data-line">CPU: 45%</div>
    <div class="data-line">MEM: 68%</div>
</div>

<div class="hud">
    <div class="radar"></div>
    <div class="data-line">Incoming Packets</div>
</div>

<div class="hud">
    <div class="data-line">Network Stability</div>
    <div class="data-line">Connection: 99%</div>
</div>
""", unsafe_allow_html=True)

# =========================
# ⚡ Streamlit Functionality (Threat Feed / IP / Domain / Dashboard)
# =========================
menu = st.sidebar.selectbox("📊 التحكم", [
    "Threat Feed",
    "IP Analyzer",
    "Domain Intelligence",
    "Dashboard"
])

# ⚡ Threat Feed
@st.cache_data(ttl=600)
def get_feed(url):
    return feedparser.parse(url)

@st.cache_data(ttl=600)
def ip_lookup(target):
    return requests.get(f"http://ip-api.com/json/{target}").json()

def threat_score(text):
    keywords = ["ransomware", "attack", "breach", "exploit", "malware"]
    score = sum(1 for k in keywords if k in text.lower())
    return min(score * 20, 100)

def resolve(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

if menu == "Threat Feed":
    st.subheader("📡 Live Threat Intelligence")
    feeds = {"HackerNews": "https://feeds.feedburner.com/TheHackersNews",
             "Bleeping": "https://www.bleepingcomputer.com/feed/"}
    data=[]
    for name,url in feeds.items():
        feed = get_feed(url)
        for e in feed.entries[:8]:
            score = threat_score(e.title + e.summary)
            data.append({"Source":name,"Title":e.title,"Threat":score,"Link":e.link})
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    high = df[df["Threat"]>60]
    if not high.empty:
        st.error(f"🚨 {len(high)} HIGH THREATS DETECTED")

elif menu == "IP Analyzer":
    st.subheader("🌐 IP Intelligence")
    target = st.text_input("Enter IP or Domain")
    if st.button("Analyze"):
        res = ip_lookup(target)
        if res.get("status")=="success":
            st.success("Analysis Complete")
            st.json(res)
            st.map(pd.DataFrame({"lat":[res["lat"]],"lon":[res["lon"]]}))

elif menu == "Domain Intelligence":
    st.subheader("🔎 Domain Intelligence")
    domain = st.text_input("Enter Domain")
    if st.button("Resolve"):
        ip = resolve(domain)
        if ip:
            st.success(f"Resolved IP: {ip}")
        else:
            st.error("Failed")

elif menu == "Dashboard":
    st.subheader("📊 System Dashboard")
    c1,c2,c3 = st.columns(3)
    c1.metric("Sources","2")
    c2.metric("Scanned","120+")
    c3.metric("Threats","5")
    st.info("🟢 SYSTEM ACTIVE")
