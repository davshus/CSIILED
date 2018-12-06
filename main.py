import os
import sys
import time
import hashlib
import bitmap as bmp
import glob
import csiiled

gods = []
play_queue = []
#look in folder and list all bmp files
#files named 1 to n, load each and put them into array
#each bmp is a 2d array
#end with a 3d array
def getAnimationArray(folder):
    print(os.getcwd())
    os.chdir('/home/pi/animations/' + folder)
    animation_array = []

    for fname in [j + ".bmp" for j in sorted([i[:len(i)-4] for i in glob.glob("*.bmp")], key=int)]:
        animation_array.append(bmp.load(fname))

    return animation_array

#TODO: implement multi-layered animation cycle using bmp.composite

def blend(priority, background):
    p = bmp.composite(priority)
    b = bmp.composite(background)
    last_pixel_of_priority = -1
    # find last pixel of cloud
    for index, col in enuemrate(priority[9]):
        if col[0] > 200 and col[1] > 200 and col[2] > 200:
            last_pixel_of_priority = index
            break
    board = [[0] * 18] * 15
    for row in range(18):
        for col in range(15):
            if col < last_pixel_of_priority:
                board = priority[row][col]
            else:
                board = background[row][col]

def displayAnimation(animation_array, intro=None, play_intro_frames=None):
    if intro is None:
        for frame in animation_array:
            csiiled.setBoard(bmp.composite(frame))
            time.sleep(1/10)
    else:
        num_frames = play_intro_frames + len(animation_array)
        for i in range(num_frames):
            if i < play_intro_frame: # only play intro
                csiiled.setBoard(bmp.composite(intro[i]))
            else if i < len(intro): #blend intro + animation
                csiiled.setBoard(bmp.composite(intro[i], bmp.normal(), animation_array[i-play_intro_frames]))
            else:
                csiiled.setBoard(bmp.composite(animation_array[i-play_intro_frames]))

layers = [-1, -1, 0]
empty = [[(255,255,255) for i in range(15)] for i in range(18)]
default = getAnimationArray("main")
cloud = getAnimationArray("cloud")
current = None
def requestAnimationFrame():
    global layers
    global empty
    global current
    global default
    global cloud
    if layers[0] <= cloud % 2 or current is None:
        if len(play_queue == 0):
            layers[0] = -1
        else:
            current = play_queue.pop()
            layers[0] += 1
    else:
        layers[1] = layers[1]+1
    layers[2] = (layers[2] + 1) % len(default)
    if not current is None and layers[1] >= len(current):
        layers[1] = -1
        layers[0] = -1
        current = None
        #Done playing animation
    c = empty if layers < 0 or layers >= len(cloud) else cloud[layers[0]]
    a = empty if current is None else current[layers[1]]
    d = default[[layers[2]]]
    render = bmp.composite(c, bmp.normal, a, bmp.normal, d)
    csiiled.setBoard(render)
    time.sleep(1/20)




def getGod(name):
    global gods
    m = hashlib.md5()
    m.update(name)
    god_num = int.from_bytes(m.digest(), byteorder=sys.byteorder, signed=False) % 12
    god = gods[god_num]
    play_queue.append(god)

if __name__ == '__main__':
    global gods
    # default = getAnimationArray("main")
    global default
    default_length = len(default)
    # cloud = getAnimationArray("cloud")
    os.chdir("/home/pi/animations")
    animations = os.listdir()
    animations.remove("main")
    animations.remove("cloud")

    for animation in animations:
        gods.append(getAnimationArray(animation)) #NOTE: shouldn't this be a map?

    # while True:
    #     if len(play_queue) == 0:
    #         displayAnimation(default)
    #     else:
    #         next = play_queue.pop()
    #         displayAnimation(next, intro=default, play_intro_frames=default_length/2)
    while True:
        requestAnimationFrame()
