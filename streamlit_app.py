import os
import streamlit as st

from engines import engine_ego, engine_echo, engine_drift, engine_form
from frame_composer import compose_frame
from frame_renderer import render_frame_as_image  # ✅ Add this

ENGINE_MAP = {
    "ego-loss": engine_ego.MyriadEgoEngine,
    "echo": engine_echo.MyriadEchoEngine,
    "chaos": engine_drift.MyriadDriftEngine,
    "structured": engine_form.MyriadFormEngine
}

st.title("Myriad Dream Engine")
st.markdown("Simulate emotional dreamframes using Myriad's layered engine system.")

emotion = st.selectbox("Emotion Key", list(ENGINE_MAP.keys()))
sim_count = st.slider("Simulation Cycles", min_value=1000, max_value=50000, value=10000, step=1000)
drift = st.slider("Drift Factor", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

if st.button("Run Dream Simulation"):
    st.write(f"Simulating `{emotion}` with {sim_count} cycles and drift {drift}")
    EngineClass = ENGINE_MAP.get(emotion, engine_ego.MyriadEgoEngine)
    engine = EngineClass(emotion=emotion, sim_count=sim_count, drift_factor=drift)
    output = engine.generate_frame_data()

    compose_frame(output, emotion)

    # ✅ Renders PNG for streamlit preview
    render_frame_as_image(output, "renders/frame_preview.png")

    st.success("Dreamframe composed and preview image saved.")

# --- 🖼️ Rendered Image Preview ---
if os.path.exists("renders/frame_preview.png"):
    st.image("renders/frame_preview.png", caption="🌀 Dreamframe Preview", use_column_width=True)
else:
    st.info("No preview image found. Generate a frame to see it here.")

