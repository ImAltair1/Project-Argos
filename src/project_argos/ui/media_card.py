
from pathlib import Path


from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
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

        # Artwork
        self.artwork = QLabel("Artwork") 
        self.artwork.setAlignment(Qt.AlignmentFlag.AlignCenter) #new things, seems to just be to align it in the center of the frame
        
        
        #self.artwork.setFixedSize(150,210) #min height for the artwork
        
        self.display_artwork()

        # Title
        title = QLabel(entry.title)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter) #same thing, for the title

        # Media type
        media_type = QLabel(entry.media_type)
        media_type.setAlignment(Qt.AlignmentFlag.AlignCenter)#same thing, for the media type

        # Add these QLabel widgets to the layout and set the layout
        layout.addWidget(self.artwork)
        layout.addWidget(title)
        layout.addWidget(media_type)
        layout.addStretch()
        
        self.setLayout(layout)

        # After setting the layout, lets improve some of the basic visuals
        self.setFrameShape(QFrame.Shape.StyledPanel)



    def display_artwork(self):
        if self.entry.cover_art is None:
            artwork_path = (
                Path(__file__).resolve().parent.parent
                / "assets"
                / "no_artwork_test.jpg"
            )
        else:
            artwork_path = Path(self.entry.cover_art)

        pixmap = QPixmap(str(artwork_path))

        if pixmap.isNull():
            self.artwork.setText("Artwork not found")
            return

        scaled_pixmap = pixmap.scaled(
            150,
            210,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.artwork.setPixmap(scaled_pixmap)
        self.artwork.setAlignment(Qt.AlignmentFlag.AlignCenter)