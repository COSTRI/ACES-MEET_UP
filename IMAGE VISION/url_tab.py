import streamlit as st  # Import Streamlit for building the web app
from helper import is_valid_url, describe_image_url  # Import helper functions for URL validation and image description

# Define a function for the "Image URL" tab
def url_tab(client):
    """
    This function creates a Streamlit tab for analyzing images from a URL.
    It allows the user to input an image URL, validates the URL, and sends it
    to the Groq API for analysis.

    Args:
        client: The Groq API client instance used for making API requests.
    """
    # Display a header for the tab
    st.header("🌐 Image URL")

    # Input field for the user to enter an image URL
    url = st.text_input("Enter an image URL")

    # Check if the user has entered a non-empty URL
    if url.strip():
        # Validate the URL using the `is_valid_url` helper function
        if is_valid_url(url.strip()):
            # If the URL is valid, display a spinner while processing
            with st.spinner("Analyzing image from URL..."):
                # Call the `describe_image_url` function to analyze the image
                description = describe_image_url(client, url.strip())

                # If a description is returned, display it
                if description:
                    st.markdown("**Description:**")  # Display a bold "Description" label
                    st.write(description)  # Write the description to the Streamlit app
        else:
            # If the URL is invalid, display a warning message
            st.warning("Please enter a valid image URL.")
