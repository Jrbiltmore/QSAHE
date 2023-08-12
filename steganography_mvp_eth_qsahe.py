# steganography_mvp_eth_qsahe.py
# Author: Jacob Thomas Vespers (jttf@medusasec.com)

from cryptography.fernet import Fernet
from PIL import Image
import qrcode
import os
import argparse

# Import Ethereum interaction functions from ethereum_interaction.py
from ethereum_interaction import embed_data_into_ethereum, extract_data_from_ethereum, make_ethereum_payment

# Import QSAHE functions from qsahe_integration.py
from qsahe_integration import quantum_safe_encrypt, quantum_safe_decrypt

class SteganographyMVPEthQSAHE:
    def __init__(self, key):
        self.key = key
        self.cipher_suite = Fernet(key)

    def embed_data_into_image(self, image_path, data_to_embed, output_image_path):
        try:
            img = Image.open(image_path)
            data_to_embed = self.cipher_suite.encrypt(data_to_embed.encode())
            width, height = img.size
            max_bytes = (width * height * 3) // 8

            if len(data_to_embed) > max_bytes:
                raise ValueError("Data is too large to embed in the image")

            binary_data = ''.join(format(byte, '08b') for byte in data_to_embed)
            data_index = 0

            for y in range(height):
                for x in range(width):
                    pixel = list(img.getpixel((x, y)))

                    for i in range(3):
                        if data_index < len(binary_data):
                            pixel[i] = int(format(pixel[i], '08b')[:-1] + binary_data[data_index], 2)
                            data_index += 1

                    img.putpixel((x, y), tuple(pixel))

            img.save(output_image_path)
            print("Data embedded in the image successfully!")
        except Exception as e:
            print(f"Error embedding data into image: {e}")

    def extract_data_from_image(self, image_path):
        try:
            img = Image.open(image_path)
            binary_data = ""

            for y in range(img.height):
                for x in range(img.width):
                    pixel = img.getpixel((x, y))

                    for color in pixel:
                        binary_data += format(color, '08b')[-1]

            decrypted_data = self.cipher_suite.decrypt(bytes(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8)))
            print("Extracted and decrypted data:", decrypted_data.decode())
        except Exception as e:
            print(f"Error extracting data from image: {e}")

    def encrypt_and_embed_into_ethereum(self, data):
        try:
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            ethereum_tx_hash = embed_data_into_ethereum(encrypted_data)
            print("Data embedded into Ethereum. Transaction hash:", ethereum_tx_hash)
        except Exception as e:
            print(f"Error encrypting and embedding into Ethereum: {e}")

    def extract_from_ethereum_and_decrypt(self, ethereum_tx_hash):
        try:
            encrypted_data = extract_data_from_ethereum(ethereum_tx_hash)
            decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode()
            print("Extracted and decrypted data:", decrypted_data)
        except Exception as e:
            print(f"Error extracting and decrypting from Ethereum: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Steganography MVP with Ethereum and QSAHE")
    parser.add_argument("-k", "--key", help="Provide encryption key")
    args = parser.parse_args()

    if args.key:
        key = args.key.encode()
    else:
        key = Fernet.generate_key()

    steganography = SteganographyMVPEthQSAHE(key)

    while True:
        print("Steganography MVP with Ethereum and QSAHE")
        print("1. Embed data into image")
        print("2. Extract data from image")
        print("3. Encrypt and Embed data into Ethereum")
        print("4. Extract and Decrypt data from Ethereum")
        print("5. Quantum-safe Encrypt and Embed data")
        print("6. Quantum-safe Decrypt data")
        print("13. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            image_path = input("Enter path to the image: ")
            data_to_embed = input("Enter data to embed: ")
            output_image_path = input("Enter output image path: ")
            steganography.embed_data_into_image(image_path, data_to_embed, output_image_path)
        elif choice == "2":
            image_path = input("Enter path to the image: ")
            steganography.extract_data_from_image(image_path)
        elif choice == "3":
            data_to_embed = input("Enter data to embed: ")
            steganography.encrypt_and_embed_into_ethereum(data_to_embed)
        elif choice == "4":
            ethereum_tx_hash = input("Enter Ethereum transaction hash: ")
            steganography.extract_from_ethereum_and_decrypt(ethereum_tx_hash)
        elif choice == "5":
            data_to_embed = input("Enter data to embed: ")
            quantum_encrypted_data = quantum_safe_encrypt(data_to_embed)
            print("Data quantum-safe encrypted:", quantum_encrypted_data)
        elif choice == "6":
            quantum_encrypted_data = input("Enter quantum-safe encrypted data: ")
            decrypted_data = quantum_safe_decrypt(quantum_encrypted_data)
            print("Quantum-safe decrypted data:", decrypted_data)
        elif choice == "13":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select a valid option.")
