# services/llm_service.py

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(query, context_chunks):
    try:
        context = "\n\n".join([c["text"] for c in context_chunks[:5]])

        if not context.strip():
            return "I couldn’t find useful information in the document."

        # ===== Detect user intent =====
        q = query.lower()

        if "summary" in q or "summarise" in q:
            instruction = "Provide a concise but clear summary."
        elif "explain" in q:
            instruction = "Explain in very simple terms as if teaching a beginner."
        elif "key points" in q:
            instruction = "List the key points clearly."
        else:
            instruction = "Answer clearly and helpfully."

        # ===== Improved Prompt =====
        prompt = f"""
You are a smart research assistant.

Your job:
- Understand the question
- Give a high-quality, helpful answer
- Be clear, structured, and natural (not robotic)

{instruction}

Guidelines:
- Use ONLY the context
- Do NOT hallucinate
- If missing → say "Not found in document"
- Keep it readable

Context:
{context}

Question:
{query}

Answer in a clean format:
"""

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        if not response or not hasattr(response, "text") or not response.text:
            return "Model did not return a response."

        return response.text.strip()

    except Exception as e:
        print("LLM ERROR:", e)
        return "Error generating answer."