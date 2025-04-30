import os  # Import os for accessing environment variables
from dotenv import load_dotenv  # Import dotenv for loading environment variables from a .env file
import streamlit as st  # Import Streamlit for building the web app
from groq import Groq  # Import Groq for interacting with the Groq API

from upload_tab import upload_tab  # Import the upload_tab function for handling image uploads
from url_tab import url_tab  # Import the url_tab function for handling image URLs

# Load API key from the .env file
load_dotenv()  # Load environment variables from a .env file
key = os.getenv("GROQ_API_KEY")  # Retrieve the GROQ_API_KEY from the environment

# Check if the API key is available
if not key:
    # Display an error message if the API key is missing
    st.error("Missing GROQ_API_KEY in environment. Please set it in your .env file.")
    st.stop()  # Stop the execution of the app if the API key is not found

# Initialize the Groq client with the API key
client = Groq(api_key=key)

# UI Setup
st.title("🖼️ Image Vision Tool")  # Display the title of the app with an emoji
st.write("Choose to either upload an image or provide a URL for analysis.")  # Display a brief description of the app

# Create tabs for the two functionalities: "Upload" and "URL"
tab1, tab2 = st.tabs(["Upload", "URL"])

# Tab 1: Upload Image
with tab1:
    upload_tab(client)  # Call the upload_tab function to handle image uploads

# Tab 2: Image URL
with tab2:
    url_tab(client)  # Call the url_tab function to handle image URLs
