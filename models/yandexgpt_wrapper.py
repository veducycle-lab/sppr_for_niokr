import requests

class YandexGPTWrapper:
    """
    Обёртка для YandexGPT. Использует REST API Яндекс Облака.
    Пример использования в мультиагентной архитектуре.
    """
    def __init__(self, api_key: str, model_uri: str = "gpt://b1gnpj1mopesukngnar1/yandexgpt-lite"):
        self.api_key = api_key
        self.model_uri = model_uri
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    def call(
        self, 
        prompt, 
        system_prompt="Ты полезный интеллектуальный ассистент для анализа текста и данных.",
        max_tokens=2000, 
        temperature=0.7, 
        dialog_history=None
    ):
        # Формируем список сообщений в стиле openai:
        messages = []
        messages.append({"role": "system", "text": system_prompt})
        # Добавляем историю (если передана)
        if dialog_history:
            for message in dialog_history:
                messages.append(message)
        # Затем добавляем последний вопрос пользователя
        messages.append({"role": "user", "text": prompt})

        payload = {
            "modelUri": self.model_uri,
            "completionOptions": {
                "stream": False,
                "temperature": float(temperature),
                "maxTokens": str(max_tokens),
            },
            "messages": messages
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}"
        }

        response = requests.post(self.url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        # Ответ находится в result['result']['alternatives'][0]['message']['text']
        try:
            answer = result['result']['alternatives'][0]['message']['text']
        except Exception:
            answer = str(result)
        return answer