import bge
import liblo
import math
import os

from . import maths
"""
A sound source game object to communicate with SATIE audio engine.
Needs to be attached to a 3D object in BGE
"""
class Satie(bge.types.KX_GameObject):
    """Represents an instance of a SATIE sound source"""
    def __init__(self, old_owner, parent, listener):
        """Initialize some values

        Arguments:
        parent -- KX_GameObject 
        listener -- KX_GamerObject

        A parent is, typically, a visible 3D object that will be associated with
        the sound.
        A listener is a virtual microhone in the scene (typically a local user)

        The spacialisation parameters are computed according the 3D space relationship
        between the parent to which the sound source is attached and the listener.
        """
        self.oscAddy = liblo.Address("127.0.0.1", 18032)
        self.satieID = None
        self.satieGroup = None
        self.satieSynth = None
        #self.myParent = parent
        self.listener = listener
        self.setParent(bge.logic.activeObjects[parent])
        
    def update(self):
        """update the information about position and send cooked AZI values to SATIE"""
        msg = self._getAED()
        azi = math.degrees(msg[0])
        ele = math.degrees(msg[1])
        gain = msg[2]
        # print("azi, ele, gain: {}, {}, {}".format(azi, ele, gain))
        liblo.send(self.oscAddy, os.path.join("/SATIE", self.satieGroup, self.satieID), "set", "aziDeg", azi, "eleDeg", ele, "gainDB", gain)

    def makeInstance(self, satieGroup, satieID, satieSynth):
        """instantiate a sound source

        Arguments:
        satieGroup -- a symbol
        satieID -- a symbol
        satieSynth -- a symbol

        satieGroup will be created automatically by SATIE if it does not exist.

        satieID should be a unique identifier for the instance and will be
        passed to SATIE as well as used in blender

        satieSynth is a symbolic name for the audio source of effect, as defined in SATIE system.
        """
        self.satieGroup = satieGroup
        self.satieID = satieID
        self.satieSynth = satieSynth
        self.makeSatieGroup()
        self.makeSatieInstance()

    def makeSatieGroup(self):
        """Tell SATIE to create a synth or effect group. SATIE will do nothing if group exists already"""
        liblo.send(self.oscAddy, "/SATIE", "create", self.satieGroup)

    def makeSatieInstance(self):
        """Tell SATIE to create and instance of a synth"""
        liblo.send(self.oscAddy, os.path.join("/SATIE", self.satieGroup), "create", self.satieID, self.satieSynth)
        liblo.send(self.oscAddy, os.path.join("/SATIE", self.satieGroup, self.satieID), "set", "gainDB", -60)

    def deleteInstance(self):
        liblo.send(self.oscAddy, os.path.join("/SATIE", self.satieGroup, self.satieID), "delete")

    def setParam(self, param, value):
        liblo.send(self.oscAddy, os.path.join("/SATIE", self.satieGroup, self.satieID), "set", param, value)

    def _getLocation(self):
        # parent = self.parent
        print(bge.logic.activeObjects)
        location = self.worldPosition
        return location

    def _getAED(self):
        distance = self._getLocation() - bge.logic.activeObjects[self.listener.name].worldPosition
        print("distance", distance)
        aed = maths.xyz_to_aed(distance)
        gain = math.log(maths.distance_to_attenuation(aed[2])) * 20
        aed[2] = gain
        return aed
    
