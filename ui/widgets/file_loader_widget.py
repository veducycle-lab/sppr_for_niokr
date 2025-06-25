from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from core.utils import process_file

class FileLoaderWidget(QWidget):
    def __init__(self, on_file_loaded_callback):
        super().__init__()
        self.on_file_loaded_callback = on_file_loaded_callback
        layout = QVBoxLayout()
        self.label = QLabel("Загрузите входной файл (.pdf, .docx, .xlsx)")
        self.button = QPushButton("Загрузить файл")
        self.button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        path, _ = file_dialog.getOpenFileName(self, "Выберите файл", "", "Документы (*.pdf *.docx *.xlsx *.xls)")
        if path:
            fragments = process_file(path)
            self.label.setText(f"Загружено {len(fragments)} фрагментов")
            self.on_file_loaded_callback(fragments)