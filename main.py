import streamlit as st
import feedparser
import pandas as pd
import requests
from datetime import datetime

# إعداد الصفحة
st.set_page_config(
    page_title="ACU Intel Dashboard",
    layout="wide",
    page_icon="🕵️‍♂️"
)

# =========================
# 🎨 CSS احترافي
# =========================
st.markdown("""
<style>
.stApp { background-color: #050801; }
h1, h2, h3, p, span, label {
    color: #00ff41 !important;
    font-family: 'Courier New', monospace;
}
.stButton>button {
    background-color: #00ff41;
    color: black;
    border-radius: 5px;
    border: none;
    font-weight: bold;
    width: 100%;
    box-shadow: 0 0 10px #00ff41;
}
.stButton>button:hover {
    background-color: #008f11;
    color: white;
}
.block {
    padding: 15px;
    border-radius: 10px;
    background-color: #0a0a0a;
    border: 1px solid #00ff41;
    margin-bottom: 15px;
    box-shadow: 0 0 5px #00ff41;
}
.stTextInput>div>div>input {
    background-color: #101010;
    color: #00ff41;
    border: 1px solid #00ff41;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🧠 العنوان
# =========================
st.title("🕵️‍♂️ ACU Intelligence Center")
st.write("---")

# =========================
# ⚡ Cache لتسريع الأداء
# =========================
@st.cache_data(ttl=600)
def load_feed(url):
    return feedparser.parse(url)

@st.cache_data(ttl=600)
def get_ip_info(target):
    return requests.get(f"http://ip-api.com/json/{target}").json()

# =========================
# 📊 Sidebar
# =========================
st.sidebar.image("https://img.icons8.com/neon/96/shield.png")
st.sidebar.title("ACU Control Panel")

option = st.sidebar.selectbox(
    "اختر المهمة:",
    ["آخر التهديدات", "فحص سريع (IP/Domain)", "عن الوحدة"]
)

# =========================
# 🔹 التهديدات
# =========================
if option == "آخر التهديدات":

    st.markdown("### 📡 رصد التهديدات السيبرانية")
    st.write(f"🕒 {datetime.now().strftime('%Y-%m-%d | %H:%M:%S')}")

    search = st.text_input("🔍 بحث:")

    feeds = {
        "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
        "Bleeping Computer": "https://www.bleepingcomputer.com/feed/"
    }

    for name, url in feeds.items():
        with st.expander(f"🛡️ {name}", expanded=True):
            try:
                with st.spinner("تحميل البيانات..."):
                    feed = load_feed(url)

                for entry in feed.entries[:10]:

                    if search and search.lower() not in entry.title.lower():
                        continue

                    st.markdown(f"""
                    <div class="block">
                        <b>{entry.title}</b><br>
                        <small>{entry.published}</small><br><br>
                        {entry.summary[:200]}...
                        <br>
                        <a href="{entry.link}" style="color:#00ff41;">
                        📄 قراءة كاملة
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

            except:
                st.error(f"فشل تحميل {name}")

# =========================
# 🔹 فحص IP
# =========================
elif option == "فحص سريع (IP/Domain)":

    st.markdown("### 🌐 تحليل IP")

    target = st.text_input("أدخل IP أو Domain:")

    if st.button("🔎 تحليل"):

        if target:
            try:
                with st.spinner("جارٍ التحليل..."):
                    res = get_ip_info(target)

                if res.get("status") == "success":

                    st.success(f"تم تحليل: {res.get('query')}")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("الدولة", res.get("country"))
                        st.write("🏙️ المدينة:", res.get("city"))

                    with col2:
                        st.metric("المزود", res.get("isp"))
                        st.write("📡 AS:", res.get("as"))

                    with col3:
                        st.metric("المنطقة الزمنية", res.get("timezone"))
                        st.write("📍 الموقع:", f"{res.get('lat')}, {res.get('lon')}")

                    # خريطة
                    map_data = pd.DataFrame({
                        'lat': [res.get('lat')],
                        'lon': [res.get('lon')]
                    })
                    st.map(map_data)

                else:
                    st.error("IP غير صالح")

            except:
                st.error("فشل الاتصال")

# =========================
# 🔹 عن الوحدة
# =========================
elif option == "عن الوحدة":

    st.markdown("""
    <div class="block" style="text-align:center;">
        <h2>ACU - Cyber Intelligence Unit</h2>
        <p>نظام OSINT لجمع وتحليل المعلومات.</p>
        <hr style="border-color:#00ff41;">
        <ul style="list-style:none;">
            <li>✅ تحليل التهديدات</li>
            <li>✅ تتبع IP</li>
            <li>✅ مراقبة الأخبار</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
