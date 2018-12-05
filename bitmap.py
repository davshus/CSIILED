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
    idx = offset
    for y in range(height - 1,-1,-1):
        for x in range(0,width):
            # idx = offset + (((height - 1 - y)*width) + x) * pixel_width
            pixel_data = ()
            for i in range(0,pixel_width):
                print(pixel_data)
                pixel_data = pixel_data + (int.from_bytes(bytes[idx+i], byteorder=sys.byteorder, signed=False),)
                # idx += 1
            #BGR to RGB
            pixel_data = pixel_data[2::-1] + pixel_data[3:]
            # print("(" + str(x) + ", " + str(y) + ") " + str(pixel_data))
            # print(len(image))
            # print(len(image[0]))
            image[x][y] = pixel_data
            idx += pixel_width
    return image #bmp starts from the bottom

def combine_bytes(list):
    return struct.unpack()
    num = 0
    for byte in list:
        num <<= 8
        num |= int.from_bytes(byte, byteorder=sys.byteorder, signed=False)
    return num

def normal(src, dst):
    s = tuple(val/255 for val in src)
    d = tuple(val/255 for val in dst)
    out = (0,0,0,0)
    alpha = s[3] + d[3]*(1-s[3])
    # out[0] = (s[0]*s[3] + d[0]*d[3]*(1-s[3]))/alpha
    # out[1] = (s[1]*s[3] + d[1]*d[3]*(1-s[3]))/alpha
    # out[2] = (s[2]*s[3] + d[2]*d[3]*(1-s[3]))/alpha
    out = ((s[0]*s[3] + d[0]*d[3]*(1-s[3]))/alpha, (s[1]*s[3] + d[1]*d[3]*(1-s[3]))/alpha, (s[2]*s[3] + d[2]*d[3]*(1-s[3]))/alpha, alpha)
    o = tuple(int(val*255) for val in out)
    return o

def composite(*args):
    if len(args) % 2 == 0:
        print("uh oh spaghett")
        raise ValueError("NO")
    layers = args + (normal, [[(255, 255, 255, 255)] * len(args[0][0])] * len(args[0]))
    # print(layers)
    curr = layers[0][:]
    for i in range(1, len(layers), 2):
        func = layers[i]
        dst = layers[i+1]
        for x in range(0, len(curr)):
            for y in range(0, len(curr[0])):
                curr[x][y] = func(curr[x][y], dst[x][y])
    fin = [[None] * len(curr[0])] * len(curr)
    for x in range(0, len(curr)):
        for y in range(0, len(curr[0])):
            # print(str(x) + ', ' + str(y))
            fin[x][y] = curr[x][y][:3]
    #Final composite
    # out = (0,0,0)
    # background = (255,255,255)
    # prefin = tuple(val/255 for val in curr)
    # out[0] = prefin[0]*prefin[3] + background[0]*(1-prefin[3])
    # out[1] = prefin[1]*prefin[3] + background[1]*(1-prefin[3])
    # out[2] = prefin[2]*prefin[3] + background[2]*(1-prefin[3])
    # return tuple(int(val*255) for val in out)
    return fin
