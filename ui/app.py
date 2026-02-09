from __future__ import annotations

import sys
from PySide6 import QtCore, QtWidgets

from core.process import ProcessLister
from ui.ai_panel import AiAssistantPanel
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
        self.write_button = QtWidgets.QPushButton("Write Value")
        self.write_button.clicked.connect(self._confirm_write)

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
        grid.addWidget(self.write_button, 1, 0, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        ai_dock = self._make_dock("AI Assistant (Offline)", AiAssistantPanel())
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, ai_dock)

        advanced_dock = self._make_dock("Advanced / God Mode (Kernel)", self._build_advanced_panel())
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, advanced_dock)

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

    def _confirm_write(self) -> None:
        dialog = QtWidgets.QMessageBox(self)
        dialog.setWindowTitle("Confirm Memory Write")
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        dialog.setText(
            "Bu değişiklik oyunun ToS'ini ihlal edebilir ve kararsızlığa neden olabilir.\n"
            "Yalnızca izinli olduğunuz yazılımlarda ve riskleri anladıysanız devam edin."
        )
        dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
        dialog.exec()

    def _build_advanced_panel(self) -> QtWidgets.QWidget:
        panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(panel)
        enable = QtWidgets.QCheckBox("Enable Kernel Driver (Advanced)")
        enable.setChecked(False)
        warning = QtWidgets.QLabel(
            "Uyarılar:\\n"
            "• Kernel driver yüklemek sisteminizi kararsız hale getirebilir (BSOD riski).\\n"
            "• Driver Signature Enforcement'ı devre dışı bırakmanız veya test signing kullanmanız gerekir.\\n"
            "• Modern anti-cheat'ler (EAC, BattlEye, Vanguard) kernel erişimini tespit edip ban verebilir.\\n"
            "• Sadece eğitimsel/offline kullanım için. Online oyunlarda kullanmak yasaktır ve hesabınız riske girer."
        )
        warning.setWordWrap(True)
        layout.addWidget(enable)
        layout.addWidget(warning)
        layout.addStretch(1)
        return panel


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(CYBER_DARK)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
