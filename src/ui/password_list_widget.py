from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QFrame, QLabel, QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QHBoxLayout
from PyQt6.QtCore import Qt

class PasswordListWidget(QWidget):
    def __init__(self, on_logout):
        super(PasswordListWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        
        # Scroll Area Setup
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.scroll_content)
        
        self.layout.addWidget(self.scroll)
        
        # Controls
        self.add_entry_button = QPushButton("+ Add New Password")
        self.add_entry_button.clicked.connect(self.add_entry_dialog)
        self.layout.addWidget(self.add_entry_button)
        
        self.logout_button = QPushButton("Lock \U0001F512")
        self.logout_button.clicked.connect(on_logout)
        self.layout.addWidget(self.logout_button)

        self.refresh_list()

    def get_entries(self) -> dict:
        # Add logic for retrieving password entries from database

        mock_data = [
            {"id": 1, "site": "GitHub", "user": "coder1", "pass": "git_pass"},
            {"id": 2, "site": "Reddit", "user": "user_123", "pass": "reddit_secret"}
        ]

        return mock_data

    def refresh_list(self):
        # Clear the current list UI
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Add a row for each entry
        for item in self.get_entries():
            row = PasswordRowWidget(
                item["id"], item["site"], item["user"], item["pass"], 
                on_delete=self.delete_entry
            )
            self.scroll_layout.addWidget(row)

    def delete_entry(self, entry_id):
        # Add logic for deleting an entry from the database

        self.refresh_list()

    def add_entry_dialog(self):
        dialog = AddPasswordEntryDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()

            if new_data["site"] and new_data["pass"]:
                # Add logic for adding password to the database

                self.refresh_list()


class PasswordRowWidget(QWidget):
    def __init__(self, entry_id, site, user, password, on_delete):
        super(PasswordRowWidget, self).__init__()
        layout = QHBoxLayout(self)
        
        self.entry_id = entry_id
        
        # Site and User info
        layout.addWidget(QLabel(f"<b>{site}</b>"))
        layout.addWidget(QLabel(f"({user})"))
        
        # Password field (masked by default)
        self.password_field = QLineEdit(password)
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_field.setReadOnly(True)
        self.password_field.setFixedWidth(120)
        layout.addWidget(self.password_field)
        
        # Action Buttons
        self.toggle_visibility_button = QPushButton('\U0001F441')
        self.toggle_visibility_button.setFixedWidth(30)
        self.toggle_visibility_button.clicked.connect(self.toggle_password)
        
        self.delete_button = QPushButton('\U0001F5D1')
        self.delete_button.setStyleSheet("color: #ff4444;")
        self.delete_button.clicked.connect(lambda: on_delete(self.entry_id))
        
        layout.addWidget(self.toggle_visibility_button)
        layout.addWidget(self.delete_button)

    def toggle_password(self):
        if self.password_field.echoMode() == QLineEdit.EchoMode.Password:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)


class AddPasswordEntryDialog(QDialog):
    def __init__(self, parent=None):
        super(AddPasswordEntryDialog, self).__init__()
        self.setWindowTitle("Add New Password")
        self.setFixedWidth(350)

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        self.site_input = QLineEdit()
        self.user_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.form_layout.addRow("Website:", self.site_input)
        self.form_layout.addRow("Username:", self.user_input)
        self.form_layout.addRow("Password:", self.password_input)

        self.layout.addLayout(self.form_layout)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def get_data(self):
        return {
            "site": self.site_input.text(),
            "user": self.user_input.text(),
            "pass": self.password_input.text()
        }