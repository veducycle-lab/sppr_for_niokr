from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton

class FeedbackWidget(QWidget):
    def __init__(self, on_feedback_submitted):
        super().__init__()
        self.on_feedback_submitted = on_feedback_submitted
        self.label = QLabel("Комментарии/обратная связь:")
        self.text = QTextEdit()
        self.button = QPushButton("Добавить")
        self.button.clicked.connect(self.submit_feedback)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.frag_id = None

    def set_fragment(self, frag_id):
        self.frag_id = frag_id

    def submit_feedback(self):
        if self.frag_id is not None:
            self.on_feedback_submitted(self.frag_id, self.text.toPlainText())
            self.text.clear()