"""
RSA + SHA256 Digital Signature for password data integrity.
"""

from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature


class RSASigner:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.private_key_file = self.data_dir / "private_key.pem"
        self.public_key_file = self.data_dir / "public_key.pem"

        self.private_key = None
        self.public_key = None

        self._load_or_create_keys()

    def _load_or_create_keys(self):
        if self.private_key_file.exists() and self.public_key_file.exists():
            self._load_keys()
        else:
            self._generate_keys()

    def _generate_keys(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        self.public_key = self.private_key.public_key()

        self.private_key_file.write_bytes(
            self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

        self.public_key_file.write_bytes(
            self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    def _load_keys(self):
        self.private_key = serialization.load_pem_private_key(
            self.private_key_file.read_bytes(),
            password=None
        )

        self.public_key = serialization.load_pem_public_key(
            self.public_key_file.read_bytes()
        )

    def sign(self, data: bytes) -> bytes:
        return self.private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def verify(self, data: bytes, signature: bytes) -> bool:
        try:
            self.public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False
        except Exception as e:
            print(f"Signer verify error: {e}")
            return False

