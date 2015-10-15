# historical_ciphers
Python library for encrypting, decrypting, and hacking historical ciphers. At the moment there are classes implemented for Caesar, Transposition, and Affine ciphers. More to come.

This library draws heavily from Al Sweigart's book [<i>Hacking Secret Ciphers with Python</i>](https://inventwithpython.com/hacking/). 

## Classes
Each of the classes in this module are (so far) subclasses of the Cipher class, and inherit its __init__ method and base parameters: message, ciphertext, and key. The base class also includes empty .encrypt() and .decryt methods(), but those are present only to allow the inherited __init__ methods of subclasses to automatically encrypt/decrypt a ciphertext/message if a key and a message/ciphertext are provided. So

    a_caesar_cipher = Caesar('This is a secret message', key = 9)
    print(a_caesar_cipher.ciphertext)

will not raise an Attribute Error.

## Hacking
The hack methods for each subclass of Cipher rely on programmatic detection of a language. At the moment, this is done by loading the dictionary file that was distributed with <i>Hacking Secret Ciphers with Python</i>, but that can be easily adjusted by passing a filename to the global-level load_dictionary() function. I tried to keep the name of the is_langage() function language agnostic (even though the semantics of the code is English... but them's the breaks).

## Unit Testing
I've started building a comprehensive unit test script, for kicks. It currently runs through defined key values for Caesar, Transposition, and Affine ciphers; a defined range of keys and 1000 random keys for Caesar; up to the range of len(message)/2 for Transposition; and 1000 random keys for Affine.

In order to expand possible inputs or randomness for tests, I will need to write ways to handle exceptions to the expected input for each attribute. Also on the agenda are tests for the autogeneration of attributes on object instantiation/construction.

## Future Plans
I plan to try sending hack attempts to Polyglot, to see if I can get the program to automatically detect language without a dictionary file, and to see how many false positives would result.
