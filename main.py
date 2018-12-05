import os
import time
import md5

default = getAnimationArray("main")
cloud = getAnimationArray("cloud")

animations = os.listdir()
animations.remove("main")
animations.remove("cloud")
gods = []

for animation in animations:
	gods.append(getAnimationArray(animation))


#look in folder and list all bmp files
#files named 1 to n, load each and put them into array
#each bmp is a 2d array
#end with a 3d array
def getAnimationArray(folder): 
    os.chdir(folder)
    animation_array = []

    for bmp in os.listdir():
        animation_array.append(loadBitmap(bmp))

    return animation_array


def displayAnimation(animation_array):

	for bmp in animation_array:
		setBoard(bmp)
		time.delay(1/30)

def getGod(name): 
	m = md5.new()
	m.update(name)
	god_num = m.digest() % 12
	god = gods[god_num]

def main():
	while True:
		displayAnimation(default)
		