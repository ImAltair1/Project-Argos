from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from project_argos.models.media_entry import MediaEntry
from project_argos.ui.category_selector import CategorySelector

class EntryDetailsView(QWidget):
    back_requested = Signal()

    def __init__(self):
        super().__init__()

        # Is given by set_entry
        self.entry = None

        layout = QVBoxLayout()

        # Initiates the widgets where the info is put inside of
        self.back_button = QPushButton("Back")
        self.id_label = QLabel()
        self.title_label = QLabel()
        self.alt_titles_label = QLabel()
        self.type_label = QLabel()
        
        
        self.category_selector = CategorySelector()
        self.category_selector.hide() #hide the widget after initiating it | .delete() deletes the widget
        self.edit_categories_button = QPushButton("Edit categories")
        self.category_selector.category_changed.connect(self.category_change)
        self.categories_label = QLabel()
        

        self.custom_tags_label = QLabel()
        

        layout.addWidget(self.back_button)

        layout.addWidget(self.id_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.alt_titles_label)
        layout.addWidget(self.type_label)
        
        layout.addWidget(self.categories_label)
        layout.addWidget(self.edit_categories_button)
        layout.addWidget(self.category_selector)
        

        layout.addWidget(self.custom_tags_label)
        
        layout.addStretch()

        self.setLayout(layout)

        # connecting the back_button clicked to the back_request signal, and emit it
        self.back_button.clicked.connect(self.back_requested.emit)

        self.edit_categories_button.clicked.connect(self.toggle_category_editor)

    # function to test the category change system
    def category_change(self, item):

        if item.checkState() == Qt.CheckState.Checked:
            self.entry.add_category(item.text())
            
        elif item.checkState() == Qt.CheckState.Unchecked:
            self.entry.remove_category(item.text())
            
        self.update_categories_label()


    # function to show the category selector - runs when button is clicked
    def toggle_category_editor(self):
        if self.category_selector.isVisible():
            self.category_selector.hide()
            self.edit_categories_button.setText("Edit categories")
        else:
            #refresh the selected categories in case they were edited somewhere else
            self.category_selector.set_selected_categories(
                self.entry.categories
            )

            self.category_selector.show()
            self.edit_categories_button.setText("Done!")

    # Sets the text that actually shows up in the entry page
    def set_entry(self, entry: MediaEntry):
        self.entry = entry

        self.id_label.setText(f"ID: {entry.id}")
        self.title_label.setText(entry.title)
        self.alt_titles_label.setText(f"Alt titles: {entry.alternative_titles}")
        self.type_label.setText(f"Type: {entry.media_type}")

        #Check if there are any already existing categories selected when loading, and select them
        self.category_selector.set_selected_categories(entry.categories)
        self.update_categories_label()


        if not entry.custom_tags:
            self.custom_tags_label.setText("No custom tags added.")
        else:
            self.custom_tags_label.setText(
                f"Custom tags: {', '.join(entry.custom_tags)}"
            )

    # updates the categories label whenever we check or uncheck a category
    def update_categories_label(self):
        if not self.entry.categories:
            self.categories_label.setText("No categories.")
        else:
            self.categories_label.setText(
                f"Categories: {', '.join(self.entry.categories)}"
            )
