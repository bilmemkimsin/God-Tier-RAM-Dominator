from __future__ import annotations

import sys
from PySide6 import QtCore, QtWidgets

from core.process import ProcessLister
from ui.theme import CYBER_DARK


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TitanRAM - God Tier RAM Dominator")
        self.resize(1400, 900)
        self._build_layout()

    def _build_layout(self) -> None:
        self.setCentralWidget(QtWidgets.QWidget())
        grid = QtWidgets.QGridLayout(self.centralWidget())

        self.process_list = QtWidgets.QListWidget()
        self.process_list.setObjectName("processList")
        self.refresh_button = QtWidgets.QPushButton("Refresh Processes")
        self.refresh_button.clicked.connect(self._refresh_processes)

        self.scan_results = QtWidgets.QTableWidget(0, 4)
        self.scan_results.setHorizontalHeaderLabels(["Address", "Value", "Type", "Last Changed"])
        self.scan_results.horizontalHeader().setStretchLastSection(True)

        self.hex_view = QtWidgets.QTextEdit("Hex viewer placeholder")
        self.disasm_view = QtWidgets.QTextEdit("Disassembler placeholder")
        self.struct_view = QtWidgets.QTextEdit("Structure viewer placeholder")

        self.watch_list = QtWidgets.QListWidget()
        self.history_view = QtWidgets.QTextEdit("Value history graph placeholder")
        self.console = QtWidgets.QTextEdit("Script console placeholder")
        self.log_view = QtWidgets.QTextEdit("Log output")

        left_dock = self._make_dock("Processes", QtWidgets.QWidget())
        left_layout = QtWidgets.QVBoxLayout(left_dock.widget())
        left_layout.addWidget(self.refresh_button)
        left_layout.addWidget(self.process_list)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, left_dock)

        right_dock = self._make_dock("Hex + Disasm + Struct", QtWidgets.QWidget())
        right_layout = QtWidgets.QVBoxLayout(right_dock.widget())
        right_layout.addWidget(self.hex_view)
        right_layout.addWidget(self.disasm_view)
        right_layout.addWidget(self.struct_view)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, right_dock)

        bottom_dock = self._make_dock("Watch / History / Console / Logs", QtWidgets.QWidget())
        bottom_layout = QtWidgets.QHBoxLayout(bottom_dock.widget())
        bottom_layout.addWidget(self.watch_list)
        bottom_layout.addWidget(self.history_view)
        bottom_layout.addWidget(self.console)
        bottom_layout.addWidget(self.log_view)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.BottomDockWidgetArea, bottom_dock)

        grid.addWidget(self.scan_results, 0, 0)

        self._refresh_processes()

    def _make_dock(self, title: str, widget: QtWidgets.QWidget) -> QtWidgets.QDockWidget:
        dock = QtWidgets.QDockWidget(title, self)
        dock.setWidget(widget)
        dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetFloatable
            | QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable
        )
        return dock

    def _refresh_processes(self) -> None:
        self.process_list.clear()
        lister = ProcessLister()
        try:
            for proc in lister.list_processes():
                self.process_list.addItem(f"{proc.pid} - {proc.name}")
        except RuntimeError as exc:
            self.process_list.addItem(str(exc))


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(CYBER_DARK)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
