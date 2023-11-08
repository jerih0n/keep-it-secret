from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
from Steganography import Steganography
import sys
import constants
import welcome
from processor import MainProcessor
# Press the green button in the gutter to run the script.


if __name__ == '__main__':

    welcome.welcome()

    selected_file_type = 0
    selected_main_command = 0

    while True:
        try:
            main_command = int(input("Select action: \n 1) Encrypt \n 2) Decrypt \n 99) Exit"))
            if main_command not in constants.VALID_MAIN_COMMANDS:
                print(f"Unknown command {main_command}")
                continue

            if main_command == 99:
                sys.exit()
            selected_main_command = main_command
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

    while True:
        try:
            file_type_command = int(input("Select file type: \n 1) Image - .jpg 99) Exit"))

            if file_type_command not in constants.VALID_FILE_TYPE_COMMANDS:
                print(f"Unknown command {main_command}")
                continue
            if main_command == 99:
                sys.exit()
            selected_file_type = file_type_command
            break
        except Exception:
            print("Invalid input. Please enter a valid number.")
            continue

    main_processor_instance = MainProcessor()
    main_processor_instance.process_action(selected_main_command, selected_file_type)

    input_string = "Hello World"

    password = input("Enter password: \r")

    password_as_byte = password.encode("utf-8")
    input_as_bite_array = input_string.encode("utf-8")
    print(password_as_byte)

    #Crypto
    # Create a key from the password using PBKDF2HMAC
    salt = b'YX,~pg3cP@QWU(w;>z&nH46'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,  # You can adjust the number of iterations for your desired security level
        salt=salt,
        length=32  # The key length should match the key length expected by Fernet (32 bytes)
    )

    key = base64.urlsafe_b64encode(kdf.derive(password_as_byte))

    # Create a Fernet instance with the derived key
    fernet = Fernet(key)

    # Encrypt the plaintext
    encrypted_text = fernet.encrypt(input_as_bite_array)

    binary_array = ['{:08b}'.format(byte) for byte in encrypted_text]

    print("Encrypted text:", encrypted_text)

    steganography = Steganography()
   # steganography.embed_data_in_image_using_lsb_method("test4.jpg",binary_array,"D:\\Documents\\result.jpg")

    binary_data = steganography.extract_data_from_image("D:\\Documents\\result.jpg")




    print(binary_array)
    original_string = ''.join([chr(int(binary, 2)) for binary in binary_array])

    # Decrypt the encrypted text
    decrypted_text = fernet.decrypt(original_string.encode("utf-8"))

    print("Decrypted text:", decrypted_text.decode())
    print(decrypted_text)



    # You can also specify the encoding if needed, such as UTF-8
    # byte_array = string_to_encode.encode("utf-8")


