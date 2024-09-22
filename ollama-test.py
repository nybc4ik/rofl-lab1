import requests
import json
# ollama run llama3.1:8b
def generate_response(prompt, model="llama3.1:8b"):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": model,
        "prompt": prompt
    }

    response = requests.post(url, json=data, stream=True)

    full_response = ""
    for line in response.iter_lines():
        if line:
            json_response = json.loads(line)
            if 'response' in json_response:
                full_response += json_response['response']
            if json_response.get('done', False):
                break

    return full_response

prompt = "расскажи анекдот"
result = generate_response(prompt)
print(result)