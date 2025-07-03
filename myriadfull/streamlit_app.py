import streamlit as st
from engines import engine_ego, engine_echo, engine_drift, engine_form
from frame_composer import compose_frame

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
    st.success("Dreamframe composed and saved.")

# --- Frame Preview Section ---
import os
import json
import glob
import matplotlib.pyplot as plt

st.markdown("---")
st.header("📊 Frame Visualizer")

render_files = sorted(glob.glob("renders/frame_*.json"), reverse=True)

if not render_files:
    st.warning("No rendered frames found. Run a simulation first.")
else:
    latest_file = render_files[0]
    st.success(f"Loaded: {latest_file}")

    with open(latest_file, "r") as f:
        data = json.load(f)

    st.subheader("🧠 Emotion Data Snapshot")
    st.json(data["data"][-1])

    st.subheader("🎨 Layer Info")
    st.write(f"Background: `{data['background']}`")
    st.write(f"Character: `{data['character']}`")
    st.write(f"FX: `{data['fx']}`")

    last_frame = data["data"][-1]
    if len(last_frame) >= 2:
        keys = list(last_frame.keys())[:3]
        values = [last_frame[k] for k in keys]

        fig, ax = plt.subplots()
        ax.bar(keys, values, color="mediumslateblue")
        ax.set_ylim(0, 1.2)
        ax.set_title("Frame Metric Preview")
        st.pyplot(fig)
    else:
        st.info("Not enough metrics for a plot.")
