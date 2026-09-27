
import sys
from PySide6.QtWidgets import (
    QApplication,#manages the app itself
)

from project_argos.ui.main_window import MainWindow



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







    