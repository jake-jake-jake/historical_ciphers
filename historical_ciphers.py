# Classes for historical, insecure ciphers. Have fun.
# IRGYYKY LUX NOYZUXOIGR, OTYKIAXK IOVNKXY. NGBK LAT.

# Inspired by Hacking Secret Ciphers with Python: http://inventwithpython.com/hacking

import math, string, random

# Functions for multiplicative/Affine cipher.
# Calculates greatest common denominator; uses Euclid's algorithm. In Python 3.5
# this would be redundant, since .gcd() is a math method, and math is imported.
def gcd(a, b):
    ''' Return greatest common denominator.'''
    while a != 0:
        a, b = b % a, a
    return b

# Calculates modular inverse of two numbers; uses Euclid's extended algorithm.
# 
def mod_inverse(a, m):
    ''' Return modular inverse of two ints.'''
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m



# Loads a dictionary to check cipher hacks against. In the main() function, defaults to
# loading the dictionary.txt provided with Hacking Ciphers with Python
def load_dictionary(file_name = None):
    ''' Loads a dictionary file. Defaults to 'dictionary.txt' provided by Al 
        Sweigart in his python hacking book. 
    '''
    dict_name = file_name or 'dictionary.txt'
    dict_words = {}
    with open(dict_name) as fo:      # Loads dictionary file
        for word in fo.read().split('\n'):
            dict_words[word] = None
    return dict_words



# The following four functions are used to clean an input to see if it is English.
# Eventually I will replace with polyglot integration to expand language functionality.
def is_language(string, dictionary, word_percentage = 20, letter_percentage = 85):
    ''' Checks if string is a language by comparing words in string with
        loaded dictionary. Returns true if given percentage of word matches 
        and letters in string is high enough. Default values: word_percentage
        is 20 and letter_percentage is 85.
    '''
    word_match = (get_dictionary_percentage(string, dictionary) * 100) >= word_percentage
    sufficient_letters = (len(strip_string(string))/len(string) * 100) >= letter_percentage
    return word_match and sufficient_letters

def strip_string(string):
    ''' Removes nonalphabetic characters from string, preserving spaces.
    '''
    stripped_string = [char for char in string if char.isalpha() or char in ' \t\n']
    return ''.join(stripped_string)

def get_dictionary_percentage(string, dictionary):
    ''' Returns a float conveying percentage of dictionary words in 
        string, from 0.0 to 1.0.
    '''
    word_list = strip_string(string).split()
    if word_list == []:
        return 0.0

    dictionary_words = 0
    for word in word_list:
        if word.upper() in dictionary:
            dictionary_words += 1
    return float(dictionary_words/len(word_list))



# Cipher classes follow. The base Cipher class initializes a message,
# ciphertext, and key. If the key is known, it automatically produces
# a ciphertext or plaintext from .encrypt()/.decrypt() class methods.
# This behavior is inherited by all Cipher subclasses.
class Cipher:
    ''' Creates class with standard cipher attributes: message,
        ciphertext, and key. Used to initialize all other cipher
        classes.
    '''
    def __init__(self, message = '', ciphertext = '', key = None):
        '''Defaults to empty values.'''
        self.message = message
        self.ciphertext = ciphertext
        self.key = key
        # Autopopulate message or ciphertext if either and key present.
        if self.message and self.key:
            self.ciphertext = self.encrypt(passed_key = self.key)
        elif self.ciphertext and self.key:
            self.message = self.decrypt(passed_key = self.key)

    def decrypt(self, ciphertext = None, passed_key = None):
        ''' This is a placeholder method. It returns None. '''
        return None

    def encrypt(self, plaintext = None, passed_key = None):
        ''' This is a placeholder method. It returns None. '''
        return None

class Caesar(Cipher):
    ''' Carries encryption and decryption methods for Caesar ciphers.
        The character set is limited to unadorned Latin. All letters majuscule
        for historical flavor. Extended Latin character set ignored. A function
        to reduce diacritically marked characters to vanilla A to Z would be useful.
    '''
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' # Letterspace for Caesar Ciphers
                                           # To make this work with extended latin
                                           # may take some doing

    def decrypt(self, ciphertext = None, passed_key = None):
        ''' Decrypts ciphertext; defaults to self.key and self.ciphertext if neither is passed.'''
        key = passed_key or self.key
        ciphertext = ciphertext or self.ciphertext
        while key:
            message = []
            for char in ciphertext.upper():
                if char in self.LETTERS:
                    index = self.LETTERS.find(char)
                    index -= key
                    if index >= len(self.LETTERS) or index < 0:
                        index = abs(index % len(self.LETTERS))
                    message.append(self.LETTERS[index])
                else:
                    message.append(char)
            return ''.join(message)
        else:
            print('Cannot decrypt without key. Set key or use .hack().')


    def encrypt(self, plaintext = None, passed_key = None):
        ''' Encrypts ciphertext; defaults to self.key and self.message if neither is passed.'''
        key = passed_key or self.key
        message = plaintext or self.message
        while key:
            ciphertext = []
            for char in message.upper():
                if char in self.LETTERS:
                    index = self.LETTERS.find(char)
                    index += key
                    if index >= len(self.LETTERS):
                        index = index % len(self.LETTERS)
                    ciphertext.append(self.LETTERS[index])
                else:
                    ciphertext.append(char)
            return ''.join(ciphertext)
        else:
            print('You must set key to encrypt. ')

    def hack(self):
        ''' Runs through all possible encrypt(key) possibilities; prints results. '''
        if len(self.ciphertext) < 1:
            raise AttributeError('There is no ciphertext. ')
        else:
            possible_match = False
            print('Attempting hack of Caesar cipher...')
            for key in range(1, len(self.LETTERS)):
                attempt = self.decrypt(key)
                if is_language(attempt, english_dict):
                    possible_match = True
                    print('Possible match with key {}:\n{}'.format(key, self.decrypt(key)))
            if not possible_match: print('Unable to find possible match.')

