import base64
import pickle


def extractBinary(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()

    binary_data = base64.b64encode(pickle.dumps(data))
    binary_string = ''.join(format(byte, '08b') for byte in binary_data)

    return binary_string


def msgToBinary(msg):

    binary_data = base64.b64encode(pickle.dumps(msg))
    binary_string = ''.join(format(byte, '08b') for byte in binary_data)

    return binary_string


def restoreData(binary_string):
    hex_string = '%0*X' % ((len(binary_string) + 3) // 4, int(binary_string, 2))
    # Convert the hexadecimal string to binary data
    binary_data = bytes.fromhex(hex_string)

    decoded_data = pickle.loads(base64.b64decode(binary_data))

    with open("Dishonoured2.jpg", 'wb') as file:
        file.write(decoded_data)
