# GUI version for r5steg
Try the [demo](https://r5steg.vspmail.net/r5steg).
___
# Host r5steg web-app at home:
- Make sure you meet all the [requirements](https://github.com/byru55o/r5steg/tree/GUI-web-app#requirements)
- Clone the repository and navigate to it's directory:
  ```bash
  git clone https://github.com/byru55o/r5steg.git && cd r5steg
  ```
- Run the program with python3:
  ```bash
  python3 webapp.py
  ```
- Navigate to [127.0.0.1:3443/r5steg](http://127.0.0.1:3443/r5steg) on your browser.
___  
## Usage
- Change the settings according to your needs, you can turn off encryption and change the **salt**, [which is highly recommended](https://github.com/byru55o/r5steg/tree/GUI-web-app#to-change-the-salt)!
- To encrypt and hide a message: select **[HIDE]** mode, enter message to hide in the textarea at the bottom,
  enter the plain text you want to show at the top and the password for the encryption.
  Finally, press the **ENCRYPT AND HIDE** button. The resulting string,
  which is copied to the clipboard and added to the history (located in the left drawer)
  contains your secret message, which you can decrypt using mode **[UNHIDE]**.
- To decrypt and unhide a message in between plain text: select option **[UNHIDE]**, enter the message and the password,
  and press the **UNHIDE AND DECRYPT**

# Requirements
- **Python 3** (3.10.8 was used but should work with any)
- [**binascii**](https://docs.python.org/3/library/binascii.html) for ASCII character support when encoding.
- [**pycryptodome**](https://www.pycryptodome.org/) for encryption.
- [**scrypt**](https://pypi.org/project/scrypt/) for key derivation.

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
- Find the salt input box in the settings:
![salt](https://github.com/byru55o/r5steg/blob/GUI-web-app/salt.png)
- Replace its value with a random string (e.g. generating a random UUID):
```python
python3
>>> from uuid import uuid4
>>> print(str(uuid4()))
36deac9e-b01e-4cf6-be2b-f3f1c63e4851
```
- Remember to store the salt safely, as it is required for the decryption of your message.
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
