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
        
        name = input("Entry name > ")
        user = input("Username > ")
        passwd = input("Password > ")

        try:
            self.db.add_entry(name, user, passwd)
            print(f"[INFO] Added password for {name}!")
        except Exception as e:
            print(f"[ERROR] Unable to save new password for {name}!\n Err: {e}")

    def delete_password(self, name_or_id: str):
        if self.db.password_locked: return

        entry_to_delete = None

        for entry in self.db.get_entries():
            if not name_or_id.isdigit():
                if entry["site"].lower() == name_or_id.lower():
                    entry_to_delete = entry
                    break
            else:
                if str(entry["id"]) == name_or_id:
                    entry_to_delete = entry
                    break

        if entry_to_delete is not None:
            confirm_delete = input(f"Confirm delete for {entry["site"]} (y/N) > ")
            if confirm_delete.lower() == "y":
                self.db.delete_entry(entry["id"])
                print(f"[INFO] Deleted Password for {entry["site"]}")
        else:
            print(f"[INFO] Database does not contain an entry for {name_or_id}")

    def get_password(self, name_or_id: str):
        if self.db.password_locked: return
        
        entry_found = False

        for entry in self.db.get_entries():
            if not name_or_id.isdigit():
                if entry["site"].lower() == name_or_id.lower():
                    print(f"Password for {entry["site"]} > '{entry["pass"]}'")
                    entry_found = True
                    break
            else:
                if str(entry["id"]) == name_or_id:
                    print(f"Password for {entry["site"]} > '{entry["pass"]}'")
                    entry_found = True
                    break

        if entry_found == False:
            print(f"[INFO] Database does not contain an entry for {name_or_id}")

    def list_entries(self):
        if self.db.password_locked: return

        print("Saved Password Entries:")
        for entry in self.db.get_entries():
            print(f"  {entry["id"]}: {entry["site"]}")

    def backup_entries(self):
        if self.db.password_locked: return

        home_dir = Path.home()
        backup_path = home_dir / f"{self.db_name}_backup.txt"

        try:
            with open(backup_path, "w", encoding="utf-8") as f:
                for row in self.db.get_entries():
                    f.write(str(row) + "\n")
            print(f"Success! File created at: {backup_path}")
        except PermissionError:
            print(f"Error: You don't have permission to write to {home_dir}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

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
        



        