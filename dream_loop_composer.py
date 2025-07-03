import os
import glob
import json
from moviepy.editor import ImageSequenceClip, AudioFileClip
from frame_renderer import render_frame_as_image
from cam_motion_engine import generate_camera_motion
from audio_reactive_engine import extract_audio_pulse

def compose_audio_loop(audio_path, output_path="renders/dreamloop_audio.mp4", fps=3):
    frame_files = sorted(glob.glob("renders/frame_*.json"))
    if not frame_files:
        print("[Composer] No frames found.")
        return

    envelope = extract_audio_pulse(audio_path, len(frame_files))

    os.makedirs("renders/frames_audio", exist_ok=True)
    images = []
    for i, fpath in enumerate(frame_files):
        with open(fpath, "r") as f:
            data = json.load(f)
        motion = generate_camera_motion(i, len(frame_files))

        pulse = envelope[i]
        motion["zoom"] *= 1 + 0.2 * pulse
        motion["rotation"] += pulse * 20

        img_path = f"renders/frames_audio/frame_{i:03d}.png"
        render_frame_as_image(data, img_path, cam_motion=motion)
        images.append(img_path)

    clip = ImageSequenceClip(images, fps=fps)
    clip = clip.set_audio(AudioFileClip(audio_path))
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"[Composer] Audio Dreamloop saved to {output_path}")