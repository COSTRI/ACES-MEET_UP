import base64  # Import base64 for encoding and decoding image data
import imghdr  # Import imghdr for detecting the type of image files
from urllib.parse import urlparse  # Import urlparse for validating URLs

# Function to get the MIME type of an image file
def get_image_mime_type(file_bytes):
    """
    Detects the MIME type of an image file based on its binary content.

    Args:
        file_bytes: The binary content of the image file.

    Returns:
        A string representing the MIME type of the image (e.g., "image/jpeg").
        Defaults to "image/jpeg" if the type cannot be determined.
    """
    file_type = imghdr.what(None, file_bytes)  # Detect the file type (e.g., "jpeg", "png")
    return f"image/{file_type}" if file_type else "image/jpeg"  # Return the MIME type

# Function to validate a URL
def is_valid_url(url):
    """
    Validates whether a given URL is properly formatted and points to a valid resource.

    Args:
        url: The URL string to validate.

    Returns:
        True if the URL is valid, False otherwise.
    """
    parsed = urlparse(url)  # Parse the URL into components (scheme, netloc, etc.)
    return all([parsed.scheme in ("http", "https"), parsed.netloc])  # Check for valid scheme and netloc

# Function to describe an image from its Base64-encoded data
def describe_image_from_base64(client, base64_image, mime_type):
    """
    Sends a Base64-encoded image to the Groq API for analysis and retrieves a description.

    Args:
        client: The Groq API client instance used for making API requests.
        base64_image: The Base64-encoded string of the image data.
        mime_type: The MIME type of the image (e.g., "image/jpeg").

    Returns:
        A string containing the description of the image, or an error message if the request fails.
    """
    try:
        # Make a request to the Groq API with the Base64-encoded image
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",  # Specify the role as "user"
                    "content": [
                        {"type": "text", "text": "What's in this image?"},  # Text prompt for the API
                        {"type": "image_url", "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"}}  # Include the Base64 image data
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",  # Specify the model to use
            temperature=0.5,  # Set the temperature for response randomness
            max_completion_tokens=1024,  # Set the maximum number of tokens in the response
            top_p=1,  # Set the top-p sampling parameter
        )
        # Return the content of the first choice in the response
        return response.choices[0].message.content
    except Exception as e:
        # Return an error message if the request fails
        return f"Error: {e}"

# Function to describe an image from a URL
def describe_image_url(client, url):
    """
    Sends an image URL to the Groq API for analysis and retrieves a description.

    Args:
        client: The Groq API client instance used for making API requests.
        url: The URL of the image to analyze.

    Returns:
        A string containing the description of the image, or an error message if the request fails.
    """
    try:
        # Make a request to the Groq API with the image URL
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",  # Specify the role as "user"
                    "content": [
                        {"type": "text", "text": "What's in this image?"},  # Text prompt for the API
                        {"type": "image_url", "image_url": {"url": url}}  # Include the image URL
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",  # Specify the model to use
            temperature=0.5,  # Set the temperature for response randomness
            max_completion_tokens=1024,  # Set the maximum number of tokens in the response
            top_p=1,  # Set the top-p sampling parameter
        )
        # Return the content of the first choice in the response
        return response.choices[0].message.content
    except Exception as e:
        # Return an error message if the request fails
        return f"Error: {e}"
