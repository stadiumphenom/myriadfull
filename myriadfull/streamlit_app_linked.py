import streamlit as st
import json
import os
import glob
import matplotlib.pyplot as plt

from main import generate_dream_frame

st.title("🌀 Myriad Dreamframe Generator")
st.markdown("Craft nonlinear, emotion-simulated dreamframes in real time.")

# --- UI Controls ---
engine = st.selectbox("Select Engine", ["ego_loss", "echo", "drift", "form"])
sim_count = st.slider("Simulation Count", 50, 300, 100, 10)
drift = st.slider("Drift", 0.0, 2.0, 0.1, 0.1)

if st.button("🎇 Generate Dreamframe"):
    result = generate_dream_frame(engine, sim_count, drift)
    st.success(f"Frame Generated: {result['engine']} | {result['sim_count']} sims")

# --- Visualizer ---
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
        ax.bar(keys, values, color="orchid")
        ax.set_ylim(0, 1.2)
        ax.set_title("Frame Metric Preview")
        st.pyplot(fig)

# --- Rendered Dream Image ---
st.markdown("---")
st.header("🖼️ Dreamframe Image Preview")
if os.path.exists("renders/frame_preview.png"):
    st.image("renders/frame_preview.png", caption="Rendered Dreamframe", use_column_width=True)
else:
    st.info("Image preview not found. Run simulation to generate.")