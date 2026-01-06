import streamlit as st
import requests
import time

st.set_page_config(page_title="Node B - Receiver", layout="wide")

st.sidebar.title("🔗 Connection Settings")
api_url_b = st.sidebar.text_input("Laptop B API Link", "http://127.0.0.1:8001")

st.title("🛰️ Quantum Node B (Receiver)")
st.write("Monitoring synchronized flipping bits...")

placeholder = st.empty()

# Persistent state to avoid flickering
if 'history' not in st.session_state:
    st.session_state['history'] = []

while True:
    try:
        # Poll the result endpoint
        resp = requests.get(f"{api_url_b}/result")
        if resp.status_code == 200:
            data = resp.json()
            if data:
                res = data['result']
                color = "#00FFAA" if res == 1 else "#FF4B4B"
                
                with placeholder.container():
                    st.markdown(f"""
                        <div style="background-color:#1E1E1E; padding:40px; border-radius:15px; border: 5px solid {color};">
                            <h3 style="text-align:center;">COLLAPSE DETECTED</h3>
                            <h1 style="text-align:center; color:{color}; font-size:120px;">{res}</h1>
                            <p style="text-align:center;">Sync Timestamp: {data['time']}</p>
                        </div>
                    """, unsafe_allow_html=True)
    except:
        placeholder.warning("Waiting for API to go online...")
    
    time.sleep(0.5)
