"""
Password Database with RSA signature for integrity.
"""

import traceback

import json
import os
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from core.hash_logic import Hash

class PasswordDB:
    def __init__(self, db_file_path: str, passphrase: str, verbose: bool = False):
        self.db_file = Path(db_file_path)
        self.passphrase = passphrase
        self.verbose = verbose
        self.password_locked = True
        self.entries = []

    def load_db(self):
        self.entries = []
        if not self.db_file.exists():
            return

        try:
            file_bytes = self.db_file.read_bytes()

            if len(file_bytes) >= 44:
                salt = file_bytes[0:16]
                nonce = file_bytes[16:28]
                ciphertext = file_bytes[28:]
                encryption_key = Hash.derive_key(self.passphrase, salt)[0]
                aesgcm = AESGCM(encryption_key)
                clear = aesgcm.decrypt(nonce, ciphertext, None)
                self.entries = json.loads(clear.decode('utf-8'))

                self.password_locked = False

                if self.verbose:
                    print(f"[INFO] Database decrypted and loaded successfully\n Path: {self.db_file}")
            else:
                raise Exception("[ERROR] File too small to contain necessary data.")
        except Exception as e:
            if self.verbose:
                print("-" * 30)
                traceback.print_exc()
                print("-" * 30)

            self.entries = []
            raise Exception("Invalid password or file!")

    def save_db(self):
        try:
            payload = json.dumps(self.entries, indent=2, ensure_ascii=False)
            plaintext = payload.encode('utf-8')

            key, salt = Hash.derive_key(self.passphrase)
            nonce = os.urandom(12)
            aesgcm = AESGCM(key)
            encrypted = salt + nonce + aesgcm.encrypt(nonce, plaintext, None)
            self.db_file.write_bytes(encrypted)

            return True
        except Exception as e:
            print(f"Error saving password DB: {e}")

            if self.verbose:
                print("-" * 30)
                traceback.print_exc()
                print("-" * 30)

            return False

    def get_entries(self):
        return list(self.entries)

    def add_entry(self, site, user, password):
        next_id = max((entry.get('id', 0) for entry in self.entries), default=0) + 1
        self.entries.append({"id": next_id, "site": site, "user": user, "pass": password})
        self.save_db()
        return next_id

    def delete_entry(self, entry_id):
        self.entries = [entry for entry in self.entries if entry.get('id') != entry_id]
        self.save_db()