from groq import Groq
import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from io import BytesIO
import requests
import cv2
import numpy as np

# Load environment variables
load_dotenv()
key = os.getenv("GROQ_API_KEY")

if not key:
    st.error("GROQ_API_KEY is not set. Please check your .env file.")
    st.stop()

# Initialize the client
client = Groq(api_key=key)

# Function to analyze the image using OpenCV
def analyze_image_with_opencv(image):
    try:
        # Convert the PIL image to a NumPy array (compatible with OpenCV)
        image_np = np.array(image)

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

        # Perform edge detection
        edges = cv2.Canny(gray_image, 100, 200)

        # Convert edges to RGB for Streamlit display
        edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

        # Calculate basic properties
        height, width = gray_image.shape
        analysis_result = f"Image Dimensions: {width}x{height} pixels"

        return edges_rgb, analysis_result
    except Exception as e:
        return None, f"Error analyzing image with OpenCV: {e}"

# Function to describe the image using the Groq API
def describe_image(image):
    try:
        # Convert the image to RGB mode if it's in RGBA or other modes
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Convert the image to Base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        image_base64 = buffered.getvalue().decode("latin1")

        # Call the Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an image analysis assistant."
                },
                {
                    "role": "user",
                    "content": f"Analyze this image: [Base64 Image: {image_base64}]"
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error analyzing image: {e}")
        return None

# Set up the Streamlit app
st.title("Image Vision Tool")
st.subheader("Just Ask")
st.write("Upload an image or enter a URL to get a description.")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# URL input
url = st.text_input("Or enter an image URL")

if uploaded_file is not None:
    # If an image is uploaded
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Analyze the image with OpenCV
        edges, analysis_result = analyze_image_with_opencv(image)
        if edges is not None:
            st.write(analysis_result)
            st.image(edges, caption='Edge Detection', use_column_width=True, clamp=True)

        # Describe the image using the Groq API
        description = describe_image(image)
        if description:
            st.write(description)
    except Exception as e:
        st.error(f"Error processing uploaded image: {e}")

elif url:
    # If a URL is provided
    try:
        # Validate the URL
        if not url.strip():
            st.error("Please enter a valid image URL.")
            st.stop()

        # Fetch the image from the URL
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            try:
                # Open the image from the URL
                image = Image.open(BytesIO(response.content))
                st.image(image, caption='Image from URL', use_column_width=True)

                # Describe the image using the Groq API
                description = describe_image(image)
                if description:
                    st.write(description)
            except Exception as e:
                st.error(f"Error processing the image: {e}")
        else:
            st.error("Failed to fetch the image. Please check the URL and try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the image from the URL: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

else:
    st.write("Please upload an image or enter a URL.")






