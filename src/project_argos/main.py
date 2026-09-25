
from PySide6.QtCore import QElapsedTimer
import sys
from datetime import datetime
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

## vvvvvvv Imports  
from project_argos.models.media_entry import MediaEntry
from project_argos.models.game_entry import GameEntry
from project_argos.models.game_copy import GameCopy
from project_argos.models.game_session import GameSession


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
        sidebar_title = QLabel("ARGOS ICON")
        self.library_button = QPushButton("Library")
        self.timeline_button = QPushButton("Timeline")
        self.statistics_button = QPushButton("Statistics")
        self.settings_button = QPushButton("Settings")


            #add subwidgets to layout, by the order we want
        sidebar_layout.addWidget(sidebar_title)
        sidebar_layout.addWidget(self.library_button)
        sidebar_layout.addWidget(self.timeline_button)
        sidebar_layout.addWidget(self.statistics_button)
        sidebar_layout.addStretch() 
        sidebar_layout.addWidget(self.settings_button)
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

        statistics_title = QLabel("Statistics")
        statistics_description = QLabel("The statistics will go here")

        statistics_layout.addWidget(statistics_title)
        statistics_layout.addWidget(statistics_description)
        statistics_layout.addStretch()

        self.statistics_page.setLayout(statistics_layout)

            # SETTINGS #
        self.settings_page = QWidget()
        settings_layout = QVBoxLayout()

        settings_title = QLabel("Settings")
        settings_description = QLabel("The settings will go here")

        settings_layout.addWidget(settings_title)
        settings_layout.addWidget(settings_description)
        settings_layout.addStretch()

        self.settings_page.setLayout(settings_layout)    


            # If adding a new page DONT FORGET TO ADD NEW BUTTON


        # -------------------------
        # Stack the pages
        # -------------------------

        self.pages = QStackedWidget()

        self.pages.addWidget(self.library_page)
        self.pages.addWidget(self.timeline_page)
        self.pages.addWidget(self.statistics_page)
        self.pages.addWidget(self.settings_page)

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
        self.settings_button.clicked.connect(self.show_settings)



    def show_library(self):
        self.pages.setCurrentWidget(self.library_page)
    def show_timeline(self):
        self.pages.setCurrentWidget(self.timeline_page)
    def show_statistics(self):
        self.pages.setCurrentWidget(self.statistics_page)
    def show_settings(self):
        self.pages.setCurrentWidget(self.settings_page)



# main app setup
def main():

    ### temporary
    game = GameEntry("Persona 5 Royal")
    print(game)
    print(repr(game))


    copy1 = GameCopy("PS4", "Physical", "Owned")
    copy2 = GameCopy("Switch", "Digital", "Owned")
    game.add_copy(copy1)
    game.add_copy(copy2)
    print(game.copies) ## uses repr
    print(game.copies[0]) ##uses str
    
    
    game.alternative_titles.append("P5R")
    game.hours_played = 12.5
    print(game.alternative_titles)
    print(game.hours_played)


    session_copy1 = GameSession(
        datetime(2026, 9, 25, 19, 0), datetime(2026, 9, 25, 21, 30),
        copy1,
    )
    session_copy2 = GameSession(
        datetime(2026, 9, 26, 19, 0), datetime(2026, 9, 26, 22, 30),
        copy1,
    )
    print(f"{session_copy1.duration_hours()}h")
    print(f"{session_copy2.duration_hours()}h")
    

    game.add_session(session_copy1)
    game.add_session(session_copy2)
    print(game.sessions)
    print(game.total_session_hours())
    
    
    print(game.id)
    
    existing_id = "12345-example-id"
    game2 = GameEntry("Persona 4 Golden", existing_id)
    print(game2.id)
    ### temporary


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







    