class Transposition(Cipher):
    ''' Carries encryption and decryption methods for Transposition cipher. '''
    def encrypt(self, plaintext = None, passed_key = None):
        ''' Encrypts message attribute for transposition cipher; defaults
            to self.key if None passed. '''
        key = passed_key or self.key
        message = plaintext or self.message
        while key < (len(message)/2):
            ciphergrid = [''] * key
            for col in range(0, key):
                index = col
                while index < len(message):
                    ciphergrid[col] += message[index]
                    index += key
            return ''.join(ciphergrid)
        else:
            print('Set a key value less than half message length.')

    def decrypt(self, ciphertext = None, passed_key = None):
        ''' Decrypts ciphertext attribute for Transposition cipher; defaults
            to self.key if None passed. '''
        key = passed_key or self.key
        ciphertext = ciphertext or self.ciphertext
        while key:
            # This is a bit counter intuitive; I suggest reading Sweigart's chapter.
            decrypt_cols = math.ceil(len(ciphertext)/key)
            decrypt_rows = key
            decrypt_grid = [''] * decrypt_cols
            empty_boxes = decrypt_cols * decrypt_rows - len(ciphertext)
            row = 0
            col = 0
            for char in ciphertext:
                decrypt_grid[col] += char
                col += 1
                if col == decrypt_cols or (col == decrypt_cols - 1 and row >= decrypt_rows - empty_boxes):
                    row += 1
                    col = 0
            return ''.join(decrypt_grid)    

        else:
            print('Cannot decrypt without key. Set key or use .hack().')

    def hack(self):
        ''' Runs through all possible encrypt(key) possibilities; prints results. '''
        if len(self.ciphertext) < 1:
            raise AttributeError('There is no ciphertext. ')
        else:
            for key in range(1, len(self.message)):
                attempt = self.decrypt(key)
                if is_language(attempt, english_dict):
                    possible_match = True
                    print('Possible match with key {}:\n{}'.format(key, self.decrypt(key)))
            if not possible_match: print('Unable to find possible match.')

class Affine(Cipher):
    ''' Carries encryption and decryption methods for Affine ciphers, as well as
        a key generator and checker. '''
    CHARS = string.printable
    
    def get_key(self):
        ''' Checks if a key is present. If not, calls gen_key() and sets self.key equal to result.
            If so, asks for confirmation first.'''
        if self.key:
            print('Key already present: {}. Overwrite? Y/n'.format(self.key))
            key_confirmation = input('> ')
            if key_confirmation.strip().upper().startswith('Y'):
                self.key = self.gen_key()
        else:
            self.key = self.gen_key()

    def gen_key(self):
        ''' Generates key for the affine cipher.'''
        while True:
            mult_key = random.randint(2, len(self.CHARS))
            add_key = random.randint(1, len(self.CHARS) - 1)
            if gcd(mult_key, len(self.CHARS)) == 1:
                return mult_key * len(self.CHARS) + add_key

    def split_key(self, key):
        ''' Splits single key into one multiplication and one additive int.'''
        return divmod(key, len(self.CHARS))

    def encrypt(self, plaintext = None, passed_key = None):
        ''' Encrypts message attribute for Affine cipher; defaults
            to self.key, self.message if None passed.
        '''
        message = plaintext or self.message
        key = passed_key or self.key
        ciphertext = [] 
        while key:
            key = self.split_key(key)
            for char in message:
                if char in self.CHARS:
                    index = self.CHARS.find(char)
                    ciphertext.append(self.CHARS[(index * key[0] + key[1]) % len(self.CHARS)])
                else:
                    ciphertext.append(char)
            return ''.join(ciphertext)
        else:
            print('Cannot encrypt without key.')

    def decrypt(self, ciphertext = None, passed_key = None):
        ''' Decrypts message for Affine cipher; defaults to self.key,
            self.ciphertext if None passed.
        '''
        ciphertext = ciphertext or self.ciphertext
        key = passed_key or self.key 
        plaintext = []
        while key:
            key = self.split_key(key)
            inverse_key = mod_inverse(key[0], len(self.CHARS))
            for char in ciphertext:
                if char in self.CHARS:
                    index = self.CHARS.find(char)
                    plaintext.append(self.CHARS[(index - key[1]) * inverse_key % len(self.CHARS)])
                else:
                    plaintext.append(char)    
            return ''.join(plaintext)
        else:
            print('Cannot decrypt without key. Set key or use .hack().')

    def hack(self):
        ''' Runs through all possible encrypt(key) possibilities; prints results.'''
        print('Attempting to hack Affine cipher. ')
        while self.ciphertext:
            possible_match = False
            for key in range(len(self.CHARS) ** 2):
                key_check = self.split_key(key)
                # Insert progress if cond. here that prints a percentage complete as
                # attempt is made; roughly 'if key % (len(self.CHARS) ** 2 / 10 == 0)'
                if gcd(key_check[0], len(self.CHARS)) != 1:
                    continue
                attempt = self.decrypt(passed_key = key)
                if is_language(attempt, english_dict):
                    possible_match = True
                    print('Possible match with key {}:\n{}'.format(key, attempt[:140]))
            if not possible_match:
                print('Unable to find possible match.')
                break
        else: print('There is no ciphertext.')


