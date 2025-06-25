class ExpertAgent:
    """
    Агент-эксперт: принимает решение, дает рекомендации.
    """
    def __init__(self, model_wrapper):
        self.model = model_wrapper
        self._last_prompt = None

    def process(self, fragment, ontology_context=None, constraints=None):
        prompt = "Предложи решение, используя информацию из текущего контекста и знаний из онтологии.\n"
        if ontology_context:
            prompt += f"Известные факты/связи (онтология): {ontology_context}\n"
        if constraints:
            prompt += f"Ограничения: {constraints}\n"
        prompt += f"\nВводные данные:\n{fragment}\nОтветь структурировано с обоснованием."
        self._last_prompt = prompt
        response = self.model.call(prompt)
        return {
            "decision": response.strip(),
        }