import requests

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}
payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0
}
response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.text)