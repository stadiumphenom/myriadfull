from PIL import Image, ImageDraw

def render_frame_as_image(data, save_path):
    img = Image.new("RGB", (512, 512), (20, 20, 30))
    draw = ImageDraw.Draw(img)
    center = (256, 256)

    for i, (k, v) in enumerate(data["data"][-1].items()):
        radius = int(50 + v * 200)
        offset = i * 60
        color = (int(200 - v*100), int(v*255), 255)
        draw.ellipse(
            [center[0] - radius + offset, center[1] - radius + offset,
             center[0] + radius - offset, center[1] + radius - offset],
            outline=color, width=4
        )

    img.save(save_path)