import sys
from CoreLogic import constants, welcome
from CoreLogic.Processors.main_processor import MainProcessor
from configparser import ConfigParser


def read_config():
    parser = ConfigParser()
    try:
        parser = ConfigParser()
        parser.read(r'config.ini')
        configure_salt = parser.get("Security", "salt")
        pattern_repeat = int(parser.get("Security", "pattern_repeat"))
        return configure_salt, pattern_repeat
    except Exception as ex:
        print(f"Exception on attempting to configure the application with message: {ex}. Application will use default settings")
        return "", 1



if __name__ == '__main__':

    welcome.welcome()
    selected_file_type = 0
    selected_main_command = 0
    salt, pattern_repeat = read_config()
    main_processor = MainProcessor(salt, pattern_repeat)

    while True:
        try:
            print("Available Actions: \n 1) Encrypt \n 2) Decrypt \n 99) Exit \n")
            main_command = int(input("Action: "))
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
            print("Supported file types: \n 1) Image - .png \n 99) Exit \n")
            file_type_command = int(input("File type: "))

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


