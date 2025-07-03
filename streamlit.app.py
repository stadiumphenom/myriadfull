# streamlit_app.py
import os
import streamlit as st
from PIL import Image
import json

# --- Real Engine Imports ---
from engines import engine_ego, engine_echo, engine_drift, engine_form
from frame_renderer import render_frame_as_image

ENGINE_MAP = {
    "ego-loss": engine_ego.MyriadEgoEngine,
    "echo": engine_echo.MyriadEchoEngine,
    "chaos": engine_drift.MyriadDriftEngine,
    "structured": engine_form.MyriadFormEngine
}

# --- Streamlit UI ---
st.set_page_config(page_title="Myriad Dream Engine", layout="centered")
st.title("🌌 Myriad Dream Engine")
st.markdown("Simulate emotional dreamframes using Myriad's layered engine system.")

prompt = st.text_input("Dream Prompt", "Enter memory fragment, dream theme, or phrase")
emotion = st.selectbox("Emotion Key", list(ENGINE_MAP.keys()), index=0)
sim_count = st.slider("Simulation Cycles", min_value=1000, max_value=50000, value=10000, step=1000)
drift = st.slider("Drift Factor", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

if st.button("Run Dream Simulation"):
    st.info(f"🌀 Simulating `{emotion}` with {sim_count} cycles and drift {drift}...")
    EngineClass = ENGINE_MAP[emotion]
    engine = EngineClass(emotion=emotion, sim_count=sim_count, drift_factor=drift)
    engine.prompt = prompt
    output = engine.generate_frame_data()

    os.makedirs("renders", exist_ok=True)
    with open("renders/frame_output.json", "w") as f:
        json.dump(output, f)

    render_frame_as_image(output, "renders/frame_preview.png")
    st.success("Dreamframe composed and saved.")

st.markdown("---")
st.subheader("🖼️ Dreamframe Preview")
if os.path.exists("renders/frame_preview.png"):
    st.image("renders/frame_preview.png", caption=f"🌀 {emotion.title()} — Prompt: {prompt}", use_column_width=True)
else:
    st.info("No preview image found. Generate a frame to view.")

with st.expander("🔍 Debug Info"):
    if os.path.exists("renders/frame_output.json"):
        with open("renders/frame_output.json", "r") as f:
            debug_data = json.load(f)
        st.json(debug_data)
    else:
        st.write("No output yet. Run simulation first.")
