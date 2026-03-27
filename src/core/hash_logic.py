"""
Password hashing and authentication module using bcrypt.
Provides secure password storage and verification for the password manager.
"""

import bcrypt
import os
import hashlib as stdlib_hashlib

class Hash(object):
    def get_hashed_password(self, password: str) -> str:
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

    def derive_key(self, password: str) -> bytes:
        """
        Derive a fixed 256-bit key from a plain text password.

        This is used to encrypt/decrypt the password database.
        """
        return stdlib_hashlib.sha256(password.encode('utf-8')).digest()

    # def verify_password(self, password: str, hashed_password: str) -> bool:
    #     """
    #     Verify a plain text password against a hashed password.
        
    #     Args:
    #         password: Plain text password to verify
    #         hashed_password: Previously hashed password to compare against
        
    #     Returns:
    #         True if password matches, False otherwise
    #     """
    #     try:
    #         return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    #     except (ValueError, TypeError):
    #         return False

    # def save_master_password(self, password: str) -> bool:
    #     """
    #     Save the master password hash to file.
        
    #     Args:
    #         password: Plain text master password
        
    #     Returns:
    #         True if save successful, False otherwise
    #     """
    #     try:
    #         self.data_dir.mkdir(parents=True, exist_ok=True)
    #         hashed = self.get_hashed_password(password)
    #         with open(self.master_password_file, 'w') as f:
    #             f.write(hashed)
    #         return True
    #     except Exception as e:
    #         print(f"Error saving master password: {e}")
    #         return False

    # def authenticate_master_password(self, password: str) -> bool:
    #     """
    #     Verify a password against the stored master password hash.
        
    #     Args:
    #         password: Plain text password to verify
        
    #     Returns:
    #         True if password is correct, False otherwise
    #     """
    #     try:
    #         if not self.master_password_file.exists():
    #             return False
            
    #         with open(self.master_password_file, 'r') as f:
    #             stored_hash = f.read().strip()
            
    #         return self.verify_password(password, stored_hash)
    #     except Exception as e:
    #         print(f"Error authenticating password: {e}")
    #         return False

    #def master_password_exists(self) -> bool:
    #    """
    #    Check if master password has been set up.
    #    
    #    Returns:
    #        True if master password file exists, False otherwise
    #    """
    #    return self.master_password_file.exists()