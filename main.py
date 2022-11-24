#!/usr/bin/env python3

import readline
from pyperclip import copy, PyperclipException


def str2bin(st):
    return ' '.join(format(ord(x), 'b') for x in st)


def bin2hid(bi):
    return bi.replace('1', b'\xE2\x80\x8B'.decode("utf-8")).replace('0', b'\xE2\x81\xA0'.decode("utf-8")) \
        .replace(' ', b'\xE2\x80\x8C'.decode("utf-8"))


def wrap(msg):
    return b'\xEF\xBB\xBF'.decode("utf-8") + msg + b'\xEF\xBB\xBF'.decode("utf-8")


def unwrap(msg):
    arr = []
    for i in range(int((len(msg.split(b'\xEF\xBB\xBF'.decode("utf-8")))) / 2)):
        arr.append(msg.split(b'\xEF\xBB\xBF'.decode("utf-8"))[2 * i + 1])
    return arr


def hid2bin(hi):
    arr = []
    for msg in hi:
        arr.append(msg.replace(b'\xE2\x80\x8B'.decode("utf-8"), '1').replace(b'\xE2\x81\xA0'.decode("utf-8"), '0')
                   .replace(b'\xE2\x80\x8C'.decode("utf-8"), ' '))
    return arr


def bin2str(bi):
    arr = []
    for msg in bi:
        arr.append(''.join([chr(int(x, 2)) for x in msg.split(' ')]))
    return arr


while True:
    print('''
    [1]: Hide a message.
    [2]: View hidden message inside text.
    ''')
    ch = input("r5steg:~$ ")
    if ch == "1":
        secret_msg = input("Enter secret message: ")
        init_str = input("Enter text where the message should be hidden: ")
        result = init_str[:(int(len(init_str) / 2))] + wrap(bin2hid(str2bin(secret_msg))) + \
            init_str[int(len(init_str) / 2):]
        print("[Hidden Message inside initial string]: " + result)
        try:
            copy(result)
            print("The result has been copied to clipboard!")
        except PyperclipException as e:
            print(e)
            print("The result couldn't be copied to clipboard :(, (maybe) missing xclip")
        print("_" * 50)
    elif ch == "2":
        result = input("Enter text with hidden message: ")
        print("\n[Secret message(s) revealed]:\n")
        for msg in bin2str(hid2bin(unwrap(result))):
            print("    " + msg)
            print("_" * 50)
    elif ch == "0":
        print("Goodbye!")
        quit()
