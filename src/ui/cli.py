from pathlib import Path
import getpass

from core.hash_logic import Hash
from core.database import PasswordDB

class CLI():
    def __init__(self, db_file_path: str):
        self.db_file_path = db_file_path
        self.db_name = Path(db_file_path).stem
        passphrase = getpass.getpass(f"Password for {self.db_name} (input hidden) > ")
        
        try:
            self.db = PasswordDB(self.db_file_path, passphrase)
            self.db.load_db()
        except Exception as e:
            print("[ERROR] Unable to open database. Wrong password?")

    def add_password(self) -> None:
        if self.db.password_locked: return

        print("Add password details:")
        
        app = input("Program > ")
        user = input("Username > ")
        passwd = input("Password > ")

        try:
            self.db.add_entry(app, user, passwd)
            print(f"[INFO] Added password for {site}!")
        except Exception as e:
            print(f"[ERROR] Unable to save new password for {site}!\n Err: {e}")

    def delete_password(self, username_or_id: str):
        if self.db.password_locked: return

        entry_to_delete = None

        for entry in self.db.get_entries():
            if not username.isdigit():
                if entry["site"].lower() == username.lower():
                    entry_to_delete = entry
                    break
            else:
                if str(entry["id"]) == username:
                    entry_to_delete = entry
                    break

        if entry_to_delete is not None:
            self.db.delete_entry(entry["id"])
            print(f"[INFO] Deleted Password for {entry["site"]}")
        else:
            print(f"[INFO] Database does not contain an entry for {username_or_id}")

    def get_password(self, username: str):
        if self.db.password_locked: return
        
        entry_found = False

        for entry in self.db.get_entries():
            if not username.isdigit():
                if entry["site"].lower() == username.lower():
                    print(f"Password for {entry["site"]} > '{entry["pass"]}'")
                    entry_found = True
                    break
            else:
                if str(entry["id"]) == username:
                    print(f"Password for {entry["site"]} > '{entry["pass"]}'")
                    entry_found = True
                    break

        if entry_found == False:
            print(f"[INFO] Database does not contain an entry for {username}")

    def list_entries(self):
        if self.db.password_locked: return

        print("Saved Password Entries:")
        for entry in self.db.get_entries():
            print(f"  {entry["id"]}: {entry["site"]}")

    def interactive_mode(self):
        if self.db.password_locked: return
        choice = ""

        def print_operations():
            print(f"Operations for {self.db_name}:")
            print(" 1: (add) add a password")
            print(" 2: (del) delete a password")
            print(" 3: (get) get a password")
            print(" 4: (ls) list a passwords")
            print(" h: (help) print this list")
            print(" q: (quit)")

        print_operations()

        while choice != "q" or choice != "quit":
            choice = input("Operation > ").lower()

            if choice == "1" or choice == "add":
                self.add_password()
            elif choice == "2" or choice == "del":
                name_or_id = input("Enter ID or name of entry to delete > ")
                self.delete_password(name_or_id)
            elif choice == "3" or choice == "get":
                name_or_id = input("Enter ID or name of entry to get > ")
                self.get_password(name_or_id)
            elif choice == "4" or choice == "ls":
                self.list_entries()
            elif choice == "h" or choice == "help":
                print_operations()
            elif choice == "q" or choice == "quit":
                break
        



        