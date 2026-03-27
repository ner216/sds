"""
Password Database with RSA signature for integrity.
"""

import json
import os
from pathlib import Path
from core.signer import RSASigner
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class PasswordDB:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_file = self.data_dir / "passwords.json"
        self.sig_file = self.data_dir / "passwords.sig"

        self.signer = RSASigner()
        self.entries = []
        self.encryption_key = None

        self.load()

    def set_encryption_key(self, key: bytes):
        self.encryption_key = key
        self.load()

    def load(self):
        self.entries = []
        if not self.db_file.exists() or not self.sig_file.exists():
            return

        try:
            file_bytes = self.db_file.read_bytes()
            signature = self.sig_file.read_bytes()

            if not self.signer.verify(file_bytes, signature):
                print("[WARNING] Password DB integrity verification failed: signature mismatch.")
                return

            if self.encryption_key is not None and len(file_bytes) >= 28:
                # AES-GCM format: nonce(12) + ciphertext
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

    def save(self):
        try:
            payload = json.dumps(self.entries, indent=2, ensure_ascii=False)
            plaintext = payload.encode('utf-8')

            if self.encryption_key is not None:
                nonce = os.urandom(12)
                aesgcm = AESGCM(self.encryption_key)
                encrypted = nonce + aesgcm.encrypt(nonce, plaintext, None)
                self.db_file.write_bytes(encrypted)
                signature = self.signer.sign(encrypted)
            else:
                self.db_file.write_bytes(plaintext)
                signature = self.signer.sign(plaintext)

            self.sig_file.write_bytes(signature)
            return True
        except Exception as e:
            print(f"Error saving password DB: {e}")
            return False

    def get_entries(self):
        return list(self.entries)

    def add_entry(self, site, user, password):
        next_id = max((entry.get('id', 0) for entry in self.entries), default=0) + 1
        self.entries.append({"id": next_id, "site": site, "user": user, "pass": password})
        self.save()
        return next_id

    def delete_entry(self, entry_id):
        self.entries = [entry for entry in self.entries if entry.get('id') != entry_id]
        self.save()

