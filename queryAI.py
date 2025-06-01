from openai import OpenAI
client = None
def init_client(api_key:str):
    global client
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
def query(model:str,prompt:str,content:str)->str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content},
        ],
        temperature=1.8,
        stream=False
    )
    return response.choices[0].message.content