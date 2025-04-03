import os
import json
import random
import string
from cryptography.fernet import Fernet
import argparse

# 1. Generate an encryption key
def generate_key():
    """
    Generates and saves the encryption key in a file called 'secret.key'.
    This key is used to encrypt/decrypt the passwords.
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Key generated and saved as 'secret.key'")

# 2. Password Manager Class
class PasswordManager:
    def __init__(self, key_file='secret.key', password_file='passwords.json'):
        # Load encryption key
        with open(key_file, 'rb') as key_file:
            self.key = key_file.read()
        self.cipher_suite = Fernet(self.key)
        self.password_file = password_file
        self.passwords = self.load_passwords()

    def load_passwords(self):
        """Load passwords from the encrypted file."""
        if os.path.exists(self.password_file):
            with open(self.password_file, 'r') as file:
                encrypted_data = json.load(file)
                return {service: self.decrypt_password(data) for service, data in encrypted_data.items()}
        return {}

    def save_passwords(self):
        """Save passwords to the encrypted file."""
        encrypted_data = {service: self.encrypt_password(data) for service, data in self.passwords.items()}
        with open(self.password_file, 'w') as file:
            json.dump(encrypted_data, file)

    def encrypt_password(self, password):
        """Encrypt the password."""
        return self.cipher_suite.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        """Decrypt the password."""
        return self.cipher_suite.decrypt(encrypted_password.encode()).decode()

    def add_password(self, service, password):
        """Add a new password for a service."""
        self.passwords[service] = password
        self.save_passwords()
        print(f"Password for {service} added successfully.")

    def get_password(self, service):
        """Retrieve a password for a service."""
        password = self.passwords.get(service)
        if password:
            return password
        else:
            print(f"No password found for {service}.")
            return None

    def list_passwords(self):
        """List all services for which passwords are stored."""
        if self.passwords:
            print("Stored passwords for the following services:")
            for service in self.passwords.keys():
                print(f"- {service}")
        else:
            print("No passwords stored.")

# 3. CLI Interface with argparse
def main():
    parser = argparse.ArgumentParser(description="CLI Password Manager")
    parser.add_argument('--add', metavar='service', type=str, help="Add a new password")
    parser.add_argument('--password', metavar='password', type=str, help="Password for the service")
    parser.add_argument('--get', metavar='service', type=str, help="Retrieve a password for a service")
    parser.add_argument('--list', action='store_true', help="List all stored services")
    parser.add_argument('--generate', action='store_true', help="Generate a random password")
    args = parser.parse_args()

    # Create an instance of the PasswordManager
    manager = PasswordManager()

    # Add a password
    if args.add:
        if args.password:
            manager.add_password(args.add, args.password)
        else:
            print("Please provide a password for the service.")

    # Get a password
    elif args.get:
        password = manager.get_password(args.get)
        if password:
            print(f"Password for {args.get}: {password}")

    # List all passwords
    elif args.list:
        manager.list_passwords()

    # Generate a random password
    elif args.generate:
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=16))
        print(f"Generated password: {password}")

if __name__ == "__main__":
    # Uncomment this line to generate the key once
    # generate_key()
    main()
