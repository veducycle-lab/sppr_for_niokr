from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel

class ModelSelectorWidget(QWidget):
    def __init__(self, agent_names, on_model_changed_callback):
        super().__init__()
        self.on_model_changed_callback = on_model_changed_callback
        layout = QVBoxLayout()
        self.combo_boxes = {}
        for agent_name in agent_names:
            lbl = QLabel(f"Модель для {agent_name}:")
            box = QComboBox()
            box.addItems(["YandexGPT", "GPT-OpenAI", "GigaChat"])
            box.currentIndexChanged.connect(lambda idx, an=agent_name: self.model_selected(an, idx))
            layout.addWidget(lbl)
            layout.addWidget(box)
            self.combo_boxes[agent_name] = box
        self.setLayout(layout)

    def model_selected(self, agent_name, idx):
        selected_model = self.combo_boxes[agent_name].currentText()
        self.on_model_changed_callback(agent_name, selected_model)