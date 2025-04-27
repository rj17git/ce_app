import streamlit as st
import cv2
import numpy as np
from pathlib import Path

@st.cache_data(show_spinner=False)
def load_image_from_path(filepath):
    if not filepath.exists():
        st.error(f"Image doesn't exist : {filepath}")
        return None
    image = cv2.imread(str(filepath))
    return image

@st.cache_data(show_spinner=False)
def load_image_from_upload(uploaded_file):
    if uploaded_file is None:
        st.error("No uploaded file !")
        return None
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return image


def get_image(source:str):
    image, image_name = None, ""
    if source == "From directory":
        image_files = list(Path("./images").glob("*.png"))
        selected_image = st.selectbox("Choose an image", image_files)
        if selected_image:
            image = load_image_from_path(selected_image)
            image_name = selected_image.name
    else:
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            image = load_image_from_upload(uploaded_image)
            image_name = uploaded_image.name
    
    return image, image_name