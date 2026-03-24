from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(context, query):
    prompt = f"""
    You are a code assistant.
    
    Use ONLY the provided code context to answer.
    
    Context:
    {context}
    
    Question:
    {query}
    
    Rules:
    - Be precise and concise.
    - Mention file names if relevant.
    - If answer not found, say "Not found in codebase".
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content