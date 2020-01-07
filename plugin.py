# Tesla Plugin module
#
# Author: Xavier Beaudouin
#
"""
<plugin
    key="TeslaTicz"
    name="Tesla plugin for Domoticz"
    author="Xavier Beaudouin"
    version="0.1.1"
    externallink="https://github.com/xbeaudouin/domoticz-tesla-plugin">

    <description>
        Plugin to control your Telsa
        <br/>
    </description>
    <params>
        <param field="Username" label="Tesla Username" width="300px" required="true" default=""/>
        <param field="Password" label="Tesla Password" width="300px" required="true" default="" password="true"/>
        <param field="Mode1"    label="VIN" width="300px" default=""/>
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
import myTesla as mt
import math
from datetime import datetime, timedelta

class TeslaPlugin:
    # Boolean : check if the module is enabled
    enabled = False
    # Username
    teslauser= False
    # Password
    teslapwd = False
    # VIN for this module
    teslavin = False
    # Token
    teslatoken = False
    # The Tesla
    my_car = False
    # Keepit easy
    myTesla = False


    def __init__(self):
        pass

    def onStart(self):
        Domoticz.Debug("onStart: Parameters: {}".format(repr(Parameters)))
        if Parameters["Mode6"] != "Normal":
            Domoticz.Debugging(1)
            DumpConfigToLog()
        else:
            Domoticz.Debugging(0)

        self.teslauser = Parameters["Username"].strip()
        self.teslapwd  = Parameters["Password"].strip()
        self.teslavin  = Parameters["Mode1"].strip()

        if self.teslauser:
            Domoticz.Log("Username :"+str(self.teslauser))

        if self.teslapwd:
            Domoticz.Log("Password set")

        if self.teslavin:
            Domoticz.Log("VIN Set to : "+str(self.teslavin))
        else:
            Domoticz.Log("No VIN Set, use the first vehicle found")

        if not self.myTesla:
            self.myTesla = mt.connect(self.teslauser, self.teslapwd)

        # Enable the plugin
        self.enabled = True

        Domoticz.Heartbeat(300)

    def onStop(self):
        Domoticz.Log("onStop called")
        Domoticz.Debugging(0)

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        self.myTesla.get_access_token(email=self.teslauser, password=self.teslapwd)
        Domoticz.Log("Vehicules : "+str(self.myTesla.vehicles()))

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
