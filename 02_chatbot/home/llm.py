from openai import OpenAI
from django.conf import settings
from .models import ChatMessage

client = OpenAI(
    api_key= settings.OPENAI_API_KEY,
)
system_prompt = """
You are helpful ai assistant your role is to give short and consise respose.
NOTE: avoid using foul words and special character like [*, #].
"""
def llm(user_query, chat = None):
    if chat:
        last_messages = ChatMessage.objects.filter(chat = chat).order_by('-created_at')[:5][::-1]

        messages = [
            {'role': 'system', 'content': system_prompt}
        ]

        for message in last_messages:
            messages.append({
                'role': message.role,
                'content': message.content
            })
        
        messages.append({
            'role': 'user', 'content': user_query
        })
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages= messages
        )

        ai_reply =  response.choices[0].message.content

        ChatMessage.objects.create(
            chat=chat,
            role="assistant",
            content=ai_reply
        )

        return ai_reply

    else:
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