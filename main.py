
import sys
import requests

#Pyside 
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt


from PIL import Image
import numpy as np
from io import BytesIO

API_KEY = "YOUR_API_KEY"

#Random Image
def get_random_image():

    # connect to API Ninja (requiremnt)
    headers = {"X-Api-Key": API_KEY}
    requests.get(
        "https://api.api-ninjas.com/v1/quotes",
        headers=headers
    )

    #random image from Unsplash
    img = requests.get("https://picsum.photos/400/300")

    if img.status_code != 200:
        raise Exception("Failed to fetch image")

    return img.content


#Finding the dominant color logic
def get_dominant_color(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    #Resizing Image
    image = image.resize((100,100))
    
    pixels = np.array(image).reshape(-1, 3)

    #color count
    colors, counts = np.unique(pixels, axis=0, return_counts=True)
    dominant = colors[counts.argmax()]

    return tuple(dominant)


#Main GUI
class ImageApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color Identifier")
        self.setMinimumSize(600, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Title
        self.title = QLabel("Random Image Viewer")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Image container
        self.image_label = QLabel()
        self.image_label.setFixedSize(500, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""background-color: white;""")

        # Color preview box
        self.color_preview = QLabel()
        self.color_preview.setFixedHeight(50)
        self.color_preview.setStyleSheet("background-color: #ddd; border-radius: 6px;")

        # Color text
        self.color_label = QLabel("Dominant Color: None")
        self.color_label.setAlignment(Qt.AlignCenter)

        # Button
        self.button = QPushButton("Load Random Image")
        self.button.clicked.connect(self.load_image)

        # Add to layout
        layout.addWidget(self.title)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.color_preview)
        layout.addWidget(self.color_label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def load_image(self):
        try:
            self.color_label.setText("Loading...")
            QApplication.processEvents()

            image_bytes = get_random_image()

            pixmap = QPixmap()
            if not pixmap.loadFromData(image_bytes):
                self.color_label.setText("Invalid image data")
                return

            self.image_label.setPixmap(
                pixmap.scaled(
                    self.image_label.width(),
                    self.image_label.height(),
                    Qt.KeepAspectRatio
                )
            )

            r, g, b = get_dominant_color(image_bytes)

            self.color_label.setText(f"Dominant Color: RGB({r}, {g}, {b})")

            # Update color preview box
            self.color_preview.setStyleSheet(
                f"background-color: rgb({r},{g},{b}); border-radius: 6px;"
            )

        except Exception as e:
            self.color_label.setText(f"Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageApp()
    window.show()
    sys.exit(app.exec())

