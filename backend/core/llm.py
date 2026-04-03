from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(context, query):
    prompt = f"""
You are a senior software engineer analyzing a codebase.

STRICT RULES:
- Use ONLY the given context
- Do NOT hallucinate
- If missing info → say "Not found in context"

----------------------------------------
CONTEXT:
{context}
----------------------------------------

QUESTION:
{query}

----------------------------------------
FORMAT YOUR ANSWER EXACTLY LIKE THIS:

## 🧠 Overview
Explain what the feature/system does in simple terms.

## ⚙️ Key Components
List important functions/classes:
- Name (File: path)
  → What it does

## 🔄 How It Works (Step-by-step)
1. Step one
2. Step two
3. Step three

## 📌 Important Notes
- Edge cases / missing parts
- Observations

----------------------------------------

Make the answer CLEAR, MULTI-LINE, and WELL STRUCTURED.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content