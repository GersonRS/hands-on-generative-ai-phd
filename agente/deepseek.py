from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

completion = client.chat.completions.create(
    extra_body={},
    model="deepseek/deepseek-v3-base:free",
    messages=[{"role": "user", "content": "O que seria uma IA?"}],
)
print(completion.choices[0].message.content)
