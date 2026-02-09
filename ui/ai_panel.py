from __future__ import annotations

from PySide6 import QtCore, QtWidgets

from core.ai_client import AiRequest, LocalAiClient


class AiAssistantPanel(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.prompt = QtWidgets.QTextEdit()
        self.prompt.setPlaceholderText("Ask the offline AI assistant (e.g., signature suggestions, pointer hints).")
        self.model = QtWidgets.QLineEdit("llama3.1")
        self.run_button = QtWidgets.QPushButton("Run Offline AI")
        self.output = QtWidgets.QTextEdit()
        self.output.setReadOnly(True)
        self.status = QtWidgets.QLabel("Local AI: waiting for input.")

        layout.addWidget(QtWidgets.QLabel("Model"))
        layout.addWidget(self.model)
        layout.addWidget(
            QtWidgets.QLabel(
                "Örnek istemler:\n"
                "• Bu AOB için en stabil signature öner\n"
                "• HP değeri için olası pointer chain yollarını tahmin et\n"
                "• Bu struct dump'ından field isimleri öner"
            )
        )
        layout.addWidget(self.prompt)
        layout.addWidget(self.run_button)
        layout.addWidget(self.output)
        layout.addWidget(self.status)

        self.run_button.clicked.connect(self._run)

    def _run(self) -> None:
        client = LocalAiClient()
        try:
            response = client.generate(AiRequest(prompt=self.prompt.toPlainText(), model=self.model.text().strip()))
        except Exception as exc:  # pragma: no cover - UI feedback only
            self.status.setText(f"AI error: {exc}")
            return
        self.output.setPlainText(response.content)
        self.status.setText("AI response received.")
