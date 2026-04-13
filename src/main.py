import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
import argparse

from ui.style import FUSION_DARK_STYLE, ADWAITA_DARK_STYLE  # Style sheets are stored in this file
from utils.config import SafeConfig
from ui.cli import CLI

def main():
    # Initialize config object for managing program settings
    default_safe_path = SafeConfig().get_default_safe_path()

    parser = argparse.ArgumentParser(description="A simple password manager.")
    parser.add_argument("-a", "--add-password", action="store_true", help="Add a new password entry to the default safe.")
    parser.add_argument("-d", "--delete-password", type=str, help="Delete a password from the default safe.")
    parser.add_argument("-g", "--get-password", type=str, help="Get password from default safe given the program-name/id.")
    parser.add_argument("-l", "--list", action="store_true", help="List saved password entries.")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode to perform many actions in one login session.")
    parser.add_argument("--delete-config", action="store_true", help="Delete all config data created by SDS.")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        # Start GUI if no args are given
        start_gui()
    elif args.list == True:
        CLI(default_safe_path).list_entries()
    elif args.add_password == True:
        CLI(default_safe_path).add_password()
    elif args.delete_config == True:
        SafeConfig().delete_all()
    elif args.interactive == True:
        CLI(default_safe_path).interactive_mode()
    elif args.delete_password:
        CLI(default_safe_path).delete_password(args.delete_password)
    elif args.get_password:
        CLI(default_safe_path).get_password(args.get_password)

def start_gui():
    app = QApplication(sys.argv)
    #app.setStyleSheet(ADWAITA_DARK_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()