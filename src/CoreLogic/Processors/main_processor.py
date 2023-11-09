from ..Processors.encryption_processor import EncryptionProcessor
from ..Processors.user_input_processor import UserInputProcessor
from ..Processors.steganography_processor import SteganographyProcessor
import cv2
import os
from getpass import getpass


class MainProcessor(object):

    def __init__(self):
        self.encrypted_file_name = "encrypted.png"
        self.default_salt = b'YX,~pg3cP@QWU(w;>z&nH46'
        self.encryption_processor = EncryptionProcessor(self.default_salt)  # TODO: add configuration for custom salt

    def process_action(self, main_command_type, file_command_type):
        if main_command_type == 1: # encrypt
            self._encrypt_png_image()
        if main_command_type == 2:
            self._decrypt_png_image()
            return

    def _process_encryption_for_selected_file_type(self, file_command_type):
        if file_command_type == 1:
            print("Encrypting .png image: \n")
            self._decrypt_png_image()

    def _encrypt_png_image(self):
        # get the mnemonic phrase

        phrase_to_encrypt = input("Message to encrypt: ")
        password_to_encrypt = getpass("Password: ")

        selected_valid_png_file_path = UserInputProcessor.get_target_file_path()

        selected_target_destination_directory = UserInputProcessor.get_destination_directory_path()

        try:

            encrypted_message_as_string= self.encryption_processor.encrypt_as_string(phrase_to_encrypt, password_to_encrypt)

            # for now it supports only LSB (Least Significant Bit) technique

            full_destination_path_and_file_name = os.path.join(selected_target_destination_directory, self.encrypted_file_name)

            steganography_processor = SteganographyProcessor(cv2.imread(selected_valid_png_file_path))

            img_encoded = steganography_processor.encode_text(encrypted_message_as_string)

            cv2.imwrite(full_destination_path_and_file_name, img_encoded)

            print(F"Encrypted message successfully embedded to image {full_destination_path_and_file_name}")



        except Exception as ex:
            print(F"Fatal Error. Encryption failed: Error Message: {str(ex)}")

    def _decrypt_png_image(self):
        # extract the encrypted data from image

        valid_jpg_file_path_of_image_to_decrypt = UserInputProcessor.get_target_file_path()

        password_to_decrypt = getpass("Password: ")

        steganography_processor = SteganographyProcessor(cv2.imread(valid_jpg_file_path_of_image_to_decrypt))

        decoded_encrypted_message_as_string = steganography_processor.decode_text()


        decrypted_result = self.encryption_processor.decrypt_byte_array_to_original_string(password_to_decrypt, decoded_encrypted_message_as_string)

        print(f"Phrase: \n {decrypted_result}")





