import binaryWork as bw


def encode(file_path, msg):
    encoded_msg = bw.msgToBinary(msg)
    binary_data = bw.extractBinary(file_path)
    # Form groups of 8 bits
    data = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]

    for i in range(len(encoded_msg)):
        data[i] = data[i][:-1] + encoded_msg[i]

    # Join the bytes
    data = ''.join(data)
    bw.restoreData(data)


encode("F:\\Dishonoured.jpg", 'Hello World!')
