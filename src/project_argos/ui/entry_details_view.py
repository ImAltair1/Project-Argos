from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from project_argos.models.media_entry import MediaEntry


class EntryDetailsView(QWidget):
    back_requested = Signal()

    def __init__(self):
        super().__init__()

        self.entry = None

        layout = QVBoxLayout()

        self.back_button = QPushButton("Back")
        self.title_label = QLabel()
        self.alt_titles_label = QLabel()
        self.type_label = QLabel()
        self.id_label = QLabel()

        layout.addWidget(self.back_button)
        layout.addWidget(self.title_label)
        layout.addWidget(self.alt_titles_label)
        layout.addWidget(self.type_label)
        layout.addWidget(self.id_label)
        layout.addStretch()

        self.setLayout(layout)

        # connecting the back_button clicked to the back_request signal, and emit it
        self.back_button.clicked.connect(self.back_requested.emit)

    def set_entry(self, entry: MediaEntry):
        self.entry = entry

        self.title_label.setText(entry.title)
        self.alt_titles_label.setText(f"Alt titles: {entry.alternative_titles}")
        self.type_label.setText(f"Type: {entry.media_type}")
        self.id_label.setText(f"ID: {entry.id}")