from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog
from PyQt6.QtCore import pyqtSignal, Qt

class VerifyFileWidget(QWidget):

    back_requested = pyqtSignal()

    def __init__(self):
        super(VerifyFileWidget, self).__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # UI Elements
        self.label = QLabel("<h2>Verify a File</h2>")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # File Selection Row
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Select File")
        self.file_input.setReadOnly(True) # Keep it read-only so they must use the button
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.open_file_dialog)
        
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.browse_button)

        self.known_hash_input = QLineEdit()
        self.known_hash_input.setPlaceholderText("Enter the known hash")
        self.known_hash_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.verify_button = QPushButton("Verify")
        self.verify_button.clicked.connect(self.clicked_verify)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.emit_back)

        # Add to layout
        layout.addWidget(self.label)
        layout.addLayout(file_layout)
        layout.addWidget(self.known_hash_input)
        layout.addWidget(self.verify_button)
        layout.addWidget(self.back_button)

    def open_file_dialog(self):
        # Filters for .json files but allows "All Files" too
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Encrypted Database", 
            "", 
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.file_input.setText(file_path)

    def clicked_verify(self):
        # Get entered password with: self.password_input.text()
        
        self.on_success()

    def emit_back(self):
        self.back_requested.emit()
    