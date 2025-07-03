from PIL import Image, ImageDraw

def render_frame_as_image(data, save_path, cam_motion=None):
    img = Image.new("RGB", (512, 512), (10, 10, 20))
    draw = ImageDraw.Draw(img)
    center = (256 + int(cam_motion.get("x", 0)), 256 + int(cam_motion.get("y", 0)))

    for i, (k, v) in enumerate(data["data"][-1].items()):
        radius = int(30 + v * 150)
        offset = i * 40
        color = (int(200 - v * 100), int(v * 255), 255)
        draw.ellipse(
            [center[0] - radius + offset, center[1] - radius + offset,
             center[0] + radius - offset, center[1] + radius - offset],
            outline=color, width=3
        )

    img = img.rotate(cam_motion.get("rotation", 0))
    zoom = cam_motion.get("zoom", 1.0)
    if zoom != 1.0:
        w, h = img.size
        img = img.resize((int(w * zoom), int(h * zoom)))
        img = img.crop(((img.width - 512) // 2, (img.height - 512) // 2,
                        (img.width + 512) // 2, (img.height + 512) // 2))

    img.save(save_path)