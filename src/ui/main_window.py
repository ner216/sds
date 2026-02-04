from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QStackedWidget


from ui.master_login_widget import MasterLoginWidget
from ui.setup_widget import SetupWidget
from ui.password_list_widget import PasswordListWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.setMinimumSize(450, 350)

        self.setup_screen = SetupWidget(on_success=self.go_to_password_view)
        self.master_login = MasterLoginWidget(on_success=self.go_to_password_view)
        self.password_view = PasswordListWidget(on_logout=self.go_to_login)

        self.stack.addWidget(self.setup_screen)
        self.stack.addWidget(self.master_login)
        self.stack.addWidget(self.password_view)

        if self.master_login_exists():
            self.go_to_login()
        else:
            self.go_to_setup()

    # Logic to check if an account is already set up.
    def master_login_exists(self) -> bool:
        #if database file -> True
        #else -> False

        return True

    def go_to_setup(self):
        self.stack.setCurrentIndex(0)
        self.setWindowTitle("Super Duper Secret - Setup")

    def go_to_login(self):
        self.stack.setCurrentIndex(1)
        self.setWindowTitle("Super Duper Secret - Login")
    
    def go_to_password_view(self):
        self.stack.setCurrentIndex(2)
        self.setWindowTitle("Super Duper Secret - Passwords")
        