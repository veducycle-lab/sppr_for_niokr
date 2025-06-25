from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from ui.widgets.file_loader_widget import FileLoaderWidget
from ui.widgets.agent_output_widget import AgentOutputWidget
from ui.widgets.ontology_graph_widget import OntologyGraphWidget
from ui.widgets.progress_bar_widget import ProgressBarWidget
from ui.widgets.pipeline_history_widget import PipelineHistoryWidget
from ui.widgets.model_selector_widget import ModelSelectorWidget
from ui.widgets.feedback_widget import FeedbackWidget
from core.utils import load_ontology_from_owl

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Мультиагентная система поддержки решений")
        self.setGeometry(100, 100, 1000, 700)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        self.file_loader = FileLoaderWidget(self.on_file_loaded)
        layout.addWidget(self.file_loader)
        self.progress_bar = ProgressBarWidget()
        layout.addWidget(self.progress_bar)
        self.agent_output = AgentOutputWidget()
        layout.addWidget(self.agent_output)
        self.ontology_graph = OntologyGraphWidget()
        layout.addWidget(self.ontology_graph)
        self.pipeline_history = PipelineHistoryWidget()
        layout.addWidget(self.pipeline_history)
        self.model_selector = ModelSelectorWidget(
            agent_names=list(self.controller.agents.keys()),
            on_model_changed_callback=self.on_model_changed
        )
        layout.addWidget(self.model_selector)
        self.feedback_widget = FeedbackWidget(on_feedback_submitted=self.on_feedback)
        layout.addWidget(self.feedback_widget)

        # Загрузка внешней онтологии при старте (если файл есть)
        try:
            triplets = load_ontology_from_owl("ontology.owl")
            self.controller.context['ontology_graph'].extend(triplets)
            self.ontology_graph.display_graph(self.controller.context['ontology_graph'])
        except Exception as e:
            pass # нет файла — игнорируем

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_model_changed(self, agent_name, model_name):
        self.controller.set_agent_model(agent_name, model_name)
        
    def on_feedback(self, frag_id, text):
        self.controller.add_user_feedback(frag_id, text)

    def on_file_loaded(self, fragments):
        self.progress_bar.set_maximum(len(fragments))
        context = self.controller.process_file_fragments(fragments)
        self.agent_output.display_results(context)
        self.ontology_graph.display_graph(context['ontology_graph'])
        self.pipeline_history.update_history(self.controller.get_history())
        self.progress_bar.set_value(len(fragments))