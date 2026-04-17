# Stylesheets to mimic the libadwaita theme on Gnome apps

adwaita_dark = """
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
        border: 1px solid #454545;
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
        border: 1px solid #454545;
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
        background-color: #353535; /* Matching the hamburger button elevation */
        color: #ffffff;
        border: 1px solid #454545;
        border-radius: 10px;       /* Matching your 10px rounding */
        padding: 6px 12px;
        min-width: 6em;
    }

    QComboBox:hover {
        background-color: #404040;
        border: 1px solid #454545;
    }

    QComboBox:on { /* When the popup is open */
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 0px;
        border: 2px solid #3584e4;
        padding: 5px 11px; /* Adjust for border thickness */
    }

    /* The arrow button container */
    QComboBox::drop-down {
        subcontrol-origin: padding;
        width: 30px;
        border-left-width: 0px; /* Remove internal line for a cleaner look */
        border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
    }

    /* The List View inside the combo box popup */
    QComboBox QAbstractItemView {
        background-color: #303030;
        border: 1px solid #454545;
        border-radius: 8px;
        selection-background-color: #3584e4;
        color: #ffffff;
        outline: none;
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

    QMenu {
        background-color: #303030;
        border: 1px solid #454545; /* Slightly lighter border looks more Adwaita */
        border-radius: 10px;       /* Match modern GNOME 40+ curvature */
        padding: 5px;
        margin: 2px;               /* Important: gives space for the rounding to render */
    }

    QMenu::item {
        background-color: transparent;
        padding: 6px 24px;
        border-radius: 6px; /* Adwaita uses rounded selection boxes */
        color: #ffffff;
    }

    /* This provides the "Glow" / Feedback you were looking for */
    QMenu::item:selected {
        background-color: #3584e4; /* Adwaita Blue */
        color: #ffffff;
    }

    QMenu::separator {
        height: 1px;
        background: #404040;
        margin: 4px 8px;
    }

    /* Tool Button (The Hamburger menu) */
    QToolButton {
        background-color: transparent;
        border-radius: 6px;
        padding: 4px;
    }

    QToolButton:hover {
        background-color: #3d3d3d; /* Feedback when hovering the hamburger icon */
    }

    QToolButton:pressed {
        background-color: #242424;
    }

    /* Remove the arrow next to the hamburger icon if using setMenu() */
    QToolButton::menu-indicator {
        image: none;
    }

    /* The Hamburger Menu Button */
    QToolButton {
        background-color: #353535; /* Lighter than #242424 to prevent blending */
        color: #ffffff;
        border: 1px solid #454545;
        border-radius: 10px; /* Matching the menu's curvature */
        padding: 4px;
    }

    QToolButton:hover {
        background-color: #404040; /* Feedback when the mouse is over it */
        border: 1px solid #454545; /* Lighter border highlight */
    }

    QToolButton:pressed {
        background-color: #1e1e1e; /* Darkens when clicked */
    }
"""

adwaita_light = """
    /* Main Window and Dialogs */
    QMainWindow, QDialog, QWidget {
        background-color: #fafafa; /* Adwaita light background */
        color: #2e3436; /* Standard dark text */
        font-family: "Cantarell", "Segoe UI", "Roboto", sans-serif;
        font-size: 10pt;
    }

    /* Text Entries */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox {
        background-color: #ffffff;
        color: #2e3436;
        border: 1px solid #cdc7c2; /* Soft grey border */
        border-radius: 6px;
        padding: 8px;
        selection-background-color: #3584e4;
        selection-color: #ffffff;
    }

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 2px solid #3584e4;
        padding: 7px; 
    }

    /* Buttons */
    QPushButton {
        background-color: #eeeeec; /* Light grey elevation */
        color: #2e3436;
        border: 1px solid #cdc7c2;
        border-radius: 6px;
        padding: 8px 16px;
        min-height: 20px;
        font-weight: 500;
    }

    QPushButton:hover {
        background-color: #f6f5f4;
    }

    QPushButton:pressed {
        background-color: #d6d6d1;
        color: #000000;
    }

    /* Suggested Action (Blue Button) - Stays blue, but slightly adjusted for light mode */
    QPushButton#suggested-action {
        background-color: #3584e4;
        color: #ffffff;
        border: 1px solid #185fb4;
    }

    QPushButton#suggested-action:hover {
        background-color: #4791eb;
    }

    /* Destructive Action (Red Button) */
    QPushButton#destructive-action {
        background-color: #e22c3c;
        color: #ffffff;
        border: 1px solid #a8202c;
    }

    /* Labels */
    QLabel {
        background-color: transparent;
        color: #2e3436;
    }

    QLabel#tip-label {
        color: #888a85; /* Muted text for tips */
        font-size: 9pt;
        font-style: italic;
    }

    /* Combo Boxes (Dropdowns) */
    QComboBox {
        background-color: #f6f5f4;
        color: #2e3436;
        border: 1px solid #cdc7c2;
        border-radius: 10px;
        padding: 6px 12px;
    }

    QComboBox:hover {
        background-color: #ffffff;
        border: 1px solid #94f0f0;
    }

    QComboBox QAbstractItemView {
        background-color: #ffffff;
        border: 1px solid #cdc7c2;
        border-radius: 8px;
        selection-background-color: #3584e4;
        color: #2e3436;
        outline: none;
    }

    /* Checkboxes */
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 1px solid #cdc7c2;
        background-color: #ffffff;
    }

    QCheckBox::indicator:checked {
        background-color: #3584e4;
        /* You may want to use a dark-check_icon.png here for contrast */
    }

    /* ScrollBars */
    QScrollBar:vertical {
        border: none;
        background: transparent;
        width: 10px;
    }

    QScrollBar::handle:vertical {
        background: #cdc7c2;
        min-height: 30px;
        border-radius: 5px;
    }

    /* Tab Bar */
    QTabBar::tab {
        background: #f6f5f4;
        color: #555753;
        padding: 8px 16px;
        border-bottom: 2px solid transparent;
    }

    QTabBar::tab:selected {
        border-bottom: 2px solid #3584e4;
        background: #ffffff;
        color: #2e3436;
    }

    /* Menus */
    QMenu {
        background-color: #ffffff;
        border: 1px solid #cdc7c2;
        border-radius: 10px;
        padding: 5px;
    }

    QMenu::item {
        background-color: transparent;
        padding: 6px 24px;
        border-radius: 6px;
        color: #2e3436;
    }

    QMenu::item:selected {
        background-color: #3584e4;
        color: #ffffff;
    }

    /* Hamburger Menu Button */
    QToolButton {
        background-color: #f6f5f4;
        color: #2e3436;
        border: 1px solid #cdc7c2;
        border-radius: 10px;
        padding: 4px;
    }

    QToolButton:hover {
        background-color: #ffffff;
        border: 1px solid #3584e4;
    }
"""