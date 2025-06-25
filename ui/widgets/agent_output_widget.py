from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLabel

class AgentOutputWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Результаты работы агентов:")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.label)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def display_results(self, context):
        text = ""
        if "decisions" in context:
            text += "Экспертные решения:\n"
            for idx, dec in enumerate(context["decisions"], 1):
                text += f"{idx}. {dec}\n"
        if "scenarios" in context:
            text += "\nСценарии:\n"
            for idx, scen in enumerate(context["scenarios"], 1):
                text += f"{idx}. {scen}\n"
        self.output.setPlainText(text)