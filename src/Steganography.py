import sys
from PIL import Image
import random
import binascii



class Steganography(object):

    def __init__(self):
        self.encoded_file_name = "encrypted.jpg"

    # this method performs steganography text embedding using Least Significant Bit (LSB) approach
    def embed_data_in_image_using_lsb_method(self, image_path, binary_data, output_image_path):
        try:
            # Open the image
            image = Image.open(image_path)

            # concatenating bytes array into binary_data
            binary_data_concatenated = ""
            for i in range(0, len(binary_data)):
                for j in range(0, len(binary_data[i])):
                    binary_data_concatenated += str(binary_data[i][j])
            # Embed the length of binary_data as a 32-bit header

            data_length = len(binary_data_concatenated)
            header = format(data_length, "032b")

            # Check if the binary data and header can fit within the image
            image_capacity = image.width * image.height * 3  # Assuming RGB image
            if len(header) + data_length > image_capacity:
                raise ValueError("Binary data is too large for the image.")

            # Embed the header into the image
            header_index = 0  # Index to track the position in the header
            for y in range(image.height):
                if header_index >= 32:
                    break
                for x in range(image.width):
                    if header_index >= 32:
                        break

                    pixel = list(image.getpixel((x, y)))
                    for component_index in range(3):  # RGB components
                        if header_index < 32:
                            current_bit = header[header_index]
                            pixel[component_index] = (pixel[component_index] & 254) | int(current_bit)
                            header_index += 1
                            image.putpixel((x, y), tuple(pixel))


            # Embed the binary data into the image

            data_index = 0  # Index to track the position in the binary_data
            binary_data_len = len(binary_data_concatenated)

            for y in range(image.height):
                if data_index >= binary_data_len:
                    break

                for x in range(32, image.width): # skipping  first 32 pixel, they contain the header information
                    if data_index >= binary_data_len:
                        break

                    pixel = list(image.getpixel((x, y)))
                    for component_index in range(3):  # RGB components
                        if data_index < binary_data_len:
                            current_bit = binary_data_concatenated[data_index]
                            pixel[component_index] = (pixel[component_index] & 254) | int(current_bit)
                            data_index += 1
                            image.putpixel((x, y), tuple(pixel))


            # Save the modified image

            image.save(output_image_path)
        except Exception as e:
            print(f"An error occurred: {e}")


    # this method text extraction from image with embedded text using Least Significant Bit (LSB) approach
    def extract_data_from_image_using_lsb_method(self, image_path) -> object:
        try:
            # Open the image
            image = Image.open(image_path)

            # Extracted binary data length header
            header = ""
            header_index = 0

            for y in range(image.height):
                for x in range(image.width):
                    pixel = list(image.getpixel((x, y)))
                    for component_index in range(3):      # RGB components
                        if header_index < 32:  # Assuming a 32-bit header
                            lsb = pixel[component_index] & 1
                            header += str(lsb)
                            header_index += 1
                    else:
                        break

            # Convert the header to an integer to determine the data length
            data_length = int(header, 2)

            # Extracted binary data
            binary_data = ""
            data_index = 0

            for y in range(image.height):
                for x in range(image.width):
                    pixel = list(image.getpixel((x, y)))
                    for component_index in range(3): # RGB components
                        if data_index < data_length:
                            lsb = pixel[component_index] & 1
                        binary_data += str(lsb)
                        data_index += 1
                    else:
                        break

            binary_data_as_bytes_array = self._transform_concatenate_binary_data_to_bytes_array(binary_data)
            return binary_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    def _transform_concatenate_binary_data_to_bytes_array(self, binary_data):
        bytes_array = []
        bits_chunk = ""

        for i in range(0, binary_data):
            if i % 8 == 0:
                bytes_array.append(bits_chunk)
                bits_chunk = ""

            bits_chunk += str(binary_data[i])
        return bytes_array




