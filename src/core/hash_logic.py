"""
Password hashing and authentication module using bcrypt.
Provides secure password storage and verification for the password manager.
"""

import bcrypt
import os
from pathlib import Path
import hashlib

class Hash():

    @staticmethod
    def get_hashed_password(password: str) -> str:
        """
        Hash a password using bcrypt with salt.
        
        Args:
            password: Plain text password to hash
        
        Returns:
            Hashed password as string
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def derive_key(password: str) -> bytes:
        """
        Derive a fixed 256-bit key from a plain text password.

        This is used to encrypt/decrypt the password database.
        """
        return hashlib.sha256(password.encode('utf-8')).digest()

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