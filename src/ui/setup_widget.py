from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

class SetupWidget(QWidget):
    def __init__(self, on_success):
        super(SetupWidget, self).__init__()
        self.on_success = on_success

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>Create Master Password</h2>"))

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.setup_button = QPushButton("Setup")
        self.setup_button.clicked.connect(self.save_password)

        layout.addWidget(self.password_input)
        layout.addWidget(self.setup_button)

    def save_password(self):
        # Place logic here for saving the password

        self.on_success()