import sys
from src.CoreLogic import constants, welcome
from src.CoreLogic.Processors.main_processor import MainProcessor

if __name__ == '__main__':

    welcome.welcome()

    selected_file_type = 0
    selected_main_command = 0

    main_processor = MainProcessor()

    while True:
        try:
            main_command = int(input("Select action: \n 1) Encrypt \n 2) Decrypt \n 99) Exit \n"))
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
            file_type_command = int(input("Select file type: \n 1) Image - .png \n 99) Exit \n"))

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

    main_processor.process_action(selected_main_command, selected_file_type)


