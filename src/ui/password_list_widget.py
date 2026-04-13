from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QLabel, QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QHBoxLayout, QStyle
from PyQt6.QtCore import Qt, pyqtSignal

class PasswordListWidget(QWidget):

    back_requested = pyqtSignal()

    def __init__(self, db):
        super(PasswordListWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.db = db
        
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
        
        self.back_button = QPushButton("Lock")
        self.back_button.setFixedWidth(250)
        self.back_button.clicked.connect(self.emit_back)        
        self.layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.refresh_list()

    def refresh_list(self):
        # Clear the current list UI
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Add a row for each entry
        for item in self.db.get_entries():
            row = PasswordRowWidget(
                item["id"], item["site"], item["user"], item["pass"], 
                on_delete=self.delete_entry
            )
            self.scroll_layout.addWidget(row)

    def delete_entry(self, entry_id):
        self.db.delete_entry(entry_id)

        self.refresh_list()

    def add_entry_dialog(self):
        dialog = AddPasswordEntryDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()

            if new_data["site"] and new_data["pass"] and new_data["user"]:
                self.db.add_entry(new_data["site"], new_data["user"], new_data["pass"])

                self.refresh_list()

    def emit_back(self):
        self.back_requested.emit()

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
        self.toggle_visibility_button = QPushButton()
        self.toggle_visibility_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
        self.toggle_visibility_button.clicked.connect(self.toggle_password)
        
        self.delete_button = QPushButton()
        self.delete_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
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
        self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)

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