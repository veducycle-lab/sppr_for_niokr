class SimulationAgent:
    """
    Агент what-if моделирования: выдает сценарии, анализ исходов.
    """
    def __init__(self, model_wrapper):
        self.model = model_wrapper
        self._last_prompt = None

    def process(self, scenario_context, ontology_context=None, extra_context=None):
        prompt = (
            "Смоделируй 3 возможных сценария развития событий на основе текущей информации ниже.\n"
            "Для каждого укажи риски, выгоды, вероятности успеха. Представь в табличной или маркированной форме.\n"
        )
        if ontology_context:
            prompt += f"Факты/связи (онтология): {ontology_context}\n"
        if extra_context:
            prompt += f"Доп. вводные: {extra_context}\n"
        prompt += f"\nАктуальная ситуация:\n{scenario_context}\n"
        self._last_prompt = prompt
        response = self.model.call(prompt)
        return {
            "scenarios": response.strip(),
        }