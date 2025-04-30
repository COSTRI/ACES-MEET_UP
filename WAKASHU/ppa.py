import os
import base64
import imghdr
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from groq import Groq
from urllib.parse import urlparse

# Load environment variables
load_dotenv()
key = os.getenv("GROQ_API_KEY")

# Check API key
if not key:
    st.error("Missing GROQ_API_KEY in environment. Please set it in your .env file.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=key)

# --- Helper Functions ---

def get_image_mime_type(file_bytes):
    file_type = imghdr.what(None, file_bytes)
    return f"image/{file_type}" if file_type else "image/jpeg"

def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme in ("http", "https"), parsed.netloc])

def describe_image_from_base64(base64_image, mime_type):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What's in this image?"},
                        {"type": "image_url", "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"}},
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error analyzing image: {e}")
        return None

def describe_image_url(url):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What's in this image?"},
                        {"type": "image_url", "image_url": {"url": url}},
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error analyzing image URL: {e}")
        return None

# --- Streamlit UI ---

st.title("🖼️ Image Vision Tool")
st.subheader("Just Ask")
st.write("Choose to either upload an image or provide an image URL for analysis.")

tab1, tab2 = st.tabs(["📁 Upload Image", "🌐 Image URL"])

# --- Tab 1: Upload Image ---
with tab1:
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        try:
            file_bytes = uploaded_file.read()
            mime_type = get_image_mime_type(file_bytes)
            base64_image = base64.b64encode(file_bytes).decode("utf-8")

            uploaded_file.seek(0)
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            with st.spinner("Analyzing uploaded image..."):
                description = describe_image_from_base64(base64_image, mime_type)
                if description:
                    st.markdown("**Description:**")
                    st.write(description)
        except Exception as e:
            st.error(f"Error processing uploaded image: {e}")

# --- Tab 2: Image URL ---
with tab2:
    url = st.text_input("Enter an image URL")
    if url.strip():
        if is_valid_url(url.strip()):
            with st.spinner("Analyzing image from URL..."):
                description = describe_image_url(url.strip())
                if description:
                    st.markdown("**Description:**")
                    st.write(description)
        else:
            st.warning("Please enter a valid image URL.")
