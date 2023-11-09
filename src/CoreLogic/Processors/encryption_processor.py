from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64


class EncryptionProcessor(object):

    def __init__(self, salt):
        self.salt = salt

    def encrypt_as_string(self, phrase, password) -> object:
        password_as_byte = password.encode("utf-8")
        phrase_as_bite_array = phrase.encode("utf-8")

        fernet = self._create_farnet(password_as_byte)

        # Encrypt the plaintext
        encrypted_text = fernet.encrypt(phrase_as_bite_array)

        return encrypted_text.decode('utf-8')

    def decrypt_byte_array_to_original_string(self, password, encrypted_as_string) -> str:
        try:
            password_as_byte = password.encode("utf-8")

            fernet = self._create_farnet(password_as_byte)

            return fernet.decrypt(encrypted_as_string)

        except Exception as ex:
            print(F"Decryption failed! Reason : {str(ex)}")


    def _create_farnet(self, password_as_byte) -> Fernet:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,  # You can adjust the number of iterations for your desired security level
            salt=self.salt,
            length=32  # The key length should match the key length expected by Fernet (32 bytes)
        )

        key = base64.urlsafe_b64encode(kdf.derive(password_as_byte))

        # Create a Fernet instance with the derived key
        fernet = Fernet(key)
        return  fernet
