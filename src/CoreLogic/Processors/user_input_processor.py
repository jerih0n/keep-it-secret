import sys
import os

class UserInputProcessor(object):

    @staticmethod
    def get_target_file_path() -> str:
        while True:

            try:
                target_file_paths = input("Enter full image path of the selected image or 99  to exit: ")
                if target_file_paths == "99":
                    sys.exit()
                if os.path.exists(target_file_paths) and os.path.isfile(target_file_paths) and target_file_paths.lower().endswith(".png"):
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
                target_destination_save_file = input("Enter destination directory path for embedded image or  99  to exit: ")
                if target_destination_save_file == "99":
                    sys.exit()
                if os.path.exists(target_destination_save_file) and os.path.isdir(target_destination_save_file):
                    return target_destination_save_file

                print("Invalid input")

                continue
            except Exception:
                print("Invalid input")
                continue