import os
from openai import OpenAI


def gpt_completion(prompt: str, model="gpt-3-turbo-0125") -> str:
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=[
            prompt
        ],
        model=model,
    )

    return chat_completion.choices[0].message.content