from groq import Groq
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()
key = os.getenv("GROQ_API_KEY")

# Initialize the client
client = Groq(api_key=key)

# Set up the Streamlit app
st.title("Question Tool")
st.subheader("Just Ask ")
#st.write("Upload an image or enter a URL to get a description.")

question = st.chat_input("Enter your question here:")


# Create a chat completion
def request_answer(question):   
    chat_completion = client.chat.completions.create(
     messages=[
            {
              "role": "system",
             "content": "you are a smart student."
          },
         {
               "role": "user",
             "content": question,
            }
     ],
        model="llama-3.3-70b-versatile",
     temperature=0.5,
     max_completion_tokens=1024,
        top_p=1,
         stop=None,
             stream=False,

    )
    return chat_completion.choices[0].message.content

if question:
    with st.chat_message("user"):
        st.write(question)
    with st.spinner("Thinking..."):
        with st.chat_message("assistant"):
            # Simulate a delay for the response (optional)
            # time.sleep(2)

            # Get the answer from the Groq API
            output = request_answer(question)
            st.write(output)