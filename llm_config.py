# llm_config.py
import json
import os
from openai import OpenAI


# Get the API key from the environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Check if the API key is set
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_llm_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.01
        )
        content = response.choices[0].message.content.strip()
        #print(f"LLM Response: {content}")  # For debugging
        return content
    except Exception as e:
        print(f"Error generating LLM response: {str(e)}")
        return None
