import json
from tqdm import tqdm


"""  
[module: vehicle_handling]

This module is used to change each vehicle in the data
to an object for better queyring later on.
"""

class Vehicle:
    def __init__(self, vehicleNumber, routeId, varId, tripList):
        self._vehicleNumber = vehicleNumber
        self._routeId = routeId
        self._varId = varId
        self._tripList = tripList

    @property
    def getVehicleNumber(self):
        return self._vehicleNumber
    @getVehicleNumber.setter
    def setVehicleNumber(self, vehicleNumber):
        self._vehicleNumber = vehicleNumber
    
    @property
    def getRouteId(self):
        return self._routeId
    @getRouteId.setter
    def setRouteId(self, routeId):
        self._routeId = routeId
    
    @property
    def getVarId(self):
        return self._varId
    @getVarId.setter
    def setVarId(self, varId):
        self._varId = self._varId
    
    @property
    def getTripList(self):
        return self._tripList
    @getTripList.setter
    def setTripList(self, tripList):
        self._tripList = tripList


class VehicleQuery:
    def __init__(self, fileName):
        self.vehicleList = []
        self.loadJson(fileName)
        
    def loadJson(self, fileName):
        with open(f"jsonFiles/{fileName}", "r") as file:
            for line in file:
                data = json.loads(line)              
                vehicle = Vehicle(**data)
                self.vehicleList.append(vehicle)

    
        