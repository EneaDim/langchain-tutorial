from openai import OpenAI

def run_openai(prompt: str, model: str, api_key: str, base_url: str | None = None) -> str:
    client = OpenAI(api_key=api_key, base_url=base_url or None)
    resp = client.chat.completions.create(model=model, messages=[{"role":"user","content":prompt}], temperature=0.1)
    return resp.choices[0].message.content
