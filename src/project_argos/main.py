
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
        self.setWindowTitle("Project Argos ")
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
        library_button = QPushButton("Library")
        timeline_button = QPushButton("Timeline")
        statistics_button = QPushButton("Statistics")

            #add subwidgets to layout, by the order we want
        sidebar_layout.addWidget(sidebar_title)
        sidebar_layout.addWidget(library_button)
        sidebar_layout.addWidget(timeline_button)
        sidebar_layout.addWidget(statistics_button)
        sidebar_layout.addStretch() 
        ### A stretch basically means not spreading the widgets across the entire layout, but letting
        ### it have space under

            #add layout to QWidget
        sidebar.setLayout(sidebar_layout)


        # -------------------------
        # Main content
        # -------------------------
            # Now we repeat the same process as for the sidebar, but for Main Content part
        
        content = QWidget()

        content_layout = QVBoxLayout()

        title = QLabel("Project Argos")
        description = QLabel("Your personal media library and tracker")

        content_layout.addWidget(title)
        content_layout.addWidget(description)
        content_layout.addStretch()

        content.setLayout(content_layout)


        # -------------------------
        # Put sidebar + content
        # into the main layout
        # -------------------------
            # The sidebar and main_content widgets are still, well, widgets, so
            # now we insert them inside the originao main app layout.

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        # -------------------------
        # Put the main layout
        # inside the window
        # -------------------------

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)


    def on_button_clicked(self):
        self.message_label.setText("Button clicked! :) Good boy")



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







    