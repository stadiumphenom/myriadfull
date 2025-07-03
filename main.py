import os
import json
import numpy as np
from frame_renderer import render_frame_as_image

ENGINES = {
    "ego_loss": lambda i, t: np.sin(t + i) * 0.5 + 0.5,
    "echo": lambda i, t: np.cos(t + i) ** 2,
    "drift": lambda i, t: np.sin(t * 0.1 + i * 0.2) * np.cos(t * 0.1) * 0.5 + 0.5,
    "form": lambda i, t: np.clip(np.sin(i * 0.3 + t) * 0.7 + 0.3, 0, 1)
}

def generate_dream_frame(engine_name, sim_count, drift=0.0):
    sim = ENGINES.get(engine_name, ENGINES["ego_loss"])
    data = []
    for i in range(sim_count):
        t = i * 0.1
        sample = {
            "pulse": sim(i + 1, t + drift),
            "echo": sim(i + 3, t + drift * 0.5),
            "field": sim(i + 7, t + drift * 1.5)
        }
        data.append(sample)

    frame = {
        "engine": engine_name,
        "sim_count": sim_count,
        "drift": drift,
        "background": f"{engine_name}_field",
        "character": f"{engine_name}_avatar",
        "fx": f"{engine_name}_fxpack",
        "data": data
    }

    os.makedirs("renders", exist_ok=True)
    frame_path = f"renders/frame_{len(os.listdir('renders')):03d}.json"
    with open(frame_path, "w") as f:
        json.dump(frame, f, indent=2)

    # Also render image preview
    render_frame_as_image(frame, save_path="renders/frame_preview.png")
    print(f"[Myriad] Frame saved to {frame_path} and preview image updated.")
    return frame