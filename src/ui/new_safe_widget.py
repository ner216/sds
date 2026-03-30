from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QStyle, QProgressBar, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
import re

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

        # Strength Row
        strength_layout = QHBoxLayout()
        # Strength label
        self.strength_label = QLabel("Password Strength:")
        strength_layout.addWidget(self.strength_label)
        # Strength Bar
        self.strength_bar = QProgressBar()
        self.strength_bar.setFixedHeight(15)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setRange(0, 4)     # 0 (Empty) to 4 (Strong)
        self.strength_bar.setValue(0)
        strength_layout.addWidget(self.strength_bar)
        #self.strength_bar.setStyleSheet("QProgressBar::chunk { background-color: gray; }")

        # Connect the password input to a checking function
        self.password_input.textChanged.connect(self.update_strength)

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
        layout.addLayout(strength_layout)
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

    def update_strength(self, password):
        score = 0
        if not password:
            self.strength_bar.setValue(0)
            return

        # Strength Criteria
        if len(password) >= 8: score += 1
        if any(char.isdigit() for char in password): score += 1
        if any(char.isupper() for char in password): score += 1
        if re.search(r"[ !@#$%^&*(),.?\":{}|<>]", password): score += 1

        self.strength_bar.setValue(score)

    def setup(self):
        self.create_safe.emit(self.specified_file_path, self.password_input.text())

    def emit_back(self):
        self.back_requested.emit()