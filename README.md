# r5steg ![License](https://img.shields.io/github/license/byru55o/r5steg "License") ![Contributors](https://img.shields.io/github/contributors/byru55o/r5steg "Contributors") ![Size](https://img.shields.io/github/repo-size/byru55o/r5steg "Size")
Encrypted text in text steganography program using zero width space characters.
It hides and encrypts a message in between plain text using zero-width characters which are invisible in most browsers and interfaces.
# [GUI version for r5steg](https://github.com/byru55o/r5steg/tree/GUI-web-app)
Try the [demo](https://r5steg.vspmail.net/page_layout).
___
## Installation
- Make sure you meet all the [requirements](https://github.com/byru55o/r5steg#requirements), if not install them with [**pip**](https://pypi.org/project/pip/)
- Clone the repository and navigate to it's directory:
  ```bash
  git clone https://github.com/byru55o/r5steg.git && cd r5steg
  ```
- Install it with GNU make:
  ```bash
  sudo make install
  ```
  or to uninstall:
```sudo make uninstall```
  
## Usage
- Execute the program: `r5steg` or, if you didn't install: `./r5steg.py` or `python3 r5steg.py`
- To encrypt and hide a message: select option **[1]**, enter message to hide,
  enter the plain text you want to show and the password for the encryption. The resulting string,
  which is copied to the clipboard contains your secret message which you can decrypt using option **[2]**.
- To decrypt and unhide a message in between plain text: select option **[2]**, enter the message and the password.

### Configuration
**It is possible to change some options** such as encryption (some of you may prefer to disable it, for a shorter/lighter hidden message) or colours (you can either disable or modify them).
The configuration file is located in `~/.config/r5steg/config.ini`. I suggest copying the provided `example_config.ini` with this command:
```bash
mkdir -p ~/.config/r5steg && cp example_config.ini ~/.config/r5steg/config.ini
```
More options are going to be added in the future: choosing binary (or other bases) or changing the zero-width characters in the config file are some examples from the top of my head!

# Requirements
- **Python 3** (3.10.8 was used but should work with any)
- [**pyperclip**](https://pyperclip.readthedocs.io/en/latest/) for auto copy-to-clipboard.
- [**readline**](https://docs.python.org/3/library/readline.html) for input usability.
- [**binascii**](https://docs.python.org/3/library/binascii.html) for ASCII character support when encoding.
- [**pycryptodome**](https://www.pycryptodome.org/) for encryption.
- [**scrypt**](https://pypi.org/project/scrypt/) for key derivation.
- [**gettext**](https://pypi.org/project/python-gettext/) for the translations.
- [**configparser**](https://docs.python.org/3/library/configparser.html) for configuration files.
- [**pathlib**](https://docs.python.org/3/library/pathlib.html) for better path-handling.

# How does it work?
First of all, the message is encrypted:

### AES in GCM mode:
- The key is derived using the password and salt
- The IV or nonce is randomized on each encryption and stored alongside the cipher text

Using the key and the initial vector, the plain text becomes cipher text.
The salt **is not** transferred with the ciphertext, so it has to be a fixed value (I used random bytes).
That's why, for optimal security, it should be changed and stored safely,
because it has to remain the same value encrypting and decrypting.

#### To change the salt:
- Find the salt variable at the beginning of the code:
```python
salt = b'\xdc\xebh\x132\x7f\x8cD\xb1U\x1bI\xfa\x1d/i'
```
- Replace its value with 16 different random bytes (e.g., using urandom function):
```python
python3
>>> import os
>>> os.urandom(16)
b'\xfaFp6\x0e[\x9e\x9dKM\x80^O\x99\x92\xf9'
```
After the encryption, the message looks like this: `f6989326b5198f881e634da623f1af5e2a632540`.  
The first 32 hex. characters represent the initial vector used, the rest represent the ciphertext,
which weights the same as the secret message.
This hex code is later hidden using the following zero width unicode characters:

### Characters used:
| Unicode code point | UTF-8 (in literal) | Name | hex to replace |
| --- | --- | --- | --- |
| U+2060 | \xe2\x81\xa0 | WORD JOINER | 0 |
| U+200B | \xe2\x80\x8b | ZERO WIDTH SPACE | 1 |
| U+200D | \xe2\x80\x8d | ZERO WIDTH JOINER | 2 |
| U+200E | \xe2\x80\x8e | LEFT-TO-RIGHT MARK | 3 |
| U+200F | \xe2\x80\x8f | RIGHT-TO-LEFT MARK | 4 |
| U+200C | \xe2\x80\x8c | ZERO WIDTH NON-JOINER | 5 |
| U+2061 | \xe2\x81\xa1 | FUNCTION APPLICATION | 6 |
| U+180E | \xe1\xa0\x8e | MONGOLIAN VOWEL SEPARATOR | 7 |
| U+202A | \xe2\x80\xaa | LEFT-TO-RIGHT EMBEDDING | 8 |
| U+202C | \xe2\x80\xac | POP DIRECTIONAL FORMATTING | 9 |
| U+202D | \xe2\x80\xad | LEFT-TO-RIGHT OVERRIDE | a |
| U+2062 | \xe2\x81\xa2 | INVISIBLE TIMES | b |
| U+2063 | \xe2\x81\xa3 | INVISIBLE SEPARATOR | c |
| U+2064 | \xe2\x81\xa4 | INVISIBLE PLUS | d |
| U+2065 | \xe2\x81\xa5 | Undefined | e |
| U+2066 | \xe2\x81\xa6 | LEFT-TO-RIGHT ISOLATE | f |
| U+FEFF | \xef\xbb\xbf | ZERO WIDTH NO-BREAK SPACE | [*]for wrapping

The last one in the table, is the *wrapper* character,
it's added at the beginning and at the end of the current hidden hex code.

#### Once the steganography is completed, the invisible characters are inserted in between the plain text and everything is copied to the clipboard.
The message can now be transferred securely without anyone to notice and, even if they notice,
it still cannot be decrypted without the password and salt!

## For the decryption:
The reversed process is applied, with the difference that it manages multiple messages at once, if they exist.
However, take in mind the same password and salt will be used for every message.
In case of failure the program will prompt the error for every message individually.

# Feedback
I'm up to any kind of feedback, questions, feature requests, etc.  
Just write [an email](mailto:r55@vspmail.net)!
