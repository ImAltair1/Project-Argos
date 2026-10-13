from PySide6.QtCore import QElapsedTimer
import sys
from datetime import datetime
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,#main window for apps
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget, #basic Qt widget that can act as a simple window
    QStackedWidget,
    QMessageBox
)


from project_argos.ui.library_view import LibraryView
from project_argos.ui.entry_details_view import EntryDetailsView
from project_argos.models.media_library import MediaLibrary
from project_argos.demo_data import create_demo_entries
# creates a class representing our app window
## We will gradually use classes to represent meaningful parts of Argos, like 
## main app window (this one), media entries, library views, review editors and database services
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Test data 
        entries = create_demo_entries()
        self.media_library = MediaLibrary(entries=entries)
    

        #Default window params
        self.setWindowTitle("Project Argos")
        self.resize(1280, 720)

        

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
        self.library_page = LibraryView(self.media_library.entries)
        # important line, we are using the LibraryView class from library_view.py
        # to create a library with the temporary date we created earlier.

            # Details view #

        self.entry_details_page = EntryDetailsView(self.media_library.available_custom_tags)
        self.entry_details_page.custom_tag_removal_requested.connect(self.delete_custom_tag)
        self.entry_details_page.custom_tag_creation_requested.connect(self.create_custom_tag)


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
        self.pages.addWidget(self.entry_details_page)

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

        # entry_selected -» show_entry function on bottom
        self.library_page.entry_selected.connect(self.show_entry)
        # inside entry, if back -» show library view function on bottom
        self.entry_details_page.back_requested.connect(self.show_library)
        
############ METHODS #####################
    def create_custom_tag(self, tag: str):
        added = self.media_library.add_custom_tag(tag)

        if not added:
            QMessageBox.information(
                self,
                "Custom tag already exists",
                f"'{tag}' is already available in your library.",
            )
            return

        # Refresh the current entry and available tags
        self.entry_details_page.set_entry(
            self.entry_details_page.entry
        )


    def delete_custom_tag(self, tag: str):
        answer = QMessageBox.question(
            self,
            "Delete custom tag",
            f"Delete '{tag}' from the library?\n\n"
            "It will also be removed from every entry that uses it.",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self.media_library.remove_custom_tag(tag)

        # Refresh the currently displayed entry
        self.entry_details_page.set_entry(
            self.entry_details_page.entry
        )


    def show_library(self):
        self.pages.setCurrentWidget(self.library_page)
    def show_timeline(self):
        self.pages.setCurrentWidget(self.timeline_page)
    def show_statistics(self):
        self.pages.setCurrentWidget(self.statistics_page)
    def show_settings(self):
        self.pages.setCurrentWidget(self.settings_page)


    def show_entry(self, entry):
        self.entry_details_page.set_entry(entry)
        self.pages.setCurrentWidget(self.entry_details_page)



    
