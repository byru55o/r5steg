from nicegui import ui, events
import binascii
import readline
import pyperclip
import scrypt
from Crypto.Cipher import AES


# This is for showing just the button of the mode selected
# "HIDE", "ENCRYPT AND HIDE", "UNHIDE" or "UNHIDE AND DECRYPT"
class Logic:
    def __init__(self):
        self.input_1: bool = True
        self.input_2: bool = True
        self.just_aes: bool = False
        self.just_hide: bool = False
        self.neither_active: bool = False
        self.both_active: bool = True

    def update_input_1(self, e: events.ValueChangeEventArguments):
        self.input_1 = e.value
        self.update()

    def update_input_2(self, e: events.ValueChangeEventArguments):
        self.input_2 = e.value
        self.update()

    def update(self):
        self.just_aes = self.input_1 and not self.input_2  # decrypt and unhide
        self.just_hide = self.input_2 and not self.input_1  # hide
        self.neither_active = not (self.input_1 or self.input_2)  # unhide
        self.both_active = self.input_1 and self.input_2  # encrypt and hide


logic = Logic()


# Characters used
zwc = [
    b"\xe2\x81\xa0",
    b"\xe2\x80\x8b",
    b"\xe2\x80\x8d",
    b"\xe2\x80\x8e",
    b"\xe2\x80\x8f",
    b"\xe2\x80\x8c",
    b"\xe2\x81\xa1",
    b"\xe1\xa0\x8e",
    b"\xe2\x80\xaa",
    b"\xe2\x80\xac",
    b"\xe2\x80\xad",
    b"\xe2\x81\xa2",
    b"\xe2\x81\xa3",
    b"\xe2\x81\xa4",
    b"\xe2\x81\xa5",
    b"\xe2\x81\xa6",
]

# Just for styling
textarea_props = "input-style='width:100%;height:150px;padding:12px;"
"box-sizing: border-box;border: 2px solid #ccc;border-radius: 4px;"
"background-color: #f8f8f8;font-size: 16px; resize: none;"
textarea_style = "width: 100%;height: 150px; resize: none;"


# Basic functions from r5steg


def str2hex(st):
    return st.encode("utf-8").hex()


def encrypt(m, enc, salt="u4bWVrvuZmcT", pwd=""):
    if enc == 1:
        key = scrypt.hash(pwd, salt, N=16384, r=8, p=1, buflen=32)
        aes_cipher = AES.new(key, AES.MODE_GCM)
        ciphertext = aes_cipher.encrypt(m)
        return (
            binascii.hexlify(aes_cipher.nonce) + binascii.hexlify(ciphertext)
        ).decode("utf-8")
    else:
        return m.hex()


def hex2hid(he):
    for i in range(16):
        he = he.replace(hex(i).split("x")[-1], zwc[i].decode("utf-8"))
    return he


def hex2str(he):
    arr = []
    for m in he:
        arr.append(bytearray.fromhex(m).decode("utf-8"))
    return arr


def wrap(m):
    return b"\xEF\xBB\xBF".decode("utf-8") + m + b"\xEF\xBB\xBF".decode("utf-8")


def unwrap(m):
    arr = []
    for i in range(int((len(m.split(b"\xEF\xBB\xBF".decode("utf-8")))) / 2)):
        arr.append(m.split(b"\xEF\xBB\xBF".decode("utf-8"))[2 * i + 1])
    return arr


def hid2hex(hi):
    arr = []
    for m in hi:
        for i in range(16):
            m = m.replace(zwc[i].decode("utf-8"), hex(i).split("x")[-1])
        arr.append(m)
    return arr


def decrypt(m, enc, salt, pwd=""):
    if enc == 1:
        nonce = binascii.unhexlify(bytes(m, "utf-8"))[:16]
        ciphertext = binascii.unhexlify(bytes(m, "utf-8"))[16:]
        key = scrypt.hash(pwd, salt, N=16384, r=8, p=1, buflen=32)
        aes_cipher = AES.new(key, AES.MODE_GCM, nonce)
        return str(aes_cipher.decrypt(ciphertext), "utf-8")
    else:
        return bytearray.fromhex(m).decode("utf-8")


def reveal(plaintext, enc, salt, hist, password=""):
    results = hid2hex(unwrap(plaintext))
    print(results)
    ui.notify(f"{len(results)} hidden messages detected!")
    for msg in results:
        try:
            result = decrypt(msg, enc, salt, password)
            hist.append(result)
            ui.notify("SUCCESS!! Secret text has been added to history")
        except UnicodeDecodeError as e:
            ui.notify("Couldn't decrypt message (wrong message/password?):")
            ui.notify(e)


# Nicegui code


# Make history refreshable
@ui.refreshable
def history(res):
    [ui.label(res[i]) for i in range(len(res))]


