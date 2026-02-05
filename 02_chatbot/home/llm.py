from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key= settings.OPENAI_API_KEY,
)
system_prompt = """
You are helpful ai assistant your role is to give short and consise respose.
NOTE: avoid using foul words and special character like [*, #].
"""
def llm(user_query):
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {   "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    return response.choices[0].message.content

