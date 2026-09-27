

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from project_argos.models.media_entry import MediaEntry

class MediaCard(QFrame):
    #We will need to give it an object with MediaEntry class, so that it has all the information
    # it needs to display what we will want it to display.
    def __init__(self, entry: MediaEntry):
        super().__init__()

        self.entry = entry

        layout = QVBoxLayout() #vertical layout inside this widget

        # Placeholder for artwork
        artwork = QLabel("Artwork") 
        artwork.setAlignment(Qt.AlignmentFlag.AlignCenter) #new things, seems to just be to align it in the center of the frame
        artwork.setMinimumSize(150, 210) #minimum size allowed for the cards

        title = QLabel(entry.title)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter) #same thing, for the title

        media_type = QLabel(entry.media_type)
        media_type.setAlignment(Qt.AlignmentFlag.AlignCenter)#same thing, for the media type

        # Add these QLabel widgets to the layout and set the layout
        layout.addWidget(artwork)
        layout.addWidget(title)
        layout.addWidget(media_type)

        self.setLayout(layout)