from PySide6.QtWidgets import QLineEdit
from logging import raiseExceptions
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)


#from project_argos.constants import GAME_CATEGORIES

# Category selector menu is a widget, obviously
class MultiSelectList(QWidget):
    item_changed = Signal(object) #the signal carries the item/category that changed

    def __init__(self, 
                options: list[str]): ## when we initialize a MultiSelectList from now on we also give it the options it has to display
        super().__init__()

        self.options = options

        # one line text input to search
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search categories...")
        self.search_box.textChanged.connect(self.filter_options) #run this function whenever the text in the search box changes

        #the item list is a List widget
        self.options_list = QListWidget()  # creates the list itself
        self.options_list.itemChanged.connect(self.item_was_changed) #when an item is un/checked, run this function

        layout = QVBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(self.options_list)

        self.setLayout(layout)

        # run the function under to populate the list
        self.populate_items()

    def filter_options(self, search_text: str):

        for index in range(self.options_list.count()):
            item = self.options_list.item(index)
    
            item.setHidden(
                search_text.lower() not in item.text().lower() # If True, set Hidden
            )

            
            


    #function for when a category row is un/checked
    def item_was_changed(self, item):
        #emit the signal created before, where we are emitting
        # the category that was changed
        self.item_changed.emit(item) 


    def populate_items(self):
        for category in self.options:
            item = QListWidgetItem(category) # creates one row item

            # An item has a set of flags that describe what the user can do with it
            # The item in this case is the category we just added to the list
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable #basically, we are saying its a checkable item
                # this | is basically "take the item's existing capabilities and add "user can check this"
            )

            item.setCheckState(Qt.CheckState.Unchecked) #and the default check is "unchecked"

            self.options_list.addItem(item) # and then we add the row to the list

    def set_selected_items(self, selected_items):
        self.options_list.blockSignals(True) #makes it so doing these "load" categories setting doesnt
                                              # emit any signals 

        #uncheck everything
        for index in range(self.options_list.count()):
            item = self.options_list.item(index)
            item.setCheckState(Qt.CheckState.Unchecked)

        for category in selected_items:
            if category not in self.options:
                raise ValueError("This category is not included in the GAME_CATEGORIES list")
            
            items = self.options_list.findItems(
                                                category,  #find this category in the category list
                                                Qt.MatchFlag.MatchExactly #and find it by exact
                                            ) # this line returns a list, so we must remove the element from it
            if items:
                item = items[0]
                item.setCheckState(Qt.CheckState.Checked)

        self.options_list.blockSignals(False) #turn it back on again

        return True