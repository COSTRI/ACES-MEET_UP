import streamlit as st  # Import Streamlit for building the web app
from PIL import Image  # Import Pillow for image processing
import base64  # Import base64 for encoding image data

from helper import get_image_mime_type, describe_image_from_base64  # Import helper functions for MIME type detection and image description

# Define a function for the "Upload Image" tab
def upload_tab(client):
    """
    This function creates a Streamlit tab for uploading and analyzing images.
    It allows the user to upload an image file, encodes it to Base64, and sends it
    to the Groq API for analysis.

    Args:
        client: The Groq API client instance used for making API requests.
    """
    # Display a header for the tab
    st.header("📁 Upload Image")

    # File uploader for the user to upload an image
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    # Check if the user has uploaded a file
    if uploaded_file:
        try:
            # Read the uploaded file as bytes
            file_bytes = uploaded_file.read()

            # Get the MIME type of the uploaded file (e.g., image/jpeg)
            mime_type = get_image_mime_type(file_bytes)

            # Encode the file bytes to a Base64 string
            base64_image = base64.b64encode(file_bytes).decode("utf-8")

            # Reset the file pointer to the beginning of the file
            uploaded_file.seek(0)

            # Open the uploaded file as an image using Pillow
            image = Image.open(uploaded_file)

            # Display the uploaded image in the Streamlit app
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Display a spinner while the image is being analyzed
            with st.spinner("Analyzing uploaded image..."):
                # Call the `describe_image_from_base64` function to analyze the image
                description = describe_image_from_base64(client, base64_image, mime_type)

                # If a description is returned, display it
                if description:
                    st.markdown("**Description:**")  # Display a bold "Description" label
                    st.write(description)  # Write the description to the Streamlit app
        except Exception as e:
            # If an error occurs, display an error message
            st.error(f"Error processing uploaded image: {e}")
