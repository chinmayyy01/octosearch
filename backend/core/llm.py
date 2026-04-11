from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"


def generate_answer(context, query):
    prompt = f"""
You are a senior software engineer analyzing a codebase.

Use ONLY the given context to answer.
Do NOT hallucinate.
If something is missing, say "Not found in context".

-----------------------------
CONTEXT:
{context}
-----------------------------

QUESTION:
{query}

-----------------------------
FORMAT YOUR ANSWER LIKE THIS:

## Overview
Explain what it is in simple terms.

## Key Components
- Name (file path)
  Explanation

## How It Works
1. Step 1
2. Step 2
3. Step 3

## Notes
Important observations

Keep it clear, structured, and readable.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=800
    )

    return response.choices[0].message.content