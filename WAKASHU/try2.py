from groq import Groq
import streamlit as st
import os
import time
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

# Get the API key from the environment
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("Error: GROQ_API_KEY environment variable is not set.")
    exit()

print(api_key)

# Initialize the Groq client
client = Groq(api_key=api_key)

# Make the API call with retries
max_retries = 3
for attempt in range(max_retries):
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What's in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://upload.wikimedia.org/wikipedia/commons/f/f2/LPU-v1-die.jpg"
                            }
                        }
                    ]
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        print(completion.choices[0].message)
        break  # Exit the loop if the request is successful
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt < max_retries - 1:
            time.sleep(2)  # Wait before retrying
        else:
            print("Error: Unable to communicate with the Groq API after multiple attempts.")
