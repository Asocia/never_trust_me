from operator import xor
from random import randint, shuffle


class VerySecureCipherApp:
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
        self.char_arrangement = list(self.character_groups.keys())
        shuffle(self.char_arrangement)
        self.arrange_characters()

    def arrange_characters(self):
        self.characters = ''
        for key in self.char_arrangement:
            self.characters += self.character_groups[key]
        self.character_table = {b: a for a, b in enumerate(self.characters)}

    def encrypt(self, text, key):
        self.new_char_arrangement()
        text = self.replace_unknown_chars(text, '?')
        key = self.replace_unknown_chars(key, 'φ')
        key = self.stretch(key, len(text))
        encrypted_text = self.xorr(text, key)
        encrypted_text = self.shift('right', encrypted_text)
        cipher = "".join(self.char_arrangement[:4]) + encrypted_text + "".join(
            self.char_arrangement[4:])
        return cipher

    def decrypt(self, cipher, key):
        self.char_arrangement = list(cipher[:4] + cipher[-4:])
        self.arrange_characters()
        key = self.replace_unknown_chars(key, 'φ')
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

    @classmethod
    def stretch(cls, string, length):
        string = (length // len(string)) * string + string[:length % len(string)]
        return string

    def xorr(self, string, key):
        r = ''
        for i in range(len(string)):
            string_index = self.get_index(string[i])
            key_index = self.get_index(key[i])
            xor_value = xor(string_index, key_index)
            r += self.get_char_from_value(xor_value)
        return r

    def shift(self, direction, string):
        r = ''
        if direction == 'right':
            for i in range(len(string)):
                r += self.get_char_from_value((self.get_index(string[i]) + i) % len(self.characters))
        elif direction == 'left':
            for i in range(len(string)):
                r += self.get_char_from_value((self.get_index(string[i]) - i) % len(self.characters))
        else:
            raise Exception("Direction value either should be 'left' or 'right' not '{}'.".format(direction))
        return r

    def get_index(self, char):
        return self.character_table[char]

    def get_char_from_value(self, index):
        for key, value in self.character_table.items():
            if value == index:
                return key

    def random_str(self, length, min_char=0, max_char=127): # This function has nothing to do with this app
        r = ''                                                      # but you might want to use it.
        for i in range(length):
            r += self.character_table[self.get_char_from_value(randint(min_char, max_char))]
        return r
