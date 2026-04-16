from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog, QComboBox
from PyQt6.QtCore import pyqtSignal, Qt

class VerifyFileWidget(QWidget):

    back_requested = pyqtSignal()
    verify_file = pyqtSignal(str, str, str)

    def __init__(self):
        super(VerifyFileWidget, self).__init__()

        # Location entered by the user for new safe
        self.specified_file_path = None
        # Hash algorithm selected by user
        self.specified_hash_algorithm = "sha256"

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

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

        # Row for entering hash value
        enter_hash_layout = QHBoxLayout()

        self.known_hash_input = QLineEdit()
        self.known_hash_input.setPlaceholderText("Enter the known hash")
        self.known_hash_input.setEchoMode(QLineEdit.EchoMode.Normal)

        self.algorithm_box = QComboBox()
        self.algorithm_box.addItems(['SHA-256 (recommended)', 'SHA-512', 'MD5'])
        self.algorithm_box.activated.connect(self.set_hash_algorithm)

        enter_hash_layout.addWidget(self.known_hash_input)
        enter_hash_layout.addWidget(self.algorithm_box)

        # Verify button
        self.verify_button = QPushButton("Verify")
        self.verify_button.setFixedHeight(40)
        self.verify_button.clicked.connect(self.clicked_verify)

        # Back button
        self.back_button = QPushButton("Back")
        self.back_button.setFixedWidth(250)
        self.back_button.clicked.connect(self.emit_back)

        # Add to layout
        layout.addWidget(self.label)
        layout.addLayout(file_layout)
        layout.addLayout(enter_hash_layout)
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

    def set_hash_algorithm(self, index):
        hash_map = {
            0: "sha256",
            1: "sha512",
            2: "md5"
        }
        
        self.specified_hash_algorithm = hash_map.get(index)

    def clicked_verify(self):        
        self.verify_file.emit(
            self.specified_file_path, 
            self.known_hash_input.text().lower(),
            self.specified_hash_algorithm
        )
        
    def emit_back(self):
        self.back_requested.emit()
    