import os
import json
import random

def compose_frame(sim_data, emotion, output_dir="renders"):
    frame = {
        "background": f"bg_{emotion}_{random.randint(1000,9999)}",
        "character": f"char_{emotion}_{random.randint(1000,9999)}",
        "fx": f"fx_{emotion}_{random.randint(1000,9999)}",
        "data": sim_data
    }
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/frame_{emotion}_{random.randint(1000,9999)}.json", "w") as f:
        json.dump(frame, f, indent=2)
    print(f"[Composer] Frame composed and saved for emotion '{emotion}'.")