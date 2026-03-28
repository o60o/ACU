import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<style>
/* Background Grid */
body, .stApp {
    background: #0b0b0b;
    font-family: 'Share Tech Mono', monospace;
    color: #00ffff;
    overflow: hidden;
    position: relative;
}

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

/* Scanline */
.scanline {
    position: fixed;
    width: 100%;
    height: 2px;
    background: rgba(0,255,204,0.1);
    animation: scanMove 3s linear infinite;
    top:0; left:0;
    z-index:1;
}
@keyframes scanMove { 0% {top:-2px;} 100% {top:100%;} }

/* HUD Panels */
.hud {
    position: fixed;
    border: 1px solid #00ffff;
    border-radius: 5px;
    padding: 10px;
    backdrop-filter: blur(5px);
    box-shadow: 0 0 20px #00ffff;
    z-index: 2;
}

.top-left { top: 20px; left: 20px; }
.top-right { top: 20px; right: 20px; }
.bottom-left { bottom: 20px; left: 20px; }
.bottom-right { bottom: 20px; right: 20px; }

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
    content:'';
    position: absolute;
    width: 2px;
    height: 80px;
    background:#00ffff;
    top:0; left:50%;
    transform-origin: bottom;
}
@keyframes rotateRadar { 0% {transform:rotate(0deg);} 100% {transform:rotate(360deg);} }

.data-line {
    border-bottom:1px dashed #00ffff;
    padding:2px;
    font-size:12px;
}
</style>

<div class="scanline"></div>

<div class="hud top-left">
    <div class="radar"></div>
    <div class="data-line">Threat: 85%</div>
    <div class="data-line">Nodes: 1,256</div>
    <div class="data-line">IP: 192.168.1.1</div>
</div>

<div class="hud top-right">
    <div class="data-line">SYSTEM STATUS: ACTIVE</div>
    <div class="data-line">CPU: 45%</div>
    <div class="data-line">MEM: 68%</div>
</div>

<div class="hud bottom-left">
    <div class="radar"></div>
    <div class="data-line">Incoming Packets</div>
</div>

<div class="hud bottom-right">
    <div class="data-line">Network Stability</div>
    <div class="data-line">Connection: 99%</div>
</div>
""", unsafe_allow_html=True)
