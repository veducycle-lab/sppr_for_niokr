from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class OntologyGraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Онтологический граф:")
        self.graph_display = QTextEdit()
        self.graph_display.setReadOnly(True)
        layout.addWidget(self.label)
        layout.addWidget(self.graph_display)
        self.setLayout(layout)

    def display_graph(self, ontology_graph):
        # Простая текстовая визуализация триплетов
        lines = [f"{t[0]} — {t[1]} — {t[2]}" for t in ontology_graph]
        self.graph_display.setPlainText("\n".join(lines))