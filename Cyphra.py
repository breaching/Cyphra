import random
import string
import secrets
import os
import subprocess
import shutil

banner = """

  /$$$$$$                      /$$                         
 /$$__  $$                    | $$                         
| $$  \__/ /$$   /$$  /$$$$$$ | $$$$$$$   /$$$$$$  /$$$$$$ 
| $$      | $$  | $$ /$$__  $$| $$__  $$ /$$__  $$|____  $$
| $$      | $$  | $$| $$  \ $$| $$  \ $$| $$  \__/ /$$$$$$$
| $$    $$| $$  | $$| $$  | $$| $$  | $$| $$      /$$__  $$
|  $$$$$$/|  $$$$$$$| $$$$$$$/| $$  | $$| $$     |  $$$$$$$
 \______/  \____  $$| $$____/ |__/  |__/|__/      \_______/
           /$$  | $$| $$                                   
          |  $$$$$$/| $$                                   
           \______/ |__/                                   
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    try:
        clear()
        print(banner + "\n")
        file_path = input("\n[+] Path Of The Payload: ")
        with open(file_path) as f:
            contents = f.read()
    except FileNotFoundError:   
        print("\n[!] File not found.")
        return

    compile_option = input("\n[+] Do you want to compile the payload into an executable? (yes/no): ").lower()
    if compile_option == "yes":
        encrypted_filename = random_file()
        try:
            with open(encrypted_filename, 'w') as f:
                f.write(contents)

            output_file = open(os.devnull, 'w') if os.name != 'nt' else open('NUL', 'w')

            print(f"\n[?] File is being Compiled...")
            subprocess.run(['pyinstaller', '--noconfirm', '--onefile', encrypted_filename], stdout=output_file, stderr=output_file)

            os.remove(encrypted_filename)
            os.remove(f"{encrypted_filename[:-3]}.spec")
            shutil.rmtree('build')  
            print(f"\n[+] File Successfully Compiled and Encrypted in /dist/{encrypted_filename[:-3]}.exe.")
        except Exception as e:
            print("\n[!] Failed to compile the payload.")
            print(f"Error: {e}")
    elif compile_option == "no":
        num_keys = random.randint(2, 5)
        keys = [random_key(len(contents)) for _ in range(num_keys)]

        var_name = [random_var() for _ in range(6)]
        encrypted_filename = random_file()

        output_string = contents
        for key in keys:
            output_string = "".join(chr(ord(s) ^ ord(k)) for s, k in zip(output_string, key))

        try:
            with open(encrypted_filename, 'w') as f:
                f.write(f'{var_name[1]} = ' + repr(output_string) + '\n')
                f.write(f'{var_name[2]} = ' + repr(keys) + '\n')
                f.write(
                    f'{var_name[3]} = len({var_name[1]})\n'
                    f'{var_name[4]} = {var_name[1]}\n'
                    f'for {var_name[5]} in {var_name[2]}:\n'
                    f'    {var_name[4]} = "".join(chr(ord(s) ^ ord(k)) for s, k in zip({var_name[4]}, {var_name[5]}))\n'
                    '\n'
                    f'exec({var_name[4]})'
                )
        except FileNotFoundError:
            print("\n[!] Failed to create encrypted file.")
            return

        print(f"\n[+] File Successfully Encrypted as '{encrypted_filename}'.")
    else:
        print("\n[!] Invalid input. Please enter 'yes' or 'no'.")
        return

def random_key(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def random_var(length=8):
    characters = string.ascii_letters
    return ''.join(secrets.choice(characters) for _ in range(length))

def random_file():
    length = 10
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length)) + '.py'

if __name__ == "__main__":
    main()
