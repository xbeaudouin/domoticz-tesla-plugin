# Tesla Plugin module
#
# Author: Xavier Beaudouin
#
"""
<plugin
    key="TeslaTicz"
    name="Tesla plugin for Domoticz"
    author="Xavier Beaudouin"
    version="0.1.0"
    externallink="https://github.com/xbeaudouin/domoticz-tesla-plugin">

    <description>
        Plugin to control your Telsa
        <br/>
    </description>
    <params>
        <param field="Username" label="Tesla Username" width="300px" default=""/>
        <param field="Password" label="Tesla Password" width="300px" default="" password="true"/>
        <param field="Mode1"    label="VIN" width="300px" default=""/>
        <param field="Mode6"    label="Logging" width="75px">
            <options>
                <option label="Verbose" value="Verbose"/>
                <option label="Debug"   value="Debug"/>
                <option label="Normal"  value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""

errmsg = ""
try:
    import Domoticz
except Exception as e:
        errmsg += "Domoticz core start error: "+str(e)
try:
    import myTesla
except Exception as e:
        errmsg += "myTesla import error: "+str(e)

import math
from datetime import datetime, timedelta

pluginDebug = True

def Debug(msg):
    if pluginDebug:
        Domoticz.Debug(msg)


class Plugin:
    # Boolean : check if the module is enabled
    enabled = False

    def __init__(self):
        #self.var = 123
        self.debuging = False
        self.telsauser = ""
        self.telsapwd = ""
        self.telsatoken = ""
        self.date = datetime.now()
        self.lastupdate = self.date
        self.updatefrequency = 1
        return

    def onStart(self):
        if errmsg == "":
            try:
                Domoticz.Heartbeat(10)
                global pluginDebug
                pluginDebug = False

                self.debugging = Parameters["Mode6"]
                if self.debugging == "Verbose":
                    Domoticz.Debugging(2+4+8+16+64)
                    pluginDebug = True
                if self.debugging == "Debug":
                    Domoticz.Debugging(2)
                    pluginDebug = True
                    DumpConfigToLog()
                else:
                    Domoticz.Debugging(0)

                Debug("onStart: Parameters: {}".format(repr(Parameters)))
                self.teslauser = Parameters["Username"].strip()
                self.teslapwd  = Parameters["Password"].strip()
                self.vin       = Parameters["Mode1"].strip()

                if self.teslauser:
                    Domoticz.Log("Username :"+str(self.teslauser))

                if self.teslapwd:
                    Domoticz.Log("Password set")

                if self.vin:
                    Domoticz.Log("VIN Set to : "+str(self.vin));

                # Most init
                self.__init__()

                # Enable the plugin
                self.Enabled = True

                ## Encore
            except Exception as e:
                Domoticz.Error("onStart: {}".format(str(e)))
        else:
            Domoticz.Error("onStart: Domoticz Python env error {}".format(errmsg))

    def debug(self, flag):
        global pluginDebug
        pluginDebug = flag

    def onStop(self):
        Domoticz.Log("onStop called")
        Domoticz.Debugging(0)

    #def onConnect(self, Connection, Status, Description):
    #    Domoticz.Log("onConnect called")

    #def onMessage(self, Connection, Data):
    #    Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    #def onDisconnect(self, Connection):
    #    Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")

global _plugin
_plugin = Plugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

#def onConnect(Connection, Status, Description):
#    global _plugin
#    _plugin.onConnect(Connection, Status, Description)

#def onMessage(Connection, Data):
#    global _plugin
#    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

#def onDisconnect(Connection):
#    global _plugin
#    _plugin.onDisconnect(Connection)

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
