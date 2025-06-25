import openai

class GPTWrapper:
    """
    Обёртка для работы с OpenAI GPT-3/4 (openai>=1.0.0).
    """
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)  # новый способ авторизации

    def call(self, prompt, max_tokens=1024, temperature=0.3):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # либо "gpt-4-1106-preview" или др.
            messages=[
                {"role": "system", "content": "Ты полезный интеллектуальный ассистент для анализа текста и данных."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content