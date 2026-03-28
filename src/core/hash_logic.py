"""
Password hashing and authentication module using bcrypt.
Provides secure password storage and verification for the password manager.
"""

import bcrypt
import os
import hashlib as stdlib_hashlib

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
        return stdlib_hashlib.sha256(password.encode('utf-8')).digest()