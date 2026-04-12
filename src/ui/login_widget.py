from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QStyle, QLabel
from PyQt6.QtCore import pyqtSignal, QTimer, Qt

import time

from utils.config import SafeConfig

class LoginWidget(QWidget):

    # Signal members to alert main_window.py of an action
    back_requested = pyqtSignal()
    decrypt_safe = pyqtSignal(str, str)

    def __init__(self):
        super(LoginWidget, self).__init__()

        # Retrieve the default path to save the database in the app data folder
        self.default_safe_path = SafeConfig().get_default_safe_path()
        self.specified_file_path = self.default_safe_path

        # Password cool down variables
        self.failed_attempts = 0
        self.lockout_end_time = 0
        self.cooldown_timer = QTimer()
        self.cooldown_timer.timeout.connect(self.update_ui_lockout)

        # Base layout (Only base layout can be initialized with self)
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        self.title_label = QLabel("<h2>Unlock Safe</h2>")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # File Selection Row
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setText(self.default_safe_path)
        self.file_input.setReadOnly(True) # Keep it read-only so they must use the button
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.open_file_dialog)
        
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

        # Login button
        self.login_button = QPushButton("Unlock")
        self.login_button.setFixedHeight(40)
        self.login_button.clicked.connect(self.emit_unlock)

        # Back button
        self.back_button = QPushButton("Back")
        self.back_button.setFixedWidth(250)
        self.back_button.clicked.connect(self.emit_back)

        # Add to layout
        layout.addWidget(self.title_label)
        layout.addLayout(file_layout)
        layout.addLayout(password_row)
        layout.addWidget(self.login_button)
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignHCenter)

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
            self.default_safe_path, 
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.file_input.setText(file_path)
            self.specified_file_path = file_path

    def emit_unlock(self):
        current_time = time.time()

        if current_time < self.lockout_end_time:
            remaining = int(self.lockout_end_time - current_time)
            self.login_button.setText(f"Locked! Wait {remaining}s")
            return

        self.decrypt_safe.emit(self.specified_file_path, self.password_input.text())

    def update_ui_lockout(self):
        remaining = int(self.lockout_end_time - time.time())
        if remaining > 0:
            self.login_button.setText(f"Locked ({remaining}s)")
        else:
            self.cooldown_timer.stop()
            self.login_button.setEnabled(True)
            self.login_button.setText("Unlock")

    def emit_back(self):
        self.back_requested.emit()