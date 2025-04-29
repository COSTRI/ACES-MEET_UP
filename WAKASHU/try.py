from groq import Groq
import base64
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to encode the image
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None

# Path to your image
# Use a raw string (prefix with 'r') or double backslashes to avoid escape character issues
image_path = r"C:\Users\trish\OneDrive\Έγγραφα\ACES MEET_UP\sf.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

if base64_image:
    # Initialize the Groq client
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable is not set.")
    else:
        client = Groq(api_key=api_key)

        # Sending the request with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"What's in this image? [Image: data:image/jpeg;base64,{base64_image}]",
                        }
                    ],
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                )
                # Print the response
                print(chat_completion.choices[0].message.content)
                break  # Exit the loop if the request is successful
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # Wait before retrying
                else:
                    print("Error: Unable to communicate with the Groq API after multiple attempts.")