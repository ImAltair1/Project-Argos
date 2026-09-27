
from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import QLibrary
from PySide6.QtWidgets import (
    QGridLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from project_argos.models.media_entry import MediaEntry
from project_argos.ui.media_card import MediaCard


# for initial version of the LibraryView we'll use the QListWidget - in the future 
# it'd be cool to have the ability to choose which layout we want - Grid, list etc

#this library view extends the QWidget class, so we'll be eventually
# creating our own "widget"
class LibraryView(QWidget):
    
    # we give this widge the entries we have (MediaEntry)
    def __init__(self, entries):
        super().__init__()

        self.entries = entries

        #basically saying that this library view widget can be scrollable 
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True) # the widget inside the scroll area can resize with the available space

                        # A layout isnt a widget, so we need:
                        #   ScrollArea
                        #       ↓
                        #     Widget
                        #       ↓
                        #    GridLayout
                        #       ↓
                        #      Cards
                        # rather than trying to put a QGridLayout directly into the scrollarea
                        # this is the same idea as central_widget and QVBoxLayout

        # Set the layout as a Grid ?
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout()

                        # A grid has:
                        #row 0:  [0,0] [0,1] [0,2] [0,3]
                        #row 1:  [1,0] [1,1] [1,2] [1,3]
                        #row 2:  [2,0] [2,1] [2,2] [2,3]
                        #we add a widget in that cell like this: self.grid_layout.addWidget(card, row, column)
                        # so if row = 1 and col = 2, the card goes into cell [1,2]

        # Set the layout for this grid widget
        self.grid_widget.setLayout(self.grid_layout)

        # Have the grid widget be scrollable?
        self.scroll_area.setWidget(self.grid_widget)

        ### 
        layout = QVBoxLayout() #its a vertical layout
        layout.addWidget(self.scroll_area)

        self.setLayout(layout) #we set the layout as the one we created

        self.display_entries() #we display the entries, per the function under


    def display_entries(self): 
    #seperate from the rest for future multiple view mods
    # so we have a if view-mode = grid then display_grid, but if a different one display_list :p
        self.clear_grid() # clear grid
        self.display_grid() # populate grid

    def display_grid(self):

        columns = 6 # will be made to adjust to window size later
        
        for index, entry in enumerate(self.entries):
            row = index // columns
            column = index % columns

            card = MediaCard(entry)

            self.grid_layout.addWidget(card, row, column) 
            # i guess we add to the grid the card object, and in the row and column given?


    # keeps removing items until layout is empty
    def clear_grid(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0) #removes the first item out

            widget = item.widget() #check is the item contains a widget
            if widget is not None: # and if so, tells Qt to delete it
                widget.deleteLater()