from PySide6.QtWidgets import QLineEdit
from logging import raiseExceptions
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)


from project_argos.constants import GAME_CATEGORIES

# Category selector menu is a widget, obviously
class CategorySelector(QWidget):
    category_changed = Signal(object) #the signal carries the category that changed

    def __init__(self):
        super().__init__()

        # one line text input to search
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search categories...")
        self.search_box.textChanged.connect(self.filter_categories) #run this function whenever the text in the search box changes

        #the category list is a List widget
        self.category_list = QListWidget()  # creates the list itself
        self.category_list.itemChanged.connect(self.category_was_changed) #when an item is un/checked, run this function

        layout = QVBoxLayout()
        layout.addWidget(self.search_box)
        layout.addWidget(self.category_list)

        self.setLayout(layout)

        # run the function under to populate the list
        self.populate_categories()

    def filter_categories(self, search_text: str):

        for index in range(self.category_list.count()):
            item = self.category_list.item(index)
    
            item.setHidden(
                search_text.lower() not in item.text().lower() # If True, set Hidden
            )

            
            


    #function for when a category row is un/checked
    def category_was_changed(self, item):
        #emit the signal created before, where we are emitting
        # the category that was changed
        self.category_changed.emit(item) 


    def populate_categories(self):
        for category in GAME_CATEGORIES:
            item = QListWidgetItem(category) # creates one row item

            # An item has a set of flags that describe what the user can do with it
            # The item in this case is the category we just added to the list
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable #basically, we are saying its a checkable item
                # this | is basically "take the item's existing capabilities and add "user can check this"
            )

            item.setCheckState(Qt.CheckState.Unchecked) #and the default check is "unchecked"

            self.category_list.addItem(item) # and then we add the row to the list

    def set_selected_categories(self, selected_cat_list):
        self.category_list.blockSignals(True) #makes it so doing these "load" categories setting doesnt
                                              # emit any signals 

        #uncheck everything
        for index in range(self.category_list.count()):
            item = self.category_list.item(index)
            item.setCheckState(Qt.CheckState.Unchecked)

        for category in selected_cat_list:
            if category not in GAME_CATEGORIES:
                raise ValueError("This category is not included in the GAME_CATEGORIES list")
            
            items = self.category_list.findItems(
                                                category,  #find this category in the category list
                                                Qt.MatchFlag.MatchExactly #and find it by exact
                                            ) # this line returns a list, so we must remove the element from it
            if items:
                item = items[0]
                item.setCheckState(Qt.CheckState.Checked)

        self.category_list.blockSignals(False) #turn it back on again

        return True