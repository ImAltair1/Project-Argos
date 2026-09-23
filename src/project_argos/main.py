
from PySide6.QtCore import QElapsedTimer
import sys

from PySide6.QtWidgets import (
    QApplication,#manages the app itself
    QLabel,
    QMainWindow,#main window for apps
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget, #basic Qt widget that can act as a simple window
    QStackedWidget,
)


# creates a class representing our app window
## We will gradually use classes to represent meaningful parts of Argos, like 
## main app window (this one), media entries, library views, review editors and database services
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Default window params
        self.setWindowTitle("Project Argos")
        self.resize(1280, 720)

        # -------------------------
        # Main application layout
        # -------------------------
        main_layout = QHBoxLayout()

        # -------------------------
        # Sidebar
        # -------------------------
            #Create the sidebar widget where we will store the layout in
        sidebar = QWidget()

            #Instantiate the sidebar layout var., where we will add the "sub-widgets"
        sidebar_layout = QVBoxLayout()

            #subwidgets 
        sidebar_title = QLabel("Sidebar")
        self.library_button = QPushButton("Library")
        self.timeline_button = QPushButton("Timeline")
        self.statistics_button = QPushButton("Statistics")

            #add subwidgets to layout, by the order we want
        sidebar_layout.addWidget(sidebar_title)
        sidebar_layout.addWidget(self.library_button)
        sidebar_layout.addWidget(self.timeline_button)
        sidebar_layout.addWidget(self.statistics_button)
        sidebar_layout.addStretch() 
        ### A stretch basically means not spreading the widgets across the entire layout, but letting
        ### it have space under

            #add layout to QWidget
        sidebar.setLayout(sidebar_layout)

        
        # -------------------------
        # Pages
        # -------------------------
            # Here we will implement the stacked widgets (pages) for the sidebar

            # LIBRARY #
        self.library_page = QWidget()
        library_layout = QVBoxLayout()

        library_title = QLabel("Library")
        library_description = QLabel("The media library will go here")

        library_layout.addWidget(library_title)
        library_layout.addWidget(library_description)
        library_layout.addStretch()

        self.library_page.setLayout(library_layout)

            # TIME LINE #
        self.timeline_page = QWidget()
        timeline_layout = QVBoxLayout()

        timeline_title = QLabel("Timeline")
        timeline_description = QLabel("The timeline will go here")

        timeline_layout.addWidget(timeline_title)
        timeline_layout.addWidget(timeline_description)
        timeline_layout.addStretch()

        self.timeline_page.setLayout(timeline_layout)


            # STATISTICS #
        self.statistics_page = QWidget()
        statistics_layout = QVBoxLayout()

        statistics_title = QLabel("statistics")
        statistics_description = QLabel("The statistics will go here")

        statistics_layout.addWidget(statistics_title)
        statistics_layout.addWidget(statistics_description)
        statistics_layout.addStretch()

        self.statistics_page.setLayout(statistics_layout)

        # -------------------------
        # Stack the pages
        # -------------------------

        self.pages = QStackedWidget()

        self.pages.addWidget(self.library_page)
        self.pages.addWidget(self.timeline_page)
        self.pages.addWidget(self.statistics_page)


        # -------------------------
        # Main layout
        # -------------------------
            # Now we add to the main layout the pages widget, which itself includes the other
            # pages as "sub widgets".
            # We will have the sidebar on the left and the pages on the right, so QHBoxLayout()

        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

        # -------------------------
        # Put the main layout
        # inside the window
        # -------------------------

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)


        # -------------------------
        # Button connections
        # -------------------------
            # Now we connect buttons to their respective functions, which are created afterwards
        
        self.library_button.clicked.connect(self.show_library)
        self.timeline_button.clicked.connect(self.show_timeline)
        self.statistics_button.clicked.connect(self.show_statistics)



    def show_library(self):
        self.pages.setCurrentWidget(self.library_page)
    def show_timeline(self):
        self.pages.setCurrentWidget(self.timeline_page)
    def show_statistics(self):
        self.pages.setCurrentWidget(self.statistics_page)



# main app setup
def main():
    #creates the QApplication obj
    app = QApplication(sys.argv) 

    #creates a basic widget and sets up the base "params" (which are now in the class MainWindow)
    window = MainWindow()
    window.show()

    #this starts the Qt's event loop
    sys.exit(app.exec())


#standard python pattern, calls main() if we run the file directly
#   but not if it is imported by another file
if __name__ == "__main__":
    main()







    