# Main page, where the app lives
@ui.page("/r5steg")
def page_layout():
    # Header
    with ui.header(elevated=True).style("background-color: #3874c8").classes(
        "items-center justify-between"
    ):
        ui.markdown("#R5STEG: text in text steganography")
        results = []  # Initialise the result list (history)
        ui.button(on_click=lambda: right_drawer.toggle(), icon="menu").props(
            "flat color=white"
        )  # Toggle settings
    # History
    with ui.left_drawer(top_corner=True, bottom_corner=True).style(
        "background-color: #d7e3f4"
    ):
        ui.markdown("#History")
        history(results)
    # Settings
    with ui.right_drawer(fixed=False).style("background-color: #ebf1fa").props(
        "bordered"
    ) as right_drawer:
        ui.markdown("#Settings")
        ui.markdown(
            "_WARNING: salt must be the same encrypting and decrypting, otherwise it wont work_"
        )
        salt = ui.input(
            label="Salt string, modify for better security", value="u4bWVrvuZmcT"
        ).props(
            "size=40"
        )  # Careful: default value isn't the same as in cli r5steg
        use_aes = ui.switch(
            "toggle AES encryption", value=True, on_change=logic.update_input_1
        )  # toggle encryption
    # Footer
    with ui.footer().style("background-color: #3874c8"):
        ui.markdown("[GITHUB](https://github.com/byru55o) | LICENSE: GPL 3.0")
    # Content
    mode = ui.toggle(
        {True: "HIDE", False: "UNHIDE"}, value=True, on_change=logic.update_input_2
    )
    ui.label(
        "Enter plaintext below:"
    )  # The text where the message (should be/is) hidden
    plaintext = ui.textarea().props(textarea_props).style(textarea_style)
    ui.label("Hidden message:").bind_visibility_from(mode, "value")  # Secret message
    hiddentext = (
        ui.textarea()
        .props(textarea_props)
        .style(textarea_style)
        .bind_visibility_from(mode, "value")
    )
    password = (
        ui.input(label="password", password=True, password_toggle_button=True)
        .props("size=40")
        .bind_visibility_from(use_aes, "value")
    )  # Password used for encryption-decryption
    ui.button(
        "Encrypt and hide message",
        on_click=lambda: (  # Code executed on-click below
            results.append(  # Add the result to the history
                plaintext.value[: (int(len(plaintext.value) / 2))]
                + wrap(  # Encrypted, hidden and wrapped text in between the plaintext
                    hex2hid(
                        encrypt(
                            bytes(hiddentext.value, "utf-8"),
                            1,
                            bytes(salt.value, "utf-8"),
                            bytes(password.value, "utf-8"),
                        )
                    )
                )
                + plaintext.value[int(len(plaintext.value) / 2) :]
            ),
            history.refresh(),  # Refresh the history to show it real-time
            ui.clipboard.write(results[-1]),
            ui.notify("Success!, result saved in history and copied to clipboard"),
        ),
    ).bind_visibility_from(
        logic, "both_active"
    )  # Only visible when use_aes and mode are True
    ui.button(
        "Hide message",
        on_click=lambda: (
            results.append(
                plaintext.value[: (int(len(plaintext.value) / 2))]
                + wrap(
                    hex2hid(
                        encrypt(  # Actually doesn't encrypt anything, as the 2nd arg is 0
                            bytes(hiddentext.value, "utf-8"),
                            0,
                            bytes(salt.value, "utf-8"),
                            None,
                        )  # This is just for reverse-compatibility with cli r5steg
                    )
                )
                + plaintext.value[int(len(plaintext.value) / 2) :]
            ),
            history.refresh(),  # TODO this code below repeats, make function to simplify!
            ui.notify("Success!, result saved in history and copied to clipboard"),
            ui.clipboard.write(results[-1]),
        ),
    ).bind_visibility_from(
        logic, "just_hide"
    )  # Only visible when use_aes False and mode True
    ui.button(
        "Unhide and decrypt message",
        on_click=lambda: (
            reveal(
                plaintext.value,
                1,
                bytes(salt.value, "utf-8"),
                results,
                bytes(password.value, "utf-8"),
            ),
            history.refresh(),
            ui.notify("Success!, result saved in history"),
        ),
    ).bind_visibility_from(
        logic, "just_aes"
    )  # Only visible when use_aes True and mode False
    ui.button(
        "Unhide",
        on_click=lambda: (
            reveal(plaintext.value, 0, bytes(salt.value, "utf-8"), results),
            history.refresh(),
            ui.notify("Success!, result saved in history"),
        ),
    ).bind_visibility_from(
        logic, "neither_active"
    )  # Only visible when use_aes and mode are False


ui.link("try r5steg beta", page_layout)  # Link to the actual app on the mainpage

ui.run(port=3443, title="r5steg beta")
