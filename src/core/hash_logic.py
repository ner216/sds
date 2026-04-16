from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
from pathlib import Path
import hashlib

class Hash():
    # Derive a 256-bit key from password
    # If salt is None, a new salt is generated
    def derive_key(password: str, salt: bytes = None):
        if salt is None:
            # Generate 16 byte random salt
            salt = os.urandom(16)

        kdf = Scrypt(
            salt=salt,
            length=32,      # We want a 32-byte (256-bit) key for AES-256
            n=2**14,        # CPU/Memory cost (Increase to 2**15 or 2**16 for more security)
            r=8,            # Block size
            p=1             # Parallelization
        )

        key = kdf.derive(password.encode('utf-8'))
        
        return key, salt

    # algorithm can be sha1, sha224, sha256, sha384, sha512, md5
    def get_file_hash(file_path: str, algorithm='sha256') -> str:
        file_path = Path(file_path)
        hash_object = hashlib.new(algorithm)
        
        try:
            with open(file_path, 'rb') as f:
                # Read the file in 4KB chunks to save memory
                # lambda function iterates every 4KB until there is an empty byte. (b"")
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_object.update(chunk)
                print(f"[INFO] Successfully generated hash for file [{file_path}]")
        except FileNotFoundError:
            print(f"Error: The file at {file_path} was not found.")
            return False

        # Calculate the final hex string
        calculated_hash = hash_object.hexdigest()
        
        # Use lower() to ensure the comparison isn't foiled by casing
        return calculated_hash.lower()