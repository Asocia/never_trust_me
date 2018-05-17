from cursor import spin
from language import get_prompts
from time import sleep
import os
import textwrap
from never_trust_this import VerySecureCipherApp
try:
    import pyperclip
except ImportError:
    pyperclip = None

if __name__ == '__main__':
    prompts = get_prompts()
    encoder = VerySecureCipherApp()
    while True:
        q = input(prompts['choice_dialog'])

        if q == "0":
            sleep(0.25)
            print("\n-" + "-" * 29 + prompts['choice_encrypt_text'] + "-" * 29 + "-\n")
            message = input(prompts['get_text_dialog'])
            key_ = input(prompts['get_key_dialog'])
            try:
                cipher = encoder.encrypt(message, key_)
                print("\n" + prompts['encrypting_msg'], end="")
                spin(26, 0.10)
                sleep(0.5)
                print("\n" + prompts['encrypted_msg'], cipher)
            except Exception as e:
                cipher = None
                sleep(0.75)
                print(
                    "\n" + prompts['failed_encryption'])
                sleep(0.75)
                print(e)
            if pyperclip is not None and cipher is not None:
                try:
                    pyperclip.copy(cipher)
                    sleep(1)
                    print("\n" + prompts['copied_to_clipboard'] + "\n")
                except:
                    if os.name == 'posix':
                        print(prompts['pyperclip_err_l'])
                    elif os.name == 'nt':
                        print(prompts['pyperclip_err_w'])
            print("-" * 70)
        elif q == "1":
            sleep(0.25)
            print("\n-" + "-" * 28 + prompts['choice_decrypt_text'] + "-" * 28 + "-\n")
            print(prompts['paste_from_clipboard'].format("Shift+" if os.name == 'posix' else "") + "\n")
            cipher = input(prompts['get_cipher_dialog'])
            key_ = input(prompts['get_key_dialog'])
            sleep(0.75)
            print("\n" + prompts['decrypting_msg'], end="")
            spin(26, 0.10)
            try:
                message = prompts['decrypted_msg'] + encoder.decrypt(cipher, key_) + "\n"
                sleep(0.75)
                print("\n" + prompts['decryption_successful'])
                sleep(0.75)
                print()
                print(textwrap.fill(message, 110))
            except:
                sleep(0.75)
                print("\n" + prompts['failed_decryption'])
                sleep(0.75)
            print("-" * 70)
            sleep(1.5)
        elif q == 'q':
            if pyperclip is None:
                print(prompts['install_pyperclip'])
                sleep(1)
            print("\n" + prompts['exit'])
            sleep(1.5)
            exit()
        else:
            sleep(0.25)
            print("\n" + prompts['unknown_op'])
        sleep(1.25)
        print()
