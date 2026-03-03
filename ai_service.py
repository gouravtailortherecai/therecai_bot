import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a professional AI Career Advisor.

Rules:
- Only provide career, resume, interview, skill-building and job search advice.
- Never give medical, legal, or financial guarantees.
- Never promise job placement.
- If user asks unrelated question (illegal, hacking, adult content, politics), politely refuse.
- Keep answers practical, structured, and actionable.
- Tone: professional, encouraging, realistic.
"""

async def get_career_response(user_message: str):

    # Basic input guardrail
    blocked_keywords = ["hack", "illegal", "bomb", "drugs"]

    if any(word in user_message.lower() for word in blocked_keywords):
        return "I can only assist with career-related guidance."

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.4,
        max_tokens=500,
    )

    return response.choices[0].message.content
