import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import os

# Stability AI API Key from environment variable
API_KEY = os.getenv("sk-Vd5S5SG1mZVlyJjySkhVW5ZcbarHfKEAtITgj5gQszKQO5aG")
API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

st.set_page_config(page_title="Dreamloop Lite", layout="centered")
st.title("🎨 Dreamloop Lite - Powered by Stability AI")

if not API_KEY:
    st.error("API key not found. Please set the STABILITY_API_KEY environment variable.")
else:
    prompt = st.text_input("Enter a prompt:", "a futuristic cityscape at sunset")
    uploaded_file = st.file_uploader("(Optional) Upload an image to guide the generation", type=["jpg", "jpeg", "png"])

    if st.button("Generate"):
        if not prompt:
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating image..."):
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }

                payload = {
                    "prompt": prompt,
                    "output_format": "png"
                }

                if uploaded_file:
                    image_bytes = uploaded_file.read()
                    b64_image = base64.b64encode(image_bytes).decode("utf-8")
                    payload["init_image"] = b64_image
                    payload["mode"] = "image-to-image"

                response = requests.post(API_URL, headers=headers, json=payload)

                if response.status_code == 200:
                    output = response.json()
                    image_data = base64.b64decode(output["image"])
                    result_img = Image.open(BytesIO(image_data))
                    st.image(result_img, caption="Generated Image")
                    st.download_button("Download Image", data=image_data, file_name="dreamloop_output.png")
                else:
                    st.error(f"Generation failed: {response.text}")
