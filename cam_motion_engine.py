import math
import random

def generate_camera_motion(frame_index, total_frames):
    t = frame_index / total_frames
    return {
        "x": math.sin(t * math.pi * 2) * 20,
        "y": math.cos(t * math.pi * 2) * 20,
        "z": 1 + 0.2 * math.sin(t * math.pi),
        "zoom": 1.0 + 0.15 * math.sin(t * 2 * math.pi),
        "rotation": (t * 360) % 360
    }