from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QStyle
from PyQt6.QtCore import Qt

class StartupWidget(QWidget):
    def __init__(self, on_unlock, on_new, on_verify):
        super(StartupWidget, self).__init__()
        self.on_unlock = on_unlock
        self.on_new = on_new
        self.on_verify = on_verify

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
        pixmap = icon.pixmap(64, 64)
        self.image_label.setPixmap(pixmap)

        # Central Widget
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        self.label = QLabel("<h2>Super Duper Secret</h2>")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.unlock_button = QPushButton("Unlock Safe")
        self.unlock_button.clicked.connect(self.clicked_unlock_button)

        self.new_safe_button = QPushButton("New Safe")
        self.new_safe_button.clicked.connect(self.clicked_new_safe_button)

        self.verify_file_button = QPushButton("Verify File")
        self.verify_file_button.clicked.connect(self.clicked_verify_file_button)

        # Add to layout
        layout.addWidget(self.image_label)
        layout.addWidget(self.label)
        layout.addWidget(self.unlock_button)
        layout.addWidget(self.new_safe_button)
        layout.addWidget(self.verify_file_button)

    def clicked_unlock_button(self):        
        self.on_unlock()

    def clicked_new_safe_button(self):        
        self.on_new()

    def clicked_verify_file_button(self):
        self.on_verify()