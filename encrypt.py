from PIL import Image
import numpy as np
import base64
import pickle
import os
from pathlib import Path


def file_to_binary(file_path):
    index = file_path.rfind('.')
    file_format = file_path[index + 1:]
    name = file_path[:index]
    name = name.split('\\')[-1]

    with open(file_path, 'rb') as file:
        data = file.read()

    file_data = {
        "data": data,
        "metadata": {"name": name, "format": file_format}
    }

    binary_data = base64.b64encode(pickle.dumps(file_data))
    binary_string = ''.join(format(byte, '08b') for byte in binary_data)

    return binary_string


def extractPixels(img):
    img = np.array(img)
    img = img.reshape(-1, 3)
    pixels = list(map(lambda x: tuple(x), img))
    return pixels


def createImage(pixels, width, height, path='encrypted.png'):
    i = 0
    frame = Image.new('RGB', (width, height))
    for y in range(height):
        for x in range(width):
            frame.putpixel((x, y), pixels[i])
            i += 1
    frame.save(path)


def encodePixels(pixels, data, file=False):
    if not file:
        data += '~'
        data = ''.join(format(ord(i), '08b') for i in data)
    else:
        data += "01111110"
    pixels = np.ravel(pixels)
    newPixels = []
    index = 0
    for p in pixels:
        if data[0] == '0' and p % 2 == 1:
            p -= 1
        elif data[0] == '1' and p % 2 == 0:
            p += 1
        newPixels.append(p)
        data = data[1:]
        index += 1
        if len(data) == 0:
            break
    for i in range(index, len(pixels)):
        newPixels.append(pixels[i])

    newPixels = np.array(newPixels)
    newPixels = newPixels.reshape(-1, 3)
    newPixels = list(map(lambda x: tuple(x), newPixels))
    return newPixels


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

    hex_string = '%0*X' % ((len(binary_string) + 3) // 4, int(binary_string, 2))

    binary_data = bytes.fromhex(hex_string)

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
