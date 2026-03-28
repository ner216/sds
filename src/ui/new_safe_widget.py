from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QStyle
from PyQt6.QtCore import pyqtSignal, Qt

from core.database import PasswordDB

class NewSafeWidget(QWidget):

    back_requested = pyqtSignal()
    create_safe = pyqtSignal(str, str)

    def __init__(self):
        super(NewSafeWidget, self).__init__()

        # Location entered by the user for new safe
        self.specified_file_path = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # File Selection Row
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Select Database File (.json)")
        self.file_input.setReadOnly(True) # Keep it read-only so they must use the button
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.create_file_dialog)
        
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.browse_button)

        # Password row layout
        password_row = QHBoxLayout()

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Action Buttons
        self.toggle_visibility_button = QPushButton()
        self.toggle_visibility_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
        self.toggle_visibility_button.clicked.connect(self.toggle_password)

        # Add elements to password row
        password_row.addWidget(self.password_input)
        password_row.addWidget(self.toggle_visibility_button)

        # Setup button
        self.setup_button = QPushButton("Setup")
        self.setup_button.setFixedHeight(40)
        self.setup_button.clicked.connect(self.setup)

        # Back button
        self.back_button = QPushButton("Back")
        self.back_button.setFixedWidth(100)
        self.back_button.clicked.connect(self.emit_back)

        # Add elements to page
        layout.addLayout(file_layout)
        layout.addLayout(password_row)
        layout.addWidget(self.setup_button)
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignHCenter)

    def toggle_password(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def create_file_dialog(self):
        # New logic for creating a file
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Create New Safe", 
            "", 
            "JSON Files (*.json)"
        )
        if file_path:
            # Ensure the file has a .json extension
            if not file_path.endswith(".json"):
                file_path += ".json"
            self.file_input.setText(file_path)
            self.specified_file_path = file_path

    def setup(self):
        self.create_safe.emit(self.specified_file_path, self.password_input.text())

    def emit_back(self):
        self.back_requested.emit()