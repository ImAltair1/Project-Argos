from PySide6.QtWidgets import QLineEdit
from logging import raiseExceptions
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QCheckBox,
    QToolButton,
    QStyle,
    QSizePolicy,
)


#from project_argos.constants import GAME_CATEGORIES

# Category selector menu is a widget, obviously
class MultiSelectList(QWidget):
    item_changed = Signal(object) #the signal carries the item/category that changed
    remove_requested = Signal(str) # signal carries the custom tag for removal

    def __init__(self, 
                options: list[str], ## when we initialize a MultiSelectList from now on we also give it the options it has to display
                allow_removal: bool = False   ## whether we want each row to have a "delete" icon
                ): 

        super().__init__()

        self.options = options

        self.allow_removal = allow_removal
        self.option_checkboxes = {}


        # one line text input to search
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search categories...")
        self.search_box.textChanged.connect(self.filter_options) #run this function whenever the text in the search box changes

        #the item list is a List widget
        self.options_list = QListWidget()  # creates the list itself

        layout = QVBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(self.options_list)

        self.setLayout(layout)

        # run the function under to populate the list
        self.populate_items()



    def filter_options(self, search_text: str):

        for item in range(self.options_list.count()):
            option = item.data(Qt.ItemDataRole.UserRole)

            item.setHidden(
                search_text.casefold() not in option.casefold()
            )



    #function for when a category row is un/checked
    def item_was_changed(self, item):
        #emit the signal created before, where we are emitting
        # the category that was changed
        self.item_changed.emit(item) 


    def populate_items(self):
        self.options_list.clear() #the list will change during runtime so we need to clear it first
        self.option_checkboxes.clear()

        for option in sorted(self.options, key=str.casefold):
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, option)
            self.options_list.addItem(item)

            # Create a custom row for this option
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(4, 0, 4, 0)

            # Create the checkbox
            checkbox = QCheckBox(option)
            checkbox.toggled.connect(
                lambda _checked, cb=checkbox:
                    self.item_was_changed(cb)
            ) #the toggled signal sends a bool indicating whether its checked
            row_layout.addWidget(checkbox)
            row_layout.addStretch()

            # Add a delete button only when removal is enabled
            if self.allow_removal:
                delete_button = QToolButton()
                delete_button.setIcon(
                    self.style().standardIcon(
                        QStyle.StandardPixmap.SP_TrashIcon
                    )
                )
                delete_button.setToolTip(f"Delete '{option}'")
                delete_button.setAutoRaise(True)

                delete_button.clicked.connect(
                    lambda _checked=False, tag=option:
                        self.remove_requested.emit(tag)
                )

                row_layout.addWidget(delete_button)

            # Attach our custom row to the list item
            self.options_list.setItemWidget(item, row)
            item.setSizeHint(row.sizeHint())

            # Keep track of the checkbox for this option
            self.option_checkboxes[option] = checkbox


    def set_selected_items(self, selected_items):
        # Validate before changing anything
        for option in selected_items:
            if option not in self.option_checkboxes:
                raise ValueError(
                    f"The item '{option}' is not included "
                    "in the list given to MultiSelectList"
                )

        # First, uncheck everything
        for checkbox in self.option_checkboxes.values():
            checkbox.blockSignals(True)
            checkbox.setChecked(False)
            checkbox.blockSignals(False)

        # Then, check the selected options
        for option in selected_items:
            checkbox = self.option_checkboxes[option]
            checkbox.blockSignals(True)
            checkbox.setChecked(True)
            checkbox.blockSignals(False)

        return True