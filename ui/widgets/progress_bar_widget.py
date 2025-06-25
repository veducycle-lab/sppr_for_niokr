from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar

class ProgressBarWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Прогресс обработки документов:")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def set_maximum(self, maximum):
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(0)

    def set_value(self, value):
        self.progress_bar.setValue(value)

    def reset(self):
        self.progress_bar.setValue(0)