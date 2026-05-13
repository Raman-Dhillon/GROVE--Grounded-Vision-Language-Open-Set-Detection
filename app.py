import streamlit as st
from PIL import Image
from model import detect_objects

st.set_page_config(page_title="Grounding DINO App", layout="wide")

st.title("🎯 GROVE: Grounded Vision–Language Open-Set Detection")
st.write("Upload an image and enter object name(s) like: dog, person")

uploaded_file = st.file_uploader("📷 Upload Image", type=["jpg", "jpeg", "png"])
prompt = st.text_input("🔍 Enter object(s) to detect", placeholder="dog")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Input Image", width=700)

    if st.button("🚀 Detect Objects"):
        if not prompt.strip():
            st.warning("Please enter object name(s)")
        else:
            with st.spinner("Detecting objects..."):
                result_image = detect_objects(image.copy(), prompt.strip())
            st.image(result_image, caption="Detected Output", width=700)