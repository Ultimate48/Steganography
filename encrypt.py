from PIL import Image
import numpy as np


def extractPixels(path):
    img = Image.open(path)
    width, height = img.size
    img = np.array(img)
    img = img.reshape(-1, 3)
    pixels = list(map(lambda x: tuple(x), img))
    return pixels, width, height


def createImage(pixels, width, height, path='encrypted.png'):
    i = 0
    frame = Image.new('RGB', (width, height))
    for y in range(height):
        for x in range(width):
            frame.putpixel((x, y), pixels[i])
            i += 1
    frame.save(path)


def encodePixels(pixels, data):
    data += '\n'
    data = ''.join(format(ord(i), '08b') for i in data)
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


def decryptImage(path):
    pixels = extractPixels(path)[0]
    data, byte = '', ''
    pixels = np.ravel(pixels)
    for p in pixels:
        if p % 2 == 0:
            byte += '0'
        else:
            byte += '1'
        if len(byte) == 8:
            byte = chr(int(byte, 2))
            if byte == '\n':
                return data
            data += byte
            byte = ''
    return data


def encryptImage(path, data):
    pixels, width, height = extractPixels(path)
    encoded_pixel = encodePixels(pixels, data)
    createImage(encoded_pixel, width, height)

if __name__ == '__main__':

    data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    encryptImage('image.png', data)

    print(decryptImage('encrypted.png'))
