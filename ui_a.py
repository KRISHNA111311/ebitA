import streamlit as st
import requests
import time

st.set_page_config(page_title="Node A - Controller", layout="wide")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("🔗 Connection Settings")
api_url_a = st.sidebar.text_input("Laptop A API Link", "http://127.0.0.1:8000")
target_url_b = st.sidebar.text_input("Laptop B API Link", "http://127.0.0.1:8001")

st.title("⚛️ Quantum Node A (Initiator)")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Measurement Controls")
    angle = st.slider("Select Basis Angle (θ)", 0.0, 3.14, 0.0, help="Simulates rotating the polarizer")
    
    if st.button("Collapse Entanglement", use_container_width=True):
        try:
            # We call the local API which then talks to Laptop B
            response = requests.get(f"{api_url_a}/measure?angle={angle}")
            if response.status_code == 200:
                data = response.json()
                st.session_state['last_result'] = data['result']
                st.session_state['sync_time'] = data['time']
            else:
                st.error("API returned an error.")
        except Exception as e:
            st.error(f"Connection Failed: {e}")

with col2:
    st.subheader("Local Measurement Result")
    if 'last_result' in st.session_state:
        res = st.session_state['last_result']
        color = "#00FFAA" if res == 1 else "#FF4B4B"
        st.markdown(f"""
            <div style="background-color:#1E1E1E; padding:20px; border-radius:10px; border: 2px solid {color};">
                <h1 style="text-align:center; color:{color}; font-size:100px;">{res}</h1>
                <p style="text-align:center;">Collapsed at: {st.session_state['sync_time']}</p>
            </div>
        """, unsafe_allow_html=True)
