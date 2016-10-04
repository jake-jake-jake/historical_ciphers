import unittest
import random
from historical_ciphers import *

test_message = """This is the default test_message that I am using to run 
             through unit tests. It is plain. It is boring. 
             But it does have all the letters:
             ABCDEFGHIJKLMNOPQRSTUVWXYZ plus
             abcdefghijklmnopqrstuvwxyz;
             and some nums:
             1234567890;
             and even some punctution:
             ~!@#$%^&*()_+=-`{}|:<>?'\" <>?,./=/*."""


class DefaultTests(unittest.TestCase):
    ''' Test to see if automatic encryption works. I have defaulted to a key
        of 8 for Caesar and Transposition. For the Affine, I am using 3399,
        which was the first that was generated by Affine.get_key() when I
        started writing this unittest script.'''
    def test_Caesar_key_8(self):
        caesar_test = Caesar(test_message, key=8)
        self.assertEqual(caesar_test.decrypt(), test_message.upper())

    def test_Transposition_key_8(self):
        transposition_test = Transposition(test_message, key=8)
        self.assertEqual(transposition_test.decrypt(), test_message)

    def test_Affine_key_3399(self):
        affine_test = Affine(test_message, key=3399)
        self.assertEqual(affine_test.decrypt(), test_message)

    def test_Substitution_set_key(self):
        set_key = '''D}>lsNKW@\t=\'z*LGE&wqJv6!(F{a2_~[y,C0h\x0brITXpnV-ZSeM#`8gf"1Qxm<;%B$R\n/9Pkt34A|dH:ou)^\x0cU\\Oi7 +.cbj5\rY]?'''
        substitution_test = Substitution(test_message, key=set_key)
        self.assertEqual(substitution_test.decrypt(), test_message)


class Caesar_cipher_range_keys(unittest.TestCase):
    ''' Test the Caesar cipher with keys in range of len(LETTERS).'''

    def test_Caesar_range_keys(self):
        ''' Caesar.encrypt() treats key = 0 as None and so does not encrypt;
            range for this test must begin at 1.'''
        for test_key in range(1, len(Caesar.LETTERS)):
            caesar_test = Caesar(test_message, key=test_key)
            self.assertEqual(caesar_test.decrypt(), test_message.upper())


class Caesar_cipher_rand_keys(unittest.TestCase):
    ''' Test the Caesar cipher with random keys. '''

    def test_Caesar_rand_keys(self):
        ''' Caesar.encrypt() treats key = 0 as None and so does not encrypt;
            range for this test must begin at 1.'''
        for test in range(0, 1000):
            test_key = random.randint(1, 1000)
            caesar_test = Caesar(test_message, key=test_key)
            self.assertEqual(caesar_test.decrypt(), test_message.upper())


class Transposition_cipher_range_keys(unittest.TestCase):
    ''' Test Transposition cipher with keys in range of len(test_message). '''

    def test_Transposition_range_keys(self):
        ''' Transposition class does not encrypt if key is set to
            greater than half the length of the plaintext message.
            This may be behavior to force to raise an exception
            rather than leaving ciphertext as None. '''
        for test_key in range(1, int(len(test_message) / 2)):
            transposition_test = Transposition(test_message, key=test_key)
            self.assertEqual(transposition_test.decrypt(), test_message)


class Affine_cipher_rand_test(unittest.TestCase):
    ''' Test the Affine cipher with 1000 random keys. '''

    def test_Affine_rand_keys(self):
        for _ in range(1000):
            test_str = 'Test Affine cipher with 1000 random keys.'
            affine_test = Affine(test_str)
            affine_test.get_key()
            affine_test.ciphertext = affine_test.encrypt()
            self.assertEqual(affine_test.decrypt(), test_str)


class Substitution_cipher_rand_test(unittest.TestCase):
    ''' Test the Substitution cipher with 1000 random keys. '''
    def test_Substitution_rand_keys(self):
        for _ in range(1000):
            substitution_test = Substitution(test_message)
            substitution_test.key = substitution_test.gen_key()
            substitution_test.ciphertext = substitution_test.encrypt()
            self.assertEqual(substitution_test.decrypt(), test_message)

if __name__ == '__main__':
    unittest.main()
