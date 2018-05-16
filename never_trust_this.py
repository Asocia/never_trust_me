from operator import xor

try:
    import pyperclip

    pyperclip_imported = True
except ImportError:
    pyperclip_imported = False
    pyperclip = None

from random import randint, shuffle, choice
import sys
import os
from time import sleep
import textwrap
import locale


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


def spin(a, b):
    spinner = spinning_cursor()
    for _ in range(a):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sleep(b)
        sys.stdout.write('\b')
    print("  ")


def open_lang_file(lang):
    prompts_ = dict()
    path = os.sep.join(('languages', lang))
    with open(path, 'r', encoding='utf8') as f:
        for line in f.readlines():
            name, description = line.split(':', 1)
            prompts_[name] = description[:-1]  # Ignore '\n' character.
    return prompts_


def get_prompts():
    try:
        language = locale.getdefaultlocale()[0]
        prmpts = open_lang_file(language)
        print(prmpts['primary_lang_info'] + "\n" + prmpts['secondary_lang_info'], end='')
        change_language_query = input()
        if change_language_query in ('l', 'L'):
            language = 'en_US' if language != 'en_US' else 'tr_TR'
            prmpts = open_lang_file(language)
            print(prmpts['lang_set_to'])
    except FileNotFoundError:
        q = input(
            "We don't have support for your language. "
            "Please choose a language: [1] for English, [2] for Turkish >> ")
        while q not in ('1', '2'):
            q = input("Unknown command. Please press [1] or [2] >> ")
        if q == '1':
            language = "en_US"
        else:
            language = "tr_TR"
        prmpts = open_lang_file(language)
        print(prmpts['lang_set_to'])
    finally:
        return prmpts


class VerySecureCipherApp():
    def __init__(self):
        self.character_groups = {'α': 'ωDXşpy`ZrüΣ~]UEK',
                                 'φ': 'πWQG-%B1#ß4V5Ş≤Ω',
                                 '2': 'Ö07OAz_ÜαjxλLĞ;e',
                                 'W': 'v$÷|6n<=öi/.çT89',
                                 '&': '\\t&[dH₺uØ^aw®I>Ρ',
                                 '%': 'İPΔY*qφ,m)}≥b€ÇR',
                                 '6': '3oJ+NC(≡flğ©\':!β',
                                 '?': 'ıMh2{FgS£@sk?"c '
                                 }
        self.char_arrangement = list(self.character_groups.keys())
        self.characters = ''
        self.character_table = dict()
        self.new_char_arrangement()

    def new_char_arrangement(self):
        shuffle(self.char_arrangement)
        self.arrange_characters()

    def arrange_characters(self):
        self.characters = ''
        for key in self.char_arrangement:
            self.characters += self.character_groups[key]
        self.character_table = {b: a for a, b in enumerate(self.characters)}

    def random_str(self, length, min_char=0, max_char=127):
        r = ''
        for i in range(length):
            r += self.character_table[self.get_char(randint(min_char, max_char))]
        return r

    def encrypt(self, text, key):
        self.new_char_arrangement()
        text = self.replace_unknown_chars(text, '?')
        key = self.replace_unknown_chars(key,'φ')
        # print("text:", text)
        key = self.stretch(key, len(text))
        # print("key_str", key)
        encrypted_text = self.xorr(text, key)
        encrypted_text = self.shift('rigth', encrypted_text)
        cipher = "".join(self.char_arrangement[:4]) + encrypted_text + "".join(
            self.char_arrangement[4:])
        return cipher

    def decrypt(self, cipher, key):
        self.char_arrangement = list(cipher[:4] + cipher[-4:])
        self.arrange_characters()
        key = self.stretch(key, len(cipher))
        encrypted_text = cipher[4:-4]
        encrypted_text = self.shift('left', encrypted_text)
        text = self.xorr(encrypted_text, key)
        return text

    def replace_unknown_chars(self, string, r):
        for j in range(len(string)):
            if string[j] not in self.character_table.keys():
                string = string[:j] + r + string[j + 1:]
        return string

    def stretch(self, string, length):
        string = (length // len(string)) * string + string[:length % len(string)]
        return string

    def xorr(self, string, key):
        r = ''
        for i in range(len(string)):
            letter_num = self.get_index(string[i])
            # print('letter num:',letter_num)
            key_num = self.get_index(key[i])
            # print('key num:',key_num)
            xor_value = xor(letter_num, key_num)
            # print('xor value:',xor_value)
            r += self.get_char(xor_value)
            # print('r:', r)
        return r

    def shift(self, direction, string):
        r = ''
        if direction == 'rigth':
            for i in range(len(string)):
                r += self.get_char((self.get_index(string[i]) + i) % len(self.characters))
        elif direction == 'left':
            for i in range(len(string)):
                r += self.get_char((self.get_index(string[i]) - i) % len(self.characters))
        else:
            raise Exception('Direction value either should be [left] or [right] not [{}].'.format(direction))
        return r

    def get_index(self, char):
        return self.character_table[char]

    def get_char(self, index):
        for key, value in self.character_table.items():
            if value == index:
                return key


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
                if pyperclip_imported:
                    try:
                        pyperclip.copy(cipher)
                        sleep(1)
                        print("\n" + prompts['copied_to_clipboard'] + "\n")
                    except:
                        if os.name == 'posix':
                            print(prompts['pyperclip_err'])
            except Exception as e:
                sleep(1.5)
                print(
                    "\n" + prompts['failed_encryption'])
                sleep(1.5)
                # print(e)
            finally:
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
            except Exception as e:
                sleep(1.5)
                print("\n" + prompts['failed_decryption'])
                sleep(1.5)
                # print(e)
            finally:
                print("-" * 70)
                sleep(1.5)
        elif q == 'q':
            if not pyperclip_imported:
                print(prompts['install_pyperclip'])
            print("\n" + prompts['exit'])
            sleep(2)
            exit()
        else:
            sleep(0.25)
            print("\n" + prompts['unknown_op'])
        sleep(1.25)
        print()
