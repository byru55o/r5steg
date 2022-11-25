#!/usr/bin/env python3

import readline, pyperclip

zwc = [b'\xe2\x81\xa0'.decode("utf-8"), b'\xe2\x80\x8b'.decode("utf-8"), b'\xe2\x80\x8d'.decode("utf-8"),
       b'\xe2\x80\x8e'.decode("utf-8"), b'\xe2\x80\x8f'.decode("utf-8"), b'\xe2\x80\x8c'.decode("utf-8"),
       b'\xe2\x81\xa1'.decode("utf-8"), b'\xe1\xa0\x8e'.decode("utf-8"), b'\xe2\x80\xaa'.decode("utf-8"),
       b'\xe2\x80\xac'.decode("utf-8"), b'\xe2\x80\xad'.decode("utf-8"), b'\xe2\x81\xa2'.decode("utf-8"),
       b'\xe2\x81\xa3'.decode("utf-8"), b'\xe2\x81\xa4'.decode("utf-8"), b'\xe2\x81\xa5'.decode("utf-8"),
       b'\xe2\x81\xa6'.decode("utf-8")]


def str2hex(st):
    return st.encode('utf-8').hex()


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


def hex2str(he):
    arr = []
    for m in he:
        arr.append(bytearray.fromhex(m).decode('utf-8'))
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
        result = init_str[:(int(len(init_str) / 2))] + wrap(hex2hid(str2hex(secret_msg))) + \
            init_str[int(len(init_str) / 2):]
        print("[Hidden Message inside initial string]: " + result)
        try:
            pyperclip.copy(result)
            print("The result has been copied to clipboard!")
        except pyperclip.PyperclipException as e:
            print(e)
            print("The result couldn't be copied to clipboard :(, (maybe) missing xclip")
        print("_" * 50)
    elif ch == "2":
        result = input("Enter text with hidden message: ")
        print("\n[Secret message(s) revealed]:\n")
        for msg in hex2str(hid2hex(unwrap(result))):
            print("    " + msg)
            print("_" * 50)
    elif ch == "0":
        print("Goodbye!")
        quit()

