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
