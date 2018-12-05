# import sys
# def load(path):
#     print("[BMP] Loading bitmap " + path)
#     bytes = list()
#     with open(path, "rb") as f:
#         byte = f.read(1)
#         while byte:
#             bytes.append(byte)
#             byte = f.read(1)
#     offset = combine_bytes(bytes[10:14][::-1])
#     print(str(bytes[18:22][::-1]))
#     print(str(bytes[22:26][::-1]))
#     width = combine_bytes(bytes[18:22][::-1])
#     height = combine_bytes(bytes[22:26][::-1])
#     image = [[(0,0,0)] * height] * width
#     print("[BMP] Bitmap is " + str(width) + "x" + str(height))
#     bpp = combine_bytes(bytes[28:30][::-1])
#     alpha = bpp == 32
#     pixel_width = bpp//8
#     for x in range(0,width):
#         for y in range(0,height):
#             idx = offset + (y*width) + x
#             pixel_data = ()
#             for i in range(0,pixel_width):
#                 pixel_data = (int.from_bytes(bytes[idx + i], byteorder=sys.byteorder, signed=False),) + pixel_data
#             image[x][y] = pixel_data
#     return image
#
# def combine_bytes(list):
#     num = 0
#     for byte in list:
#         num <<= 8
#         num |= int.from_bytes(byte, byteorder=sys.byteorder, signed=False)
#     return num
import sys
import struct
def load(path):
    print("[BMP] Loading bitmap " + path)
    bytes = list()
    with open(path, "rb") as f:
        byte = f.read(1)
        while byte:
            bytes.append(byte)
            byte = f.read(1)
    offset = struct.unpack('I', b''.join(bytes[10:14]))[0]
    print(str(bytes[18:22]))
    print(str(bytes[22:26]))
    width = struct.unpack('I', b''.join(bytes[18:22]))[0]
    height = struct.unpack('I', b''.join(bytes[22:26]))[0]
    image = [[(0,0,0)] * height] * width
    print("[BMP] Bitmap is " + str(width) + "x" + str(height))
    bpp = struct.unpack('H', b''.join(bytes[28:30]))[0]
    alpha = bpp == 32
    pixel_width = bpp//8
    # print(offset)

    for y in range(0,height):
        for x in range(0,width):
            idx = offset + ((y*width) + x) * pixel_width
            pixel_data = ()
            for i in range(0,pixel_width):
                pixel_data = pixel_data + (int.from_bytes(bytes[idx + i], byteorder=sys.byteorder, signed=False),)
            # print("(" + str(x) + ", " + str(y) + ") " + str(pixel_data))
            # print(len(image))
            # print(len(image[0]))
            image[x][y] = pixel_data
    return image

def combine_bytes(list):
    return struct.unpack()
    num = 0
    for byte in list:
        num <<= 8
        num |= int.from_bytes(byte, byteorder=sys.byteorder, signed=False)
    return num
