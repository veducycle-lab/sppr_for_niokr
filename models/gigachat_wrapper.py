import requests
import urllib3

class GigaChatWrapper:
    """
    Обёртка для GigaChat API, подходит для мультиагентных промптов.
    """
    def __init__(self, access_token: str, model: str = "GigaChat:latest"):
        urllib3.disable_warnings()
        self.access_token = access_token
        self.model = model
        self.url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    def call(
        self, 
        prompt, 
        system_prompt="Ты полезный интеллектуальный ассистент для анализа текста и данных.",
        max_tokens=1024, 
        temperature=0.7, 
        dialog_history=None
    ):
        messages = []
        messages.append({"role": "system", "content": system_prompt})
        if dialog_history:
            for m in dialog_history:
                messages.append(m)
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "top_p": 0.9,
            "n": 1,
            "stream": False,
            "max_tokens": max_tokens
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.post(self.url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        result = response.json()
        # Для stream:False ответ будет тут:
        # result['choices'][0]['message']['content']
        return result['choices'][0]['message']['content']