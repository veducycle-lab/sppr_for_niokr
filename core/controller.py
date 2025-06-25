import time

class Controller:
    """
    Главный контроллер системы: маршрутизация данных между агентами,
    управление очередью задач и хранение контекста и истории аудита (лог pipeline).
    """
    def __init__(self, agents, config=None):
        self.agents = agents  # {'ontology': ..., 'expert': ..., 'simulation': ...}
        self.config = config or {}
        self.context = {
            'ontology_graph': [],
            'decisions': [],
            'scenarios': [],
            'user_feedback': {},
        }
        self.task_queue = []
        self.pipeline_history = []  # аудит цепочки операций

    def set_agent_model(self, agent_name, model_name):
        """
        Меняет LLM для указанного агента (использует данные из config.yaml)
        """
        if model_name == "YandexGPT":
            from models.yandexgpt_wrapper import YandexGPTWrapper
            model = YandexGPTWrapper(
                api_key=self.config["yandex_api_key"],
                model_uri=self.config.get("yandexgpt_model_uri", "gpt://b1gnpj1mopesukngnar1/yandexgpt-lite")
            )
        elif model_name == "GPT-OpenAI":
            from models.gpt_wrapper import GPTWrapper
            model = GPTWrapper(api_key=self.config["openai_api_key"])
        elif model_name == "GigaChat":
            from models.gigachat_wrapper import GigaChatWrapper
            model = GigaChatWrapper(access_token=self.config["gigachat_access_token"])
        else:
            raise ValueError("Неизвестная модель!")
        # Назначаем новую модель агенту
        self.agents[agent_name].model = model

    def add_user_feedback(self, fragment_id, feedback_text):
        self.context['user_feedback'][fragment_id] = feedback_text

    def log_step(self, agent_name, step_type, input_data, output_data, prompt=None, meta=None):
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "agent": agent_name,
            "step_type": step_type,
            "input": input_data,
            "output": output_data,
            "prompt": prompt,
            "meta": meta,
        }
        self.pipeline_history.append(log_entry)

    def process_file_fragments(self, fragments):
        all_triplets = []
        for frag_idx, fragment in enumerate(fragments, 1):
            # 1. Онтология
            ontology_agent = self.agents['ontology']
            res1 = ontology_agent.process(fragment)
            triplets = res1['triplets']
            all_triplets.extend(triplets)
            self.log_step(
                agent_name="OntologyAgent",
                step_type="extract_triplets",
                input_data=fragment,
                output_data=triplets,
                prompt=ontology_agent._last_prompt,
                meta={"fragment_index": frag_idx}
            )

            # 2. Эксперт
            expert_agent = self.agents['expert']
            res2 = expert_agent.process(fragment, ontology_context=triplets)
            self.context['decisions'].append(res2['decision'])
            self.log_step(
                agent_name="ExpertAgent",
                step_type="decision",
                input_data={"fragment": fragment, "ontology_context": triplets},
                output_data=res2['decision'],
                prompt=expert_agent._last_prompt,
                meta={"fragment_index": frag_idx}
            )

            # 3. Simulation
            sim_agent = self.agents['simulation']
            res3 = sim_agent.process(fragment, ontology_context=triplets)
            self.context['scenarios'].append(res3['scenarios'])
            self.log_step(
                agent_name="SimulationAgent",
                step_type="scenario_generation",
                input_data={"fragment": fragment, "ontology_context": triplets},
                output_data=res3['scenarios'],
                prompt=sim_agent._last_prompt,
                meta={"fragment_index": frag_idx}
            )

        self.context['ontology_graph'].extend(all_triplets)
        return self.context

    def get_history(self):
        return self.pipeline_history

    def reset(self):
        self.context = {
            'ontology_graph': [],
            'decisions': [],
            'scenarios': [],
            'user_feedback': {},
        }
        self.task_queue = []
        self.pipeline_history = []