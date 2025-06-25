from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.controller import Controller
from agents.ontology_agent import OntologyAgent
from agents.expert_agent import ExpertAgent
from agents.simulation_agent import SimulationAgent
from models.gpt_wrapper import GPTWrapper
from models.yandexgpt_wrapper import YandexGPTWrapper
from models.gigachat_wrapper import GigaChatWrapper
import yaml

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()

    # Загружаем шаблоны промптов для агентов из конфига (если есть)
    prompts = config.get("prompts", {})

    # Инициализация моделей
    yandexgpt = YandexGPTWrapper(
        api_key=config["yandex_api_key"],
        model_uri=config.get("yandexgpt_model_uri", "gpt://b1gnpj1mopesukngnar1/yandexgpt-lite")
    )
    gpt = GPTWrapper(api_key=config["openai_api_key"])
    gigachat = GigaChatWrapper(access_token=config["gigachat_access_token"])
    # Модели добавляйте сюда при необходимости

    # По умолчанию — для старта — используем YandexGPT:
    agents = {
        "ontology": OntologyAgent(yandexgpt, prompt_config=prompts),
        "expert": ExpertAgent(yandexgpt),
        "simulation": SimulationAgent(yandexgpt)
    }

    controller = Controller(agents, config=config)
    
    app = QApplication([])
    window = MainWindow(controller)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()