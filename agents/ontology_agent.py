class OntologyAgent:
    def __init__(self, model_wrapper, prompt_config=None):
        self.model = model_wrapper
        self.ontology_graph = []
        self._last_prompt = None
        self.prompt_config = prompt_config or {}

    def process(self, fragment, context=None):
        word_count = len(fragment.split())
        if word_count < 500:
            prompt = self.prompt_config.get("ontology_short", "Введите промпт по умолчанию (короткий)").format(fragment=fragment)
        elif 500 <= word_count <= 1500:
            prompt = self.prompt_config.get("ontology_medium", "Введите промпт по умолчанию (средний)").format(fragment=fragment)
        else:
            prompt = self.prompt_config.get("ontology_long", "Введите промпт по умолчанию (длинный)").format(fragment=fragment)
        self._last_prompt = prompt
        response = self.model.call(prompt)
        triplets = self.parse_triplets(response)
        self.ontology_graph.extend(triplets)
        return {"triplets": triplets, "raw_response": response, "ontology_graph": self.ontology_graph}

    def parse_triplets(self, response_text):
        triplets = []
        for line in response_text.split('\n'):
            parts = [x.strip() for x in line.split('–')]
            if len(parts) == 3:
                triplets.append(tuple(parts))
        return triplets