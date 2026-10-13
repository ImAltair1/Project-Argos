from PySide6.QtCore import Signal, Qt

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget, 
    QLineEdit
)

from project_argos.models.media_entry import MediaEntry
from project_argos.ui.multi_select_list import MultiSelectList

from project_argos.constants import GAME_CATEGORIES

class EntryDetailsView(QWidget):
    back_requested = Signal()
    custom_tag_removal_requested = Signal(str)
    custom_tag_creation_requested = Signal(str)

    def __init__(self, 
                 available_custom_tags: list[str] # available custom tags in general
                 ):
        super().__init__()

        self.available_custom_tags = available_custom_tags

        # Is given by set_entry
        self.entry = None

        layout = QVBoxLayout()

        # Initiates the widgets where the info is put inside of
        self.back_button = QPushButton("Back")
        self.id_label = QLabel()
        self.title_label = QLabel()
        self.alt_titles_label = QLabel()
        self.type_label = QLabel()
        
        
        ## Category Selector area
        self.category_selector = MultiSelectList(GAME_CATEGORIES)
        self.category_selector.hide() #hide the widget after initiating it | .delete() deletes the widget
        self.edit_categories_button = QPushButton("Edit categories")
        self.category_selector.item_changed.connect(self.category_change)
        self.categories_label = QLabel()
    
        
        ### Custom tags area
        self.custom_tags_label = QLabel()

        self.edit_custom_tags_button = QPushButton("Edit Custom Tags")
        self.edit_custom_tags_button.clicked.connect(self.toggle_custom_tags_editor)

        self.custom_tags_selector = MultiSelectList(self.available_custom_tags, allow_removal=True,)
        self.custom_tags_selector.remove_requested.connect(self.custom_tag_removal_requested)
        self.custom_tags_selector.item_changed.connect(self.custom_tag_change)
        self.custom_tags_selector.hide()

        self.custom_tags_input = QLineEdit()
        self.custom_tags_input.setPlaceholderText("New tag name")
        self.custom_tags_input.hide()

        self.add_custom_tag_button = QPushButton("Create Tag")
        self.add_custom_tag_button.clicked.connect(self.request_custom_tag_creation)
        self.add_custom_tag_button.hide()
        



        # Layout the above widgets
        layout.addWidget(self.back_button)

        layout.addWidget(self.id_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.alt_titles_label)
        layout.addWidget(self.type_label)
        
        layout.addWidget(self.categories_label)
        layout.addWidget(self.edit_categories_button)
        layout.addWidget(self.category_selector)
        
        
        layout.addWidget(self.custom_tags_label)
        layout.addWidget(self.edit_custom_tags_button)
        layout.addWidget(self.custom_tags_selector)
        layout.addWidget(self.custom_tags_input)
        layout.addWidget(self.add_custom_tag_button)


        layout.addStretch() # add space at the end 

        # set the created leayout
        self.setLayout(layout)

        # connecting the back_button clicked to the back_request signal, and emit it
        self.back_button.clicked.connect(self.back_requested.emit)

        self.edit_categories_button.clicked.connect(self.toggle_category_editor)


    ##### CATEGORIES FUNCTIONS
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
            self.category_selector.set_selected_items(
                self.entry.categories
            )

            self.category_selector.show()
            self.edit_categories_button.setText("Done!")


    ### CUSTOM TAGS FUNCTIONS

    #follows same pattern as category
    def custom_tag_change(self, item):
        tag = item.text()

        if item.checkState() == Qt.CheckState.Checked:
            self.entry.add_custom_tag(tag)

        elif item.checkState() == Qt.CheckState.Unchecked:
            self.entry.remove_custom_tag(tag)

        self.update_custom_tags_label()


    #follows same pattern as category, basically makes the editor visible or not.
    def toggle_custom_tags_editor(self):
        if self.custom_tags_selector.isVisible():
            self.custom_tags_selector.hide()
            self.custom_tags_input.hide()
            self.add_custom_tag_button.hide()

            self.edit_custom_tags_button.setText("Edit Custom Tags")

        else:
            # Refresh available tags and current entry's selections
            self.custom_tags_selector.populate_items()
            self.custom_tags_selector.set_selected_items(
                self.entry.custom_tags
            )

            self.custom_tags_selector.show()
            self.custom_tags_input.show()
            self.add_custom_tag_button.show()

            self.edit_custom_tags_button.setText("Done!")


    def request_custom_tag_creation(self):
        # gets custom tags input and removes the blanks
        tag = self.custom_tags_input.text().strip()

        if not tag:
            return

        # clear input and emit creation request
        self.custom_tags_input.clear()
        self.custom_tag_creation_requested.emit(tag)
    


    # Sets the text that actually shows up in the entry page
    def set_entry(self, entry: MediaEntry):
        self.entry = entry

        self.id_label.setText(f"ID: {entry.id}")
        self.title_label.setText(entry.title)
        self.alt_titles_label.setText(f"Alt titles: {entry.alternative_titles}")
        self.type_label.setText(f"Type: {entry.media_type}")

        #Check if there are any already existing categories selected when loading, and select them
        self.category_selector.set_selected_items(self.entry.categories)
        self.update_categories_label()

        # this is to fix the fact that when changing media entries with the
        # custom tag menu open it would duplicate the one from the original one, visually
        # into the new entry.
        # when we switch from one entry to another we need to update the checkboxes to 
        # match the new entry, and calling pop_items() + set_sel_items() does that
        self.custom_tags_selector.populate_items()
        self.custom_tags_selector.set_selected_items(self.entry.custom_tags)
        self.update_custom_tags_label()


    # updates the categories label whenever we check or uncheck a category
    def update_categories_label(self):
        if not self.entry.categories:
            self.categories_label.setText("No categories.")
        else:
            sorted_categories = sorted(self.entry.categories, key=str.casefold)
            self.categories_label.setText(
                f"Categories: {', '.join(sorted_categories)}"
            )
    
    def update_custom_tags_label(self):
        if not self.entry.custom_tags:
            self.custom_tags_label.setText("No custom tags.")
        else:
            sorted_tags = sorted(self.entry.custom_tags, key=str.casefold)
            self.custom_tags_label.setText(
                f"Custom tags: {', '.join(sorted_tags)}"
            )
