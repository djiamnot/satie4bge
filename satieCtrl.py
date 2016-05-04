import bge
import os
import random
import sys

#print("--> SATIE EXAMPLE - loading")
#
#
#CURDIR = bge.logic.expandPath('//')
#print("-->> current directory {}".format(CURDIR))
#SCRIPTS_PATH = os.path.join(CURDIR, 'postmetrue-common', 'scripts')
#SATIE_PATH = os.path.join(CURDIR, 'postmetrue-common', 'scripts', 'satie')
#print("sys.path before -->> {}".format(sys.path))
#if SATIE_PATH not in sys.path:
#    sys.path.append(SATIE_PATH)
#    print("sys.path after -->> {}".format(sys.path))
#
#sys.path.append(SCRIPTS_PATH)

from . import satie

cont = bge.logic.getCurrentController()
scene = bge.logic.getCurrentScene()
print("objects active: {}".format(scene.objects))
print("objects inactive: {}".format(scene.objectsInactive))

bge.logic.synths = []

# pinky = Satie(scene.addObject("SatieObject", "Pinky"), "Pinky", "posture101")
# pinky.makeInstance("synths", "testtone", "tastee")
# pinky.setParent("Pinky")
# pinky.myParent = "Pinky"

#scene.addObject("Cube")

def instantiateVoices():
    import socket
    users = bge.logic.globalDict["users"]
    print("found following users", users)
    me = socket.gethostname()
    print("my hostname is", me)
    for idx, user in enumerate(users):
        if user == me:
            print("Not doing anything for user ", user)
        else:
            print("Creating SATIE source for", user)
            print("scene objects: ", scene.objects)
            satieInput = satie.Satie(scene.addObject(scene.objectsInactive["SatieObject"], scene.objects[user]), user, me)
            satieInput.visible = False
            # satieInput.makeInstance("voices", user, "tastee")
            satieInput.makeInstance("voices", user, "monoIn") # instantiate a mono input
            satieInput.setParam("bus", idx)
            bge.logic.synths.append(satieInput)

def instantiateTestSound():
    sound = satie.Satie(scene.addObject(scene.objectsInactive["SatieObject"]), "Plane", "00_startup")
    sound.makeInstance("synths", "testtone"+str(random.randint(0,1000)), "tastee")
    sound.localPosition = [random.randint(-100, 100)*0.03, random.randint(-100,100)*0.02, random.randint(0,50)*0.05]
    sound.visible = True
    bge.logic.synths.append(sound)

def update():
    for synth in bge.logic.synths:
        synth.update()
        # print("synth world position", synth.worldPosition)
    
def cleanSynths():
    for synth in bge.logic.synths:
        synth.deleteInstance()
    # bge.logic.endGame()
