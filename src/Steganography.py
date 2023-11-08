import sys
from PIL import Image
import random
import binascii



class Steganography(object):

    # this method performs steganography text embedding using Least Significant Bit (LSB) approach

    @staticmethod
    def embed_data_in_image_using_lsb_method(image_path, binary_data, output_image_path):
        try:
            # Open the image
            image = Image.open(image_path)

            # Check if the binary data can fit within the image
            image_capacity = image.width * image.height * 3  # Assuming RGB image
            if len(binary_data) > image_capacity:
                raise ValueError("Binary data is too large for the image.")

            # Embed the data into the image
            index = 0  # Index to track the position in the binary_data
            for y in range(image.height):
                for x in range(image.width):
                    pixel = list(image.getpixel((x, y)))
                    for component_index in range(3):  # RGB components
                        if index < len(binary_data):
                            current_bit = binary_data[index]
                            pixel[component_index] = (pixel[component_index] & 254) | int(current_bit)
                            index += 1
                    image.putpixel((x, y), tuple(pixel))

            # Save the modified image
            image.save(output_image_path)
            print(f"Data embedded successfully. Image created in {output_image_path} directory")
        except Exception as e:
            print(f"An error occurred: {e}")

    # this method text extraction from image with embedded text using Least Significant Bit (LSB) approach
    @staticmethod
    def extract_data_from_image(image_path):
        try:
            # Open the image
            image = Image.open(image_path)

            # Extract the embedded data
            binary_data = ""
            for y in range(image.height):
                for x in range(image.width):
                    pixel = list(image.getpixel((x, y)))
                    for component_index in range(3):  # RGB components
                        lsb = pixel[component_index] & 1
                        binary_data += str(lsb)

            return binary_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def encode_using_random_pixels(self, input_image_path, output_image_path, encode_text):

        self._normalize(input_image_path, output_image_path)
        self._hide_text(output_image_path, encode_text)

        #assert self._read_text(output_image_path) == encode_text, self._read_text(output_image_path)

    def decode(self, image_path):
        return self._read_text(image_path)

    def _normalize_pixel(self, r, g, b):
        if self._is_modify_pixel(r, g, b):
            seed = random.randint(1, 3)
            if seed == 1:
                r = self._normalize(r)
            if seed == 2:
                g = self._normalize(g)
            if seed == 3:
                b = self._normalize(b)
        return r, g, b

    def _modify_pixel(self, r, g, b):

        return map(self._modify, [r, g, b])

    def _is_modify_pixel(self, r, g, b):

        return r % self.DIST == g % self.DIST == b % self.DIST == 1

    def _modify(self,i):
        if i >= 128:
            for x in range(self.DIST + 1):
                if i % self.DIST == 1:
                    return i
                i -= 1
        else:
            for x in range(self.DIST + 1):
                if i % self.DIST == 1:
                    return i
                i += 1
        raise ValueError

    @staticmethod
    def _normalize(i):
        if i >= 128:
            i -= 1
        else:
            i += 1
        return i

    def _normalize(self, path, output):
        img = Image.open(path)
        img = img.convert('RGB')
        size = img.size
        new_img = Image.new('RGB', size)

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r, g, b = img.getpixel((x, y))
                _r, _g, _b = self._normalize_pixel(r, g, b)
                new_img.putpixel((x, y), (_r, _g, _b))
        new_img.save(output, "PNG", optimize=True)

    def _hide_text(self, path, text):

        text = str(text)

        # convert text to hex for write
        write_param = []
        _base = 0
        for _ in self._to_hex(text):
            write_param.append(int(_, 16) + _base)
            _base += 16

        # hide hex-text to image
        img = Image.open(path)
        counter = 0
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if counter in write_param:
                    r, g, b = img.getpixel((x, y))
                    r, g, b = self.modify_pixel(r, g, b)
                    img.putpixel((x, y), (r, g, b))
                counter += 1

        # save
        img.save(path, "PNG", optimize=True)

    @staticmethod
    def _to_hex(string):
        return binascii.hexlify(string.encode()).decode()

    @staticmethod
    def _to_str(string):
        return binascii.unhexlify(string).decode()

    def read_text(self, path):

        img = Image.open(path)
        counter = 0
        result = []
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r, g, b = img.getpixel((x, y))
                if self._is_modify_pixel(r, g, b):
                    result.append(counter)
                counter += 1
                if counter == 16:
                    counter = 0
        return self._to_str(''.join([hex(_)[-1:] for _ in result]))




