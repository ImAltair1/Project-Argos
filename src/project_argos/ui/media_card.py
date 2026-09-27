
from pathlib import Path


from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from project_argos.models.media_entry import MediaEntry

class MediaCard(QFrame):
    # We are creating our own signal here
    # This means "ths widget has a signal called "entry selected" that can carry a Python obj.
    # Used in the mousepressedevent function
    entry_selected = Signal(object)


    #We will need to give it an object with MediaEntry class, so that it has all the information
    # it needs to display what we will want it to display.
    def __init__(self, entry: MediaEntry):
        super().__init__()

        self.entry = entry

        #Visual change when the cursor is above a MediaEntry - just to indicate its clickable
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout() #vertical layout inside this widget

        # Artwork
        self.artwork = QLabel("Artwork") 
        self.artwork.setAlignment(Qt.AlignmentFlag.AlignCenter) #new things, seems to just be to align it in the center of the frame
        self.artwork.setMinimumHeight(180) #min height for the artwork
        
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

        # After setting the layout, improve some of the basic visuals
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


    # method that Qt calls when theuser clicks on a media card -» it emits a single, sending the MediaEntry 
    # in this card
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            #emit this signal, and send the MediaEntry that belongs to this card along with it
            self.entry_selected.emit(self.entry) 

        super().mousePressEvent(event)