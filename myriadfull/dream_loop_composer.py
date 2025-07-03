import os
import glob
import json
from moviepy.editor import ImageSequenceClip
from frame_renderer import render_frame_as_image
from cam_motion_engine import generate_camera_motion

def compose_motion_loop(output_path="renders/dreamloop_motion.mp4", fps=3):
    frame_files = sorted(glob.glob("renders/frame_*.json"))
    if not frame_files:
        print("[Composer] No frames found.")
        return

    os.makedirs("renders/frames_motion", exist_ok=True)
    images = []
    for i, fpath in enumerate(frame_files):
        with open(fpath, "r") as f:
            data = json.load(f)
        motion = generate_camera_motion(i, len(frame_files))
        img_path = f"renders/frames_motion/frame_{i:03d}.png"
        render_frame_as_image(data, img_path, cam_motion=motion)
        images.append(img_path)

    clip = ImageSequenceClip(images, fps=fps)
    clip.write_videofile(output_path, codec="libx264", audio=False)
    print(f"[Composer] Motion Dreamloop saved to {output_path}")