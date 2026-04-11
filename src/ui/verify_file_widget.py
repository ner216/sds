from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog
from PyQt6.QtCore import pyqtSignal, Qt

class VerifyFileWidget(QWidget):

    back_requested = pyqtSignal()
    verify_file = pyqtSignal(str, str)

    def __init__(self):
        super(VerifyFileWidget, self).__init__()

        # Location entered by the user for new safe
        self.specified_file_path = None

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

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
        self.known_hash_input.setEchoMode(QLineEdit.EchoMode.Normal)

        self.verify_button = QPushButton("Verify")
        self.verify_button.setFixedHeight(40)
        self.verify_button.clicked.connect(self.clicked_verify)

        self.back_button = QPushButton("Back")
        self.back_button.setFixedWidth(250)
        self.back_button.clicked.connect(self.emit_back)

        # Add to layout
        layout.addWidget(self.label)
        layout.addLayout(file_layout)
        layout.addWidget(self.known_hash_input)
        layout.addWidget(self.verify_button)
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignHCenter)

    def open_file_dialog(self):
        # Filters for .json files but allows "All Files" too
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open File", 
            "", 
            "All Files (*)"
        )
        if file_path:
            self.file_input.setText(file_path)
            self.specified_file_path = file_path

    def clicked_verify(self):        
        self.verify_file.emit(self.specified_file_path, self.known_hash_input.text().lower())
        
    def emit_back(self):
        self.back_requested.emit()
    