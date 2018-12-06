import os
import sys
import time
import hashlib
import bitmap as bmp
import glob
import csiiled



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

def displayAnimation(animation_array):
    for frame in animation_array:
        csiiled.setBoard(bmp.composite(frame))
        time.sleep(1/10)

def getGod(name):
    m = hashlib.md5()
    m.update(name)
    god_num = int.from_bytes(m.digest(), byteorder=sys.byteorder, signed=False) % 12
    god = gods[god_num]

if __name__ == '__main__':
    default = getAnimationArray("main")
    # cloud = getAnimationArray("cloud")
    os.chdir("/home/pi/animations")
    animations = os.listdir()
    animations.remove("main")
    animations.remove("cloud")
    gods = []

    for animation in animations:
        gods.append(getAnimationArray(animation))
    while True:
        displayAnimation(default)
