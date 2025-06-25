from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QTextEdit, QDialog

class LogDetailDialog(QDialog):
    """
    Диалог для подробного просмотра log-entry (input/output/prompt)
    """
    def __init__(self, log_entry):
        super().__init__()
        self.setWindowTitle("Детализация шага пайплайна")
        layout = QVBoxLayout()
        for k in ["agent", "step_type", "input", "output", "prompt", "meta", "timestamp"]:
            te = QTextEdit(str(log_entry.get(k)))
            te.setReadOnly(True)
            layout.addWidget(te)
        self.setLayout(layout)

class PipelineHistoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.table = QTableWidget(0, 5)  # timestamp, agent, step_type, input/short, output/short
        self.table.setHorizontalHeaderLabels(["Время", "Агент", "Шаг", "Вход (коротко)", "Выход (коротко)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.show_details)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.history = []

    def update_history(self, history):
        self.table.setRowCount(0)
        self.history = history or []
        for entry in self.history:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(entry.get("timestamp", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(entry.get("agent", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(entry.get("step_type", ""))))
            input_short = str(entry.get("input", ""))[:70].replace('\n', ' ')
            output_short = str(entry.get("output", ""))[:70].replace('\n', ' ')
            self.table.setItem(row, 3, QTableWidgetItem(input_short))
            self.table.setItem(row, 4, QTableWidgetItem(output_short))

    def show_details(self, row, column):
        if row < len(self.history):
            dlg = LogDetailDialog(self.history[row])
            dlg.exec_()