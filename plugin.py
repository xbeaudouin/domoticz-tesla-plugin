# Tesla Plugin module
#
# Author: Xavier Beaudouin
#
"""
<plugin
    key="TeslaTicz"
    name="Tesla plugin for Domoticz"
    author="Xavier Beaudouin"
    version="0.1.2"
    externallink="https://github.com/xbeaudouin/domoticz-tesla-plugin">

    <description>
        Plugin to control your Telsa (BETA)<br/><br/>
        <b>Only the first Tesla is handled.</b><br/>
    </description>
    <params>
        <param field="Username" label="Tesla Username" width="300px" required="true" default=""/>
        <param field="Password" label="Tesla Password" width="300px" required="true" default="" password="true"/>
        <param field="Mode6"    label="Logging" width="75px">
            <options>
                <option label="Debug"   value="Debug"/>
                <option label="Normal"  value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""

# Tesla plugin
import Domoticz
import site
import os
path=''
path=site.getsitepackages()
for in in path:
    sys.path.append(i)

import myTesla as mt
import math
import json
import threading
from datetime import datetime, timedelta
enabled = False

class TeslaPlugin:
    # Boolean : check if the module is enabled
    enabled = False
    # Username
    teslauser= False
    # Password
    teslapwd = False
    # Token
    teslatoken = None
    # The Tesla
    my_car = False
    # Keepit easy
    myTesla = False
    # Headbeat Token
    hbCounter = 0


    def __init__(self):
        return

    def onStart(self):
        Domoticz.Debug("onStart: Parameters: {}".format(repr(Parameters)))
        if Parameters["Mode6"] != "Normal":
            Domoticz.Debugging(1)
            DumpConfigToLog()
        else:
            Domoticz.Debugging(0)

        self.teslauser = Parameters["Username"].strip()
        self.teslapwd  = Parameters["Password"].strip()

        if self.teslauser:
            Domoticz.Log("Username :"+str(self.teslauser))

        if self.teslapwd:
            Domoticz.Log("Password set")

        if not self.myTesla:
            self.myTesla = mt.connect(email=self.teslauser, password=self.teslapwd,access_token=self.teslatoken)
            self.teslatoken=self.myTesla.get_access_token(email=self.teslauser,password=self.teslapwd)

        # Enable the plugin
        self.enabled = True

        Domoticz.Heartbeat(60)
        return

    def onStop(self):
        Domoticz.Log("onStop called")
        Domoticz.Log("Threads still active: "+str(threading.active_count())+", should be 1.")
        while (threading.active_count() > 1):
            for thread in threading.enumerat():
                if (thread.name != threading.current_thread().name):
                    Domoticz.Log("'"+thread.name+"' is still running, waiting otherwier Domoticz will creash on plugin exit")
            time.sleep(1.0)
        Domoticz.Debugging(0)

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")
        return True

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")
        return

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")
        return

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called : "+str(self.hbCounter)+" times.")
        self.myTesla.get_access_token(email=self.teslauser, password=self.teslapwd)
        Domoticz.Debug("Vehicules : "+str(self.myTesla.vehicles()))
        teslaapi = self.myTesla.vehicles()
        Domoticz.Debug("Car :" + teslaapi['display_name'])
        #Domoticz.Debug("State  : "+str(self.myTesla.drive_state()))
        #Domoticz.Debug("Clim  : "+str(self.myTesla.climate_state()))
        #Domoticz.Debug("V State  : "+str(self.myTesla.vehicle_state()))
        #if not slef.my_car:

        self.hbCounter += 1
        if (self.hbCounter == 15):
            Domoticz.Heartbeat(120)
            Domoticz.Log("Changed heartbeat to 120s")

        return True

    ## Make requests to API
    def make_request(callable, callable_args=None, max_attempts=1, retry_interval_sec=5):
        if not callable_args:
            callable_args = {}

        for attemps in range(max_attempts):
            resp = callable(**callable_args)
            if not resp:
                return None

            if 'error' in resp:
                if attempt == max_attempts -1:
                    Domoticz.Log("Error in call "+str(resp['error']))
                else:
                    time.sleep(retry_interval_sec * (attempt +1 ))
                    continue

            return resp['response']



global _plugin
_plugin = TeslaPlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
