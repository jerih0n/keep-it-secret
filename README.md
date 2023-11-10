Keep it sectrer
=================

Python program providing the abbility to embed an encrypted message into image file. Currently works only with .png file.

This program uses steganography technique called least significant bit (LSB) and enhance it with security key. In a nutshell - a colour pixel is composed of red, green and blue, encoded on one byte. The idea is to store information in the first bit of every pixel's RGB component. In the worst case, the decimal value is different by one which is not visible to the human eye. In practice, if you don't have space to store all of your data in the first bit of every pixel you should start using the second bit, and so on. You have to keep in mind that the more your store data in an image, the more it can be detected. LSB however is a well known technique, and its vulnerable to steganography analysys. In order to enhance the security, the program applies a security key in a form of a salted password.


Information
-----------
Current capabilities of the program:

* encode: User provides string, password and image. The program encrypts the provided string with the provided password + salt and then embed the encrypted message into the image. As a result a new encrypted.png file is created
* decode: User provides image and password. The program firts extracts the encrypted message from the provided image and then decrypt. The result is the embedded message in plain text
* configuration*: So far the programm has one one configuration option - changing the provided password salt using config.ini file.
  
> *If you change the default salt, you must keep it the same way you keep your password. Without that you will not be able to decrypt the embedded message

> *Only images without compression are supported*, namely not JPEG as LSB bits might get tampered during the compression phase.

Installation
------------

This tool only require several python pachages for processing images, encryption and configuration. You can find all required dependencies in requirements.txt
To intall run the following command in the directory of this program

```bash
pip install -r requirements.txt
```

Usage
------------
For Windows:
    
```bash
cd [Program Directory where Encryptor.py is located] 
```
Then run in that 
```bash
python Encryptor.py
```
After that just follow the instruction

Acknowledgement
------------
Robin David and his LSB implementation. You can fine more here -> https://github.com/RobinDavid/LSB-Steganography/tree/master

