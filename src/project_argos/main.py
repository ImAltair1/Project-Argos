
import sys

from PySide6.QtWidgets import QApplication, QWidget
# QApplication = manages the app itself
# QWidget is a basic Qt widget that can act as a simple window


# main app setup
def main():
    #creates the QApplication obj
    app = QApplication(sys.argv) 

    #creates a basic widget and sets up the base "params"
    window = QWidget()
    window.setWindowTitle("Project Argos")
    window.resize(1280, 720)
    window.show()

    #this starts the Qt's event loop
    sys.exit(app.exec())


#standard python pattern, calls main() if we run the file directly
#   but not if it is imported by another file
if __name__ == "__main__":
    main()







    