class Substitution(Cipher):
    ''' Contains encrypt, decrypt, and key gen methods for the Substitution cipher.
        Can work as a poor man's (that is, insecure) one-time pad. There is no hack
        method for this Cipher class, since hack methods will be indeterminate. '''
    CHARS = string.printable

    def gen_key(self):
        ''' Returns a key as string equal to the character set (self.CHARS) of the
            cipher. '''
        key_popper = list(self.CHARS)
        key_array = [key_popper.pop(random.randint(0, len(key_popper) - 1)) \
                     for _ in range(len(self.CHARS))]
        return ''.join(key_array)
        
    def encrypt(self, plaintext = None, passed_key = None):
        ''' Encrypts using key. If no key set, raises AttributeError. '''
        plaintext = plaintext or self.message
        key = passed_key or self.key
        while key:
            ciphertext = []
            for char in plaintext:
                if char in self.CHARS:
                    ciphertext.append(key[self.CHARS.find(char)])
                else:
                    ciphertext.append(char)
            return ''.join(ciphertext)
        else:
            raise AttributeError('Cannot encrypt without key. Use gen_key method to generate key. ')

    def decrypt(self, ciphertext = None, passed_key = None):
        ''' Encrypts using key. If no key set, raises AttributeError. '''
        ciphertext = ciphertext or self.ciphertext
        key = passed_key or self.key
        while key:
            plaintext = []
            for char in ciphertext:
                if char in self.CHARS:
                    plaintext.append(self.CHARS[key.find(char)])
                else:
                    plaintext.append(char)
            return ''.join(plaintext)
        else:
            raise AttributeError('Cannot decripty without key. Use gen_key method to generate key. ')
            
class Vegenere(Cipher):
    ''' Contains encrypt and decrypt methods for the Vegenère cipher. '''
    self.CHARS = string.printable
    
    def encrypt(self, plaintext = None, passed_key = None):
        ''' Returns ciphertext from plaintext parameter, using instance key and CHAR attributes.'''
        ct, abc = [], self.CHARS    # ciphertext and alphabet
        key = passed_key or self.key
        plaintext = plaintext or self.message
        if not key:
            raise AttributeError('Key needed to encrypt.')
        cm = zip(plaintext, cycle(key))   # ciphermatrix
        for char, key_char in cm:
            if char in abc:
                ct.append(abc[(abc.find(char) + abc.find(key_char)) % len(abc)])
            else:
                ct.append(char)
        return ''.join(ct)

    def decrypt(self, ciphertext = None, passed_key = None):
        ''' Returns plaintext from ciphertext parameter, using instance key and CHAR attributes.'''
        pt, abc = [], self.CHARS   # plaintext and alphabet
        key = passed_key or self.key
        ciphertext = ciphertext or self.ciphertext
        if not key:
            raise AttributeError('Key needed to decrypt.')
        cm = zip(ciphertext, cycle(key))
        for char, key_char in cm:
            if char in abc:
                pt.append(abc[(abc.find(char) - abc.find(key_char)) % len(abc)])
            else:
                pt.append(char)
        return ''.join(pt)
    
# The main loop
if __name__ == '__main__':
    print('''This library currently encrypts, decrypts, and hacks
             Caesar, Transposition, and Affine ciphers. Encryption
             and decryption methods are available for Substitution
             and Vegenère (Vegenere) ciphers.''')
    english_dict = load_dictionary()
