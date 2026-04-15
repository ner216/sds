import qdarktheme

STYLES = {
    "Fusion-Dark": qdarktheme.load_stylesheet("dark"),
    "Adwaita-Dark": """
        /* Main Window and Dialogs */
        QMainWindow, QDialog, QWidget {
            background-color: #242424;
            color: #ffffff;
            font-family: "Cantarell", "Segoe UI", "Roboto", sans-serif;
            font-size: 10pt;
        }

        /* Text Entries (QLineEdit, QTextEdit, QPlainTextEdit) */
        QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #101010;
            border-radius: 6px;
            padding: 8px;
            selection-background-color: #3584e4;
        }

        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
            border: 2px solid #3584e4;
            padding: 7px; /* Adjust for border thickness */
        }

        /* Buttons */
        QPushButton {
            background-color: #303030;
            color: #ffffff;
            border: 1px solid #101010;
            border-radius: 6px;
            padding: 8px 16px;
            min-height: 20px;
            font-weight: 500;
        }

        QPushButton:hover {
            background-color: #3d3d3d;
        }

        QPushButton:pressed {
            background-color: #242424;
            color: #d0d0d0;
        }

        /* Suggested Action (Blue Button) */
        QPushButton#suggested-action {
            background-color: #3584e4;
            border: 1px solid #185fb4;
        }

        QPushButton#suggested-action:hover {
            background-color: #4791eb;
        }

        QPushButton#suggested-action:pressed {
            background-color: #2160ac;
        }

        /* Destructive Action (Red Button) */
        QPushButton#destructive-action {
            background-color: #e22c3c;
            border: 1px solid #a8202c;
        }

        /* Labels */
        QLabel {
            background-color: transparent;
            color: #ffffff;
        }

        QLabel#tip-label {
            color: #b0b0b0;
            font-size: 9pt;
            font-style: italic;
        }

        /* Combo Boxes (Dropdowns) */
        QComboBox {
            background-color: #303030;
            border: 1px solid #101010;
            border-radius: 6px;
            padding: 6px 12px;
        }

        QComboBox::drop-down {
            border: none;
            width: 20px;
        }

        /* Checkboxes */
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 1px solid #101010;
            background-color: #303030;
        }

        QCheckBox::indicator:checked {
            background-color: #3584e4;
            image: url(check_icon.png); /* You can add an SVG/PNG icon path here */
        }

        /* ScrollBars */
        QScrollBar:vertical {
            border: none;
            background: transparent;
            width: 10px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: #4d4d4d;
            min-height: 30px;
            border-radius: 5px;
            margin: 2px;
        }

        QScrollBar::handle:vertical:hover {
            background: #5d5d5d;
        }

        QScrollBar:horizontal {
            border: none;
            background: transparent;
            height: 10px;
        }

        QScrollBar::handle:horizontal {
            background: #4d4d4d;
            min-width: 30px;
            border-radius: 5px;
            margin: 2px;
        }

        /* Tab Bar */
        QTabBar::tab {
            background: #2b2b2b;
            padding: 8px 16px;
            border-bottom: 2px solid transparent;
        }

        QTabBar::tab:selected {
            border-bottom: 2px solid #3584e4;
            background: #353535;
        }
        """
}


