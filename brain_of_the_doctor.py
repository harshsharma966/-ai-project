import os
import base64
from dotenv import load_dotenv
from groq import Groq

# Step 1: Load environment variables
load_dotenv()

# Access the API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Ensure API key is present
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Please set it in the .env file.")

# Step 2: Convert image to base64 format
def encode_image(image_path):   
    with open(image_path, "rb") as image_file:  # Open image safely
        return base64.b64encode(image_file.read()).decode('utf-8')

# Step 3: Setup Multimodal LLM
query = "Is there something wrong with my face?"
model = "meta-llama/llama-4-scout-17b-16e-instruct"
image_path = "acne.jpg"  

def analyze_image_with_query(query, model, encoded_image):
    client = Groq(api_key=GROQ_API_KEY)  

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
            ],
        }
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content  

# Encode image before using it
encoded_image = encode_image(image_path)

# Call function and print response
response = analyze_image_with_query(query, model, encoded_image)
print("Model Response:", response)  
