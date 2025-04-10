import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("./.env")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

completion = client.chat.completions.create(
    extra_body={},
    model="deepseek/deepseek-r1:free",
    messages=[{"role": "user", "content": "O que seria uma IA?"}],
)
print(completion.choices[0].message.content)
