from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog, QStyle
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal, Qt

class LoginWidget(QWidget):

    back_requested = pyqtSignal()
    decrypt_safe = pyqtSignal(str, str)

    def __init__(self):
        super(LoginWidget, self).__init__()

        self.specified_file_path = None

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # File Selection Row
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Select Database File (.json)")
        self.file_input.setReadOnly(True) # Keep it read-only so they must use the button
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.open_file_dialog)
        
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.browse_button)

        self.password_row = QHBoxLayout(self)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Master Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Action Buttons
        self.toggle_visibility_button = QPushButton()
        self.toggle_visibility_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
        self.toggle_visibility_button.clicked.connect(self.toggle_password)

        self.password_row.addWidget(self.password_input)
        self.password_row.addWidget(self.toggle_visibility_button)

        # Login button
        self.login_button = QPushButton("Unlock")
        self.login_button.clicked.connect(self.emit_unlock)

        # Back button
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.emit_back)

        # Add to layout
        layout.addLayout(file_layout)
        layout.addLayout(self.password_row)
        layout.addWidget(self.login_button)
        layout.addWidget(self.back_button)

    def toggle_password(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

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
            self.specified_file_path = file_path

    def emit_unlock(self):
        self.decrypt_safe.emit(self.specified_file_path, self.password_input.text())

    def emit_back(self):
        self.back_requested.emit()