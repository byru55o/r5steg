#!/usr/bin/env python3

import binascii, readline, pyperclip, scrypt, gettext
from Crypto.Cipher import AES

t = gettext.translation('r5steg', '/usr/share/locale/', fallback=True,)
_ = t.gettext

salt = b'\xdc\xebh\x132\x7f\x8cD\xb1U\x1bI\xfa\x1d/i'

zwc = [b'\xe2\x81\xa0'.decode("utf-8"), b'\xe2\x80\x8b'.decode("utf-8"), b'\xe2\x80\x8d'.decode("utf-8"),
       b'\xe2\x80\x8e'.decode("utf-8"), b'\xe2\x80\x8f'.decode("utf-8"), b'\xe2\x80\x8c'.decode("utf-8"),
       b'\xe2\x81\xa1'.decode("utf-8"), b'\xe1\xa0\x8e'.decode("utf-8"), b'\xe2\x80\xaa'.decode("utf-8"),
       b'\xe2\x80\xac'.decode("utf-8"), b'\xe2\x80\xad'.decode("utf-8"), b'\xe2\x81\xa2'.decode("utf-8"),
       b'\xe2\x81\xa3'.decode("utf-8"), b'\xe2\x81\xa4'.decode("utf-8"), b'\xe2\x81\xa5'.decode("utf-8"),
       b'\xe2\x81\xa6'.decode("utf-8")]


def encrypt(m, pwd):
    key = scrypt.hash(pwd, salt, N=16384, r=8, p=1, buflen=32)
    aes_cipher = AES.new(key, AES.MODE_GCM)
    ciphertext = aes_cipher.encrypt(m)
    return (binascii.hexlify(aes_cipher.nonce) + binascii.hexlify(ciphertext)).decode('utf-8')


def hex2hid(he):
    for i in range(16):
        he = he.replace(hex(i).split('x')[-1], zwc[i])
    return he


def wrap(m):
    return b'\xEF\xBB\xBF'.decode("utf-8") + m + b'\xEF\xBB\xBF'.decode("utf-8")


def unwrap(m):
    arr = []
    for i in range(int((len(m.split(b'\xEF\xBB\xBF'.decode("utf-8")))) / 2)):
        arr.append(m.split(b'\xEF\xBB\xBF'.decode("utf-8"))[2 * i + 1])
    return arr


def hid2hex(hi):
    arr = []
    for m in hi:
        for i in range(16):
            m = m.replace(zwc[i], hex(i).split('x')[-1])
        arr.append(m)
    return arr


def decrypt(m, pwd):
    nonce = binascii.unhexlify(bytes(m, 'utf-8'))[:16]
    ciphertext = binascii.unhexlify(bytes(m, 'utf-8'))[16:]
    key = scrypt.hash(pwd, salt, N=16384, r=8, p=1, buflen=32)
    aes_cipher = AES.new(key, AES.MODE_GCM, nonce)
    return str(aes_cipher.decrypt(ciphertext), 'utf-8')


while True:
    print()
    print(_("    [1]: Hide a message."))
    print(_("    [2]: View hidden message inside text."))
    print()
    ch = input("r5steg:~$ ")
    if ch == "1":
        secret_msg = input(_("Enter secret message: "))
        init_str = input(_("Enter text where the message should be hidden: "))
        password = bytes(input(_("Enter password for encryption: ")), 'utf-8')
        result = init_str[:(int(len(init_str) / 2))] + wrap(hex2hid(encrypt(bytes(secret_msg, 'utf-8'), password))) + \
            init_str[int(len(init_str) / 2):]
        print(_("[Hidden Message inside initial string]: ") + result)
        try:
            pyperclip.copy(result)
            print(_("The result has been copied to clipboard!"))
        except pyperclip.PyperclipException as e:
            print(e)
            print(_("The result couldn't be copied to clipboard :(, (maybe) missing xclip"))
        print("_" * 50)
    elif ch == "2":
        result = input(_("Enter text with hidden message: "))
        password = bytes(input(_("Enter password for encryption: ")), 'utf-8')
        print(_("\n[Secret message(s) revealed]:\n"))
        for msg in hid2hex(unwrap(result)):
            try:
                print("    " + decrypt(msg, password))
            except UnicodeDecodeError as e:
                print(_("    Couldn't decrypt message (wrong message/password?):"))
                print(e)
            print("_" * 50)
    elif ch == "0":
        print(_("Goodbye!"))
        quit()
