
import os
import streamlit as st
from mock_engine import MockEngine
from render_frame import render_frame_as_image
from composer import compose_audio_loop
import json

ENGINE_MAP = {
    "ego-loss": MockEngine,
    "echo": MockEngine,
    "chaos": MockEngine,
    "structured": MockEngine
}

st.set_page_config(page_title="Myriad Dream Engine", layout="centered")
st.title("🌌 Myriad Dream Engine")
st.markdown("Create immersive dreamframes using Myriad's layered simulation system.")

prompt = st.text_input("Dream Prompt", "Enter memory fragment, dream theme, or phrase")
emotion = st.selectbox("Emotion Key", list(ENGINE_MAP.keys()), index=0)
sim_count = st.slider("Simulation Cycles", min_value=1000, max_value=50000, value=10000, step=1000)
drift = st.slider("Drift Factor", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
audio_file = st.file_uploader("Upload Audio for Dreamloop", type=["mp3", "wav"])

if st.button("Run Dream Simulation"):
    st.info(f"🌀 Simulating `{emotion}` with {sim_count} cycles and drift {drift}...")
    EngineClass = ENGINE_MAP[emotion]
    engine = EngineClass(emotion=emotion, sim_count=sim_count, drift_factor=drift)
    engine.prompt = prompt
    frames = engine.generate_multiple_frames(num_frames=10)

    os.makedirs("renders/frames_audio", exist_ok=True)
    for i, data in enumerate(frames):
        img_path = f"renders/frames_audio/frame_{i:03d}.png"
        render_frame_as_image(data, img_path)
    with open("renders/frame_output.json", "w") as f:
        json.dump(frames[-1], f)
    st.success("All dreamframes generated.")

    if audio_file:
        audio_path = f"uploads/{audio_file.name}"
        os.makedirs("uploads", exist_ok=True)
        with open(audio_path, "wb") as f:
            f.write(audio_file.read())
        compose_audio_loop(audio_path)
        st.video("renders/dreamloop_audio.mp4")

st.markdown("---")
if os.path.exists("renders/frames_audio/frame_000.png"):
    st.image("renders/frames_audio/frame_000.png", caption=f"🌀 {emotion.title()} — Prompt: {prompt}", use_column_width=True)
