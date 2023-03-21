#!/usr/bin/env python3

import binascii, readline, pyperclip, scrypt, gettext
from Crypto.Cipher import AES
from configparser import ConfigParser
from pathlib import Path

t = gettext.translation(
    'r5steg',
    '/usr/share/locale/',
    fallback=True,
)
_ = t.gettext

parser = ConfigParser()
cfg_file = Path('~/.config/r5steg/config.ini').expanduser()

zwc = [
    b'\xe2\x81\xa0', b'\xe2\x80\x8b', b'\xe2\x80\x8d', b'\xe2\x80\x8e',
    b'\xe2\x80\x8f', b'\xe2\x80\x8c', b'\xe2\x81\xa1', b'\xe1\xa0\x8e',
    b'\xe2\x80\xaa', b'\xe2\x80\xac', b'\xe2\x80\xad', b'\xe2\x81\xa2',
    b'\xe2\x81\xa3', b'\xe2\x81\xa4', b'\xe2\x81\xa5', b'\xe2\x81\xa6'
]

if cfg_file.is_file():
    parser.read(cfg_file)
use_aes = parser.getboolean('settings', 'encrypt', fallback=True)
use_colours = parser.getboolean('settings', 'colours', fallback=True)
colour_options = parser.getint('colours', 'options', fallback=36)
colour_prompt = parser.getint('colours', 'prompt', fallback=33)
colour_inputs = parser.getint('colours', 'inputs', fallback=37)
colour_important = parser.getint('colours', 'important', fallback=31)
colour_success = parser.getint('colours', 'success', fallback=32)
colour_separator = parser.getint('colours', 'separator', fallback=37)
salt = bytes(
    parser.get('settings',
               'salt',
               fallback="\xdc\xebh\x132\x7f\x8cD\xb1U\x1bI\xfa\x1d/i"),
    'raw_unicode_escape')


def colour_text(colour, text):
    if use_colours == 1:
        return "\33[{colour}m".format(colour=colour) + text + "\033[0m"
    else:
        return text


def str2hex(st):
    return st.encode('utf-8').hex()


def encrypt(m, pwd=''):
    if use_aes == 1:
        key = scrypt.hash(pwd, salt, N=16384, r=8, p=1, buflen=32)
        aes_cipher = AES.new(key, AES.MODE_GCM)
        ciphertext = aes_cipher.encrypt(m)
        return (binascii.hexlify(aes_cipher.nonce) +
                binascii.hexlify(ciphertext)).decode('utf-8')
    else:
        return m.hex()


def hex2hid(he):
    for i in range(16):
        he = he.replace(hex(i).split('x')[-1], zwc[i].decode('utf-8'))
    return he


def hex2str(he):
    arr = []
    for m in he:
        arr.append(bytearray.fromhex(m).decode('utf-8'))
    return arr


def wrap(m):
    return b'\xEF\xBB\xBF'.decode("utf-8") + m + b'\xEF\xBB\xBF'.decode(
        "utf-8")


def unwrap(m):
    arr = []
    for i in range(int((len(m.split(b'\xEF\xBB\xBF'.decode("utf-8")))) / 2)):
        arr.append(m.split(b'\xEF\xBB\xBF'.decode("utf-8"))[2 * i + 1])
    return arr


def hid2hex(hi):
    arr = []
    for m in hi:
        for i in range(16):
            m = m.replace(zwc[i].decode('utf-8'), hex(i).split('x')[-1])
        arr.append(m)
    return arr


def decrypt(m, pwd=''):
    if use_aes == 1:
        nonce = binascii.unhexlify(bytes(m, 'utf-8'))[:16]
        ciphertext = binascii.unhexlify(bytes(m, 'utf-8'))[16:]
        key = scrypt.hash(pwd, salt, N=16384, r=8, p=1, buflen=32)
        aes_cipher = AES.new(key, AES.MODE_GCM, nonce)
        return str(aes_cipher.decrypt(ciphertext), 'utf-8')
    else:
        return bytearray.fromhex(m).decode('utf-8')


while True:
    print()
    print(colour_text(colour_options, "    [1]") + _(": Hide a message."))
    print(
        colour_text(colour_options, "    [2]") +
        _(": View hidden message inside text."))
    print()
    ch = input(colour_text(colour_prompt, "r5steg:~$ "))
    if ch == "1":
        secret_msg = input(
            colour_text(colour_inputs, _("Enter secret message: ")))
        init_str = input(
            colour_text(colour_inputs,
                        _("Enter text where the message should be hidden: ")))
        if use_aes == True:
            password = bytes(
                input(
                    colour_text(colour_inputs,
                                _("Enter password for encryption: "))),
                'utf-8')
        else:
            password = None
        result = init_str[:(int(len(init_str) / 2))] + wrap(hex2hid(encrypt(bytes(secret_msg, 'utf-8'), password))) + \
            init_str[int(len(init_str) / 2):]
        print(
            colour_text(colour_important,
                        _("[Hidden Message inside initial string]: ")) +
            result)
        try:
            pyperclip.copy(result)
            print(
                colour_text(colour_success,
                            _("The result has been copied to clipboard!")))
        except pyperclip.PyperclipException as e:
            print(e)
            print(
                colour_text(
                    colour_important,
                    _("The result couldn't be copied to clipboard :(, (maybe) missing xclip"
                      )))
        print(colour_text(colour_separator, "_" * 50))
    elif ch == "2":
        result = input(
            colour_text(colour_inputs, _("Enter text with hidden message: ")))
        if use_aes == True:
            password = bytes(
                input(
                    colour_text(colour_inputs,
                                _("Enter password for encryption: "))),
                'utf-8')
        print(
            colour_text(colour_success,
                        _("\n[Secret message(s) revealed]:\n")))
        for msg in hid2hex(unwrap(result)):
            try:
                print("    " + decrypt(msg, password))
            except UnicodeDecodeError as e:
                print(
                    colour_text(
                        colour_important,
                        _("    Couldn't decrypt message (wrong message/password?):"
                          )))
                print(e)
            print("_" * 50)
    elif ch == "0":
        print(colour_text(colour_success, _("Goodbye!")))
        quit()
