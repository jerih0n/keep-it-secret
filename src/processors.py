from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import os
import sys
from steganography import Steganography



class MainProcessor(object):

    def __init__(self):
        self.default_salt = b'YX,~pg3cP@QWU(w;>z&nH46'
        self.steganography_processor = Steganography()
        self.encryption_processor = EncryptionProcessor(self.default_salt)  # TODO: add configuration for custom salt

    def process_action(self, main_command_type, file_command_type):
        if main_command_type == 1: # encrypt
            self._encrypt_jpg()
        if main_command_type == 2:
            self._decrypt_jpg()
            return

    def _process_encryption_for_selected_file_type(self, file_command_type):
        if file_command_type == 1:
            print("Encrypting JPG: \n")
            self._encrypt_jpg()

    def _encrypt_jpg(self):
        # get the mnemonic phrase
        print('\033[93m' + "Warning! It's highly recommended to proceed with turned off internet connection for security reasons. You won't need it! \n" + '\033[0m')
        phrase_to_encrypt = input("Enter your phrase: ")
        password_to_encrypt = input("Enter your password " + '\033[93m' + "Warning! REMEMBER YOUR PASSWORD! WITHOUT IT YOU WON'T BE ABLE TO DECRYPT THE PHRASE! \n" + '\033[0m')

        print("\n")

        selected_valid_jpg_file_path = UserInputProcessor.get_target_file_path()

        selected_target_destination_directory = UserInputProcessor.get_destination_directory_path()

        try:

            encrypted_message_as_byte_array = self.encryption_processor.encrypt_as_byte_array(phrase_to_encrypt, password_to_encrypt)

            # for now it supports only LSB (Least Significant Bit) technique
            self.steganography_processor.embed_data_in_image_using_lsb_method(selected_valid_jpg_file_path, encrypted_message_as_byte_array, selected_target_destination_directory)

        except Exception as ex:
            print(F"Fatal Error. Encryption failed: Error Message: {str(ex)}")

    def _decrypt_jpg(self):
        # extract the encrypted data from image

        valid_jpg_file_path_of_image_to_decrypt = UserInputProcessor.get_target_file_path()
        password_to_decrypt = input(
            "Enter your password: " + '\033[93m' + "Warning! REMEMBER YOUR PASSWORD! WITHOUT IT YOU WON'T BE ABLE TO DECRYPT THE PHRASE! \n" + '\033[0m')

        encrypted_byte_array_extracted = self.steganography_processor.extract_data_from_image_lsg_method(valid_jpg_file_path_of_image_to_decrypt)

        decrypted_result = self.encryption_processor.decrypt_byte_array_to_original_string(password_to_decrypt, encrypted_byte_array_extracted)

        print(f"Phrase: \n {decrypted_result}")



class EncryptionProcessor(object) :

    def __init__(self, salt):
        self.salt = salt

    def encrypt_as_byte_array(self, phrase, password) -> object:
        password_as_byte = password.encode("utf-8")
        phrase_as_bite_array = phrase.encode("utf-8")

        fernet = self._create_farnet(password_as_byte)

        # Encrypt the plaintext
        encrypted_text = fernet.encrypt(phrase_as_bite_array)

        binary_array_result = ['{:08b}'.format(byte) for byte in encrypted_text]

        return binary_array_result

    def decrypt_byte_array_to_original_string(self, password, encrypted_byte_array) -> str:
        try:
            password_as_byte = password.encode("utf-8")
            encrypted_text = ''.join([chr(int(binary, 2)) for binary in encrypted_byte_array])
            fernet = self._create_farnet(password_as_byte)
        except  Exception as ex:
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



class UserInputProcessor(object):

    @staticmethod
    def get_target_file_path() -> str:
        while True:

            try:
                target_file_paths = input("Enter full image path of the selected image or 99  to exit")
                if target_file_paths == "99":
                    sys.exit()
                if os.path.exists(target_file_paths) and os.path.isfile(target_file_paths) and target_file_paths.lower().endswith(".jpg"):
                     return target_file_paths

                print("Invalid input try again")

                continue
            except Exception:
                print("Invalid input try again")
                continue

    @staticmethod
    def get_destination_directory_path() -> str:

        while True:
            try:
                target_destination_save_file = input("Enter destination directory path for embedded image or  99  to exit")
                if target_destination_save_file == "99":
                    sys.exit()
                if os.path.exists(target_destination_save_file) and os.path.isdir(target_destination_save_file):
                    return target_destination_save_file

                print("Invalid input")

                continue
            except Exception:
                print("Invalid input")
                continue