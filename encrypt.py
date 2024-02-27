from PIL import Image
import numpy as np
import base64
import pickle
import os
from pathlib import Path
import binascii


def extractPixels(img):
    img = np.array(img)
    img = img.reshape(-1, 3)
    pixels = [tuple(p) for p in img]
    return pixels


def createImage(pixels, width, height, path='encrypted.png'):
    pixels_flat = np.array(pixels).reshape(-1)
    frame = Image.fromarray(pixels_flat.reshape((height, width, 3)).astype(np.uint8), 'RGB')
    frame.save(path)


def encodePixels(pixels, data, file=False):
    if not file:
        data += '~'
        data = ''.join(format(ord(i), '08b') for i in data)
    else:
        data += "01111110"

    pixels = np.ravel(pixels)

    for i, pixel_value in enumerate(pixels):
        if i < len(data):
            if data[i] == '0' and pixel_value % 2 == 1:
                pixels[i] -= 1
            elif data[i] == '1' and pixel_value % 2 == 0:
                pixels[i] += 1
        else:
            break

    pixels = pixels.reshape(-1, 3)
    return [tuple(p) for p in pixels]


def decryptImageToText(path):
    img = Image.open(path)
    width, height = img.size
    pixels = np.ravel(extractPixels(img))
    data, byte = '', ''
    for p in pixels:
        if p % 2 == 0:
            byte += '0'
        else:
            byte += '1'
        if len(byte) == 8:
            byte = chr(int(byte, 2))
            if byte == '~':
                return data
            data += byte
            byte = ''


def getData(data):
    binary_string = data

    binary_data = binascii.unhexlify('%0*X' % ((len(binary_string) + 3) // 4, int(binary_string, 2)))

    decoded_data = pickle.loads(base64.b64decode(binary_data))

    original_data = decoded_data["data"]
    name = decoded_data["metadata"]["name"]
    file_format = decoded_data["metadata"]["format"]

    output_file_path = Path(f"{name}.{file_format}")
    with output_file_path.open('wb') as new_file:
        new_file.write(original_data)

    exit()


def decryptImageToFile(path):
    img = Image.open(path)
    width, height = img.size
    pixels = np.ravel(extractPixels(img))
    data, byte = '', ''
    for p in pixels:
        if p % 2 == 0:
            byte += '0'
        else:
            byte += '1'
        if len(byte) == 8:
            if chr(int(byte, 2)) == '~':
                getData(data)
            data += byte
            byte = ''


def encryptImageWithData(path, data):
    img = Image.open(path)
    width, height = img.size
    if (len(data) + 1) * 8 > width * height * 3:
        raise Exception('Image is too small to encrypt this data.')
    pixels = extractPixels(img)
    encoded_pixel = encodePixels(pixels, data)
    createImage(encoded_pixel, width, height)


def encryptImageWithFile(img_path, file_path):
    def file_to_binary(file_path):
        name = os.path.basename(file_path)
        file_format = os.path.splitext(name)[1][1:]

        chunk_size = 8192
        data = b''

        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                data += chunk

        file_data = {
            "data": data,
            "metadata": {"name": name, "format": file_format}
        }

        binary_data = base64.b64encode(pickle.dumps(file_data))
        binary_string = ''.join(format(byte, '08b') for byte in binary_data)

        return binary_string

    data = file_to_binary(file_path)
    img = Image.open(img_path)
    width, height = img.size
    if len(data) + 8 > width * height * 3:
        raise Exception('Image is too small to encrypt this file.')
    pixels = extractPixels(img)
    encoded_pixel = encodePixels(pixels, data, file=True)
    createImage(encoded_pixel, width, height)


if __name__ == '__main__':
    pass
