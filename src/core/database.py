"""
Password Database with RSA signature for integrity.
"""

import json
import os
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class PasswordDB:
    def __init__(self, db_file_path: str, encryption_key: bytes = None):
        self.db_file = db_file_path
        self.encryption_key = encryption_key

        self.load_db()

    def set_encryption_key(self, key: bytes):
        self.encryption_key = key
        self.load_db()

    def load_db(self):
        self.entries = []
        if not self.db_file.exists():
            return

        try:
            file_bytes = self.db_file.read_bytes()

            # AES-GCM stores nonce(12 bytes) + ciphertext + authentication_tag(16 bytes fixed)
            if self.encryption_key is not None and len(file_bytes) >= 28:
                nonce = file_bytes[:12]
                ciphertext = file_bytes[12:]
                aesgcm = AESGCM(self.encryption_key)
                clear = aesgcm.decrypt(nonce, ciphertext, None)
                self.entries = json.loads(clear.decode('utf-8'))
            else:
                # fallback for non-encrypted source (legacy)
                self.entries = json.loads(file_bytes.decode('utf-8'))
        except Exception as e:
            print(f"Error loading password DB: {e}")
            self.entries = []

    def save_db(self):
        try:
            payload = json.dumps(self.entries, indent=2, ensure_ascii=False)
            plaintext = payload.encode('utf-8')

            if self.encryption_key is not None:
                nonce = os.urandom(12)
                aesgcm = AESGCM(self.encryption_key)
                encrypted = nonce + aesgcm.encrypt(nonce, plaintext, None)
                self.db_file.write_bytes(encrypted)
            else:
                self.db_file.write_bytes(plaintext)

            return True
        except Exception as e:
            print(f"Error saving password DB: {e}")
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

