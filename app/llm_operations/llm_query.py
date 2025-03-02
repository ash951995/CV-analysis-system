

import requests
import os
import json
from app.models import Resume


# Set up the Together AI API
API_KEY = os.getenv('API_KEY',"38302e34fb50f335c6af24c728a126c76df4ca2afd3bc3fbfe62770988d8c38b")
TOGETHER_API_URL = os.getenv('TOGETHER_API_URL',"https://api.together.xyz/v1/completions")

def query_cv_data(query_text):
    cvs = Resume.query.all()
    all_cv_data = [{"filename": resume.filename, "data": resume.text_content} for resume in cvs]

    prompt = f"""
    Given the following CV data (in JSON format), answer the user's query:

    User Query: {query_text}

    CV Data:
    {json.dumps(all_cv_data)}

    Provide a concise and relevant response.
    """

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/Mistral-7B-Instruct-v0.1",
             "messages": [
            {"role": "system", "content": "You are an AI trained to extract structured resume data."},
            {"role": "user", "content": prompt}  # Explicitly sending the prompt
        ],
            "max_tokens": 1000
        }

        response = requests.post(TOGETHER_API_URL, headers=headers, json=data)
        print("Raw API Response:", response.text)  # Debugging

        print(f"response  data is ->{response}")

        data = response.json()
        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}: {response.text}"}

        # Parse JSON response
        data = response.json()
        print("Parsed JSON Response:", data)  # Debugging

        if "choices" not in data or not data["choices"]:
            return {"error": "Invalid response format", "raw_output": data}

        # Extract the model's generated response (it's inside "text" field)
        result_text = data["choices"][0].get("text", "").strip()
        print("Extracted Result:", result_text,type(result_text))  # Debugging        

        return result_text


    except Exception as e:
        print(f"Error querying CV data with OpenAI: {e}")
        return "Sorry, I couldn't process your query."

    
