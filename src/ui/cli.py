import getpass

from core.hash_logic import Hash
from core.database import PasswordDB

class CLI():
    def __init__(self, db_file_path: str):
        passphrase = getpass.getpass("Password (input hidden) > ")
        self.db_file_path = db_file_path
        
        try:
            self.db = PasswordDB(self.db_file_path, passphrase)
            self.db.load_db()
        except Exception as e:
            print("[ERROR] Unable to open database. Wrong password?")

    def get_password(self, username: str):
        if self.db.password_locked: return
        
        entry_found = False

        for entry in self.db.get_entries():
            if not username.isdigit():
                if entry["site"].lower() == username.lower():
                    print(f"Password for {entry["site"]} > '{entry["pass"]}'")
                    entry_found = True
            else:
                if str(entry["id"]) == username:
                    print(f"Password for {entry["site"]} > '{entry["pass"]}'")
                    entry_found = True

        if entry_found == False:
            print(f"[INFO] Database does not contain an entry for {username}")

    def list_entries(self):
        if self.db.password_locked: return

        print("Saved Password Entries:")
        for entry in self.db.get_entries():
            print(f"  {entry["id"]}: {entry["site"]}")
        