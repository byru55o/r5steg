def str2bin(st):
    return ' '.join(format(ord(x), 'b') for x in st)


def bin2hid(bi):
    return bi.replace('1', b'\xE2\x80\x8B'.decode("utf-8")).replace('0', b'\xE2\x81\xA0'.decode("utf-8")). \
        replace(' ', b'\xE2\x80\x8C'.decode("utf-8"))


def wrap(msg):
    return b'\xEF\xBB\xBF'.decode("utf-8") + msg + b'\xEF\xBB\xBF'.decode("utf-8")


def unwrap(msg):
    return msg.split(b'\xEF\xBB\xBF'.decode("utf-8"))[1]


def hid2bin(hi):
    return hi.replace(b'\xE2\x80\x8B'.decode("utf-8"), '1').replace(b'\xE2\x81\xA0'.decode("utf-8"), '0'). \
        replace(b'\xE2\x80\x8C'.decode("utf-8"), ' ')


def bin2str(bi):
    return ''.join([chr(int(x, 2)) for x in bi.split(' ')])


init_str = "Initial String"
secret_msg = "Encoded Message"
print(init_str)
print(secret_msg)
print("[Secret Message encoded in binary]: " + str2bin(secret_msg))
print("[Encoded Message hidden]: >" + bin2hid(str2bin(secret_msg)) + "<")
print("[Encoded Message hidden wrapped]: >" + wrap(bin2hid(str2bin(secret_msg))) + "<")
result = init_str[0] + wrap(bin2hid(str2bin(secret_msg))) + init_str[1:len(init_str)]
print("[Hidden Message inside initial string]: " + result)

print("[Unwrapped encoded message hidden]: >" + unwrap(result) + "<")
print("[Encoded message in binary]: " + hid2bin(unwrap(result)))
print("[Secret message revealed]: " + bin2str(hid2bin(unwrap(result))))


while True:
    print('''
    [1]: Hide a message.
    [2]: View hidden message inside text.
    ''')
    ch = input("r5steg:~$ ")
    if ch == "1":
        secret_msg = input("Enter secret message: ")
        init_str = input("Enter text where the message should be hidden: ")
        result = init_str[0] + wrap(bin2hid(str2bin(secret_msg))) + init_str[1:len(init_str)]
        print("[Hidden Message inside initial string]: " + result)
        print("Now feel free to copy the result and paste it where you want!")
        print("_____________________________________________________________\n")

    elif ch == "2":
        result = input("Enter text with hidden message: ")
        print("[Secret message revealed]: " + bin2str(hid2bin(unwrap(result))))
        print("_____________________________________________________________\n")
