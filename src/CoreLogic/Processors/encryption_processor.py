from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import hashlib

class EncryptionProcessor(object):

    def __init__(self, salt: str, pattern_repeat: int):
        self.salt = salt
        self.pattern_repeat = pattern_repeat

    def encrypt_as_string(self, phrase, password) -> object:

        password_as_byte = self._get_enhanced_password(password, self.pattern_repeat)
        phrase_as_bite_array = phrase.encode("utf-8")

        fernet = self._create_farnet(password_as_byte)

        # Encrypt the plaintext
        encrypted_text = fernet.encrypt(phrase_as_bite_array)

        return encrypted_text.decode('utf-8')

    def decrypt_byte_array_to_original_string(self, password, encrypted_as_string) -> str:
        try:

            password_as_byte = self._get_enhanced_password(password, self.pattern_repeat)

            fernet = self._create_farnet(password_as_byte)

            return fernet.decrypt(encrypted_as_string).decode("utf-8")

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


    def _apply_complex_pattern(self, password_as_string: str, salt: str, pattern_repeat: int):
        enhanced_password_pattern = ""
        for i in range(0, pattern_repeat):

            enhanced_password_pattern += str(f"{salt}_stack_sats_{password_as_string}")

        return enhanced_password_pattern

    def _apply_sha256(self, enhanced_password:str):
        # Create a new SHA-256 hash object
        sha256_hash_object = hashlib.sha256()

        # Update the hash object with the bytes of the input string
        sha256_hash_object.update(enhanced_password.encode('utf-8'))

        # Get the hexadecimal representation of the hash
        hashed_result = sha256_hash_object.hexdigest()

        return hashed_result

    def _get_enhanced_password(self, password:str, pattern_repeat: int):
        enhanced_password_pattern = self._apply_complex_pattern(password, pattern_repeat)
        sha256_as_string = self._apply_sha256(enhanced_password_pattern)
        return sha256_as_string.encode("utf-8")
