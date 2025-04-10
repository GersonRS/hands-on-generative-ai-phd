from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="xxx",  # required, but unused
)

response = client.chat.completions.create(
    model="deepseek-r1:7b",
    messages=[
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Quem ganhou a World Series em 2020?"},
        {"role": "assistant", "content": "O LA Dodgers venceu em 2020."},
        {"role": "user", "content": "Onde foram os jogos?"},
    ],
    stream=True,
)
# Print the streaming response as it arrives
for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()  # just add a newline at the end
