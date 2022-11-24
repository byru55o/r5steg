# r5steg
Text in text steganography program using zero width space characters.

# Usage
- Make sure you meet all the [requirements](https://github.com/byru55o/r5steg#requirements), if not install them with [**pip**](https://pypi.org/project/pip/)
- Execute `main.py`: `python3 main.py` or `./main.py`


# Under development
This piece of free software is currently on BETA phase, feel free to report any bugs or contribute with a PR!
### To do list:
- ~~Support decoding multiple messages at once~~
- ~~Add compression~~ (characters used are listed below)
- Add encryption with passwords
### ZW characters used:
characters to be used in the future are marked with [*]
- `U+2060 \xe2\x81\xa0	WORD JOINER` for '0'
- `U+200B \xe2\x80\x8b	ZERO WIDTH SPACE` for '1'
- `U+200D \xe2\x80\x8d	ZERO WIDTH JOINER` for '2'
- `U+200E \xe2\x80\x8e	LEFT-TO-RIGHT MARK` for '3'
- `U+200F \xe2\x80\x8f	RIGHT-TO-LEFT MARK` for '4'
- `U+200C \xe2\x80\x8c	ZERO WIDTH NON-JOINER` for '5'
- `U+2061 \xe2\x81\xa1 FUNCTION APPLICATION` for '6'
- `U+180E \xe1\xa0\x8e MONGOLIAN VOWEL SEPARATOR` for '7'
- `U+202A \xe2\x80\xaa LEFT-TO-RIGHT EMBEDDING` for '8'
- `U+202C \xe2\x80\xac POP DIRECTIONAL FORMATTING` for '9'
- `U+202D \xe2\x80\xad LEFT-TO-RIGHT OVERRIDE` for 'a'
- `U+2062 \xe2\x81\xa2 INVISIBLE TIMES` for 'b'
- `U+2063⁣ \xe2\x81\xa3 INVISIBLE SEPARATOR` for 'c'
- `U+2064 \xe2\x81\xa4 INVISIBLE PLUS` for 'd'
- `U+2065 \xe2\x81\xa5 Undefined` for 'e'
- `U+2066 \xe2\x81\xa6 LEFT-TO-RIGHT ISOLATE` for 'f'
- `U+FEFF \xef\xbb\xbf  ZERO WIDTH NO-BREAK SPACE` for wrapping
### Feedback
Im up to any kind of feedback!

# Requirements
- **Python 3** (3.10.8 was used but should work with any)
- [**pyperclip**](https://pyperclip.readthedocs.io/en/latest/) for auto copy-to-clipboard.
- [**readline**](https://docs.python.org/3/library/readline.html) for input usability.
