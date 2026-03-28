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
    page_title="ACU Pro Intelligence",
    layout="wide",
    page_icon="🧠"
)

# =========================
# 🎨 تصميم احترافي
# =========================
st.markdown("""
<style>
.stApp { background-color: #030303; }
h1, h2, h3, p, span, label {
    color: #00ffcc !important;
    font-family: monospace;
}
.block {
    background: #0a0a0a;
    border: 1px solid #00ffcc;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
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
# 🧠 تحليل تهديد بسيط
# =========================
def threat_score(text):
    keywords = ["ransomware", "attack", "breach", "exploit", "malware"]
    score = sum(1 for k in keywords if k in text.lower())
    return min(score * 20, 100)

# =========================
# 🌐 DNS lookup
# =========================
def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

# =========================
# 🧠 UI
# =========================
st.title("🧠 ACU Pro Intelligence System")

menu = st.sidebar.selectbox("📊 اختر:", [
    "Threat Feed",
    "IP Analyzer",
    "Domain Intelligence",
    "Dashboard Stats"
])

# =========================
# 🔹 Threat Feed
# =========================
if menu == "Threat Feed":

    st.subheader("📡 Live Cyber Threats")

    feeds = {
        "HackerNews": "https://feeds.feedburner.com/TheHackersNews",
        "Bleeping": "https://www.bleepingcomputer.com/feed/"
    }

    data = []

    for name, url in feeds.items():
        feed = get_feed(url)

        for e in feed.entries[:10]:
            score = threat_score(e.title + e.summary)
            data.append({
                "Source": name,
                "Title": e.title,
                "Threat Score": score,
                "Link": e.link
            })

    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True)

    # تنبيه
    high_threats = df[df["Threat Score"] > 60]
    if not high_threats.empty:
        st.error(f"🚨 {len(high_threats)} تهديد عالي الخطورة!")

# =========================
# 🔹 IP Analyzer
# =========================
elif menu == "IP Analyzer":

    target = st.text_input("🌐 أدخل IP أو Domain")

    if st.button("تحليل"):

        if target:
            res = ip_lookup(target)

            if res.get("status") == "success":

                st.success("تم التحليل")

                st.json(res)

                # خريطة
                st.map(pd.DataFrame({
                    "lat": [res["lat"]],
                    "lon": [res["lon"]]
                }))

# =========================
# 🔹 Domain Intelligence
# =========================
elif menu == "Domain Intelligence":

    domain = st.text_input("🔎 Domain")

    if st.button("تحليل Domain"):

        ip = resolve_domain(domain)

        if ip:
            st.success(f"IP: {ip}")
        else:
            st.error("فشل التحليل")

# =========================
# 🔹 Dashboard
# =========================
elif menu == "Dashboard Stats":

    st.subheader("📊 System Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Threat Sources", "2")
    col2.metric("Scanned Today", "128")
    col3.metric("High Risk", "7")

    st.info("⚡ النظام يعمل بكفاءة")
