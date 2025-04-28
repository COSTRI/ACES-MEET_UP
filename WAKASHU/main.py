from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
key = os.getenv("GROQ_API_KEY")

# Initialize the client
client = Groq()

# Create a chat completion
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama-3.3-70b-versatile",
    temperature=0.5,
    max_completion_tokens=1024,
    top_p=1,
    stop=None,
    stream=False,
)

# Check if choices exist and print the completion
if chat_completion.choices:
    print(chat_completion.choices[0].message.content)
else:
    print("No choices returned.")