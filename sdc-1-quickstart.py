from __future__ import print_function
import binascii
import struct
import time
import yaml
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, UUID

DISCOVERY_UUID = UUID("9DFACA9D-7801-22A0-9540-F0BB65E824FC")
SPIN_SERVICE_UUID = UUID("5E5A10D3-6EC7-17AF-D743-3CF1679C1CC7")
COMMAND_CHARACTERISTIC_UUID = UUID("92E92B18-FA20-D486-5E43-099387C61A71")
ACTION_CHARACTERISTIC_UUID = UUID("182BEC1F-51A4-458E-4B48-C431EA701A3B")
UUID_CLIENT_CHARACTERISTIC_CONFIG = UUID("00002902-0000-1000-8000-00805f9b34fb")

# Load the strings from the yaml file
with open("strings.yaml", "r") as stream:
    try:
        strings = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

class ScanDelegate(DefaultDelegate):
    """
    If a new device is found during scanning, it will be handled by the handleDiscovery def in here
    """
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            # Unfortunately we can't stop() the Scanner (in case the right device is found) at this point: It will raise an error :(
            print(" ", end="\r") #just an empty print to prevent errors because of an empty if
        elif isNewData:
            # Never seen this happen, but it case it does, we'll get some output ;)
            print("Received new data from " + dev.addr)


class NotificationDelegate(DefaultDelegate):
    """
    If a notification is received, it will be handled by the handleNotification def in here
    """
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global strings
        print(strings["action"][ord(data)] + (" " * 15), end="\r")

# Scan for 10 seconds
print("Scanning for the next 10 seconds, please wait...", end="\r")
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

# Prepare some variables for later use
device = None
peripheral = None

# We should have found some devices by now, walk through the list to look for a SPIN Remote
for dev in devices:

    # Create an Peripheral object for this device in order to get the services
    peripheral = Peripheral(dev)
    services = peripheral.getServices()
    
    # Walk through the list of services to see if one of them matches the DISCOVERY_UUID
    for service in services:
        if service.uuid == DISCOVERY_UUID:
            # We now know for sure we're dealing with a SPIN Remote! Store the device in our premade variable and stop looking
            device = dev
            print("Device " + dev.addr + " (" + dev.addrType + "), RSSI=" + str(dev.rssi) + " dB")
    
    # If we're not dealing with a SPIN, we can disconnect the peripheral and reuse the variable
    if device == None:
        peripheral.disconnect()
    else:
        break

if device != None:
    # Prep the peripheral for receiving notifications
    peripheral.withDelegate(NotificationDelegate())

    # Get the list of services again, to perform some more checks
    services = peripheral.getServices() #takes the cached list, no worries!

    # Walk through the list of services to see if one of them matches the SPIN_SERVICE_UUID
    for service in services:
        if service.uuid == SPIN_SERVICE_UUID:

            # Look for the characteristic to send commands to
            commandCharacteristic = service.getCharacteristics(COMMAND_CHARACTERISTIC_UUID)
            if commandCharacteristic:

                # Override and cancel the LED three times
                for i in range(0, 3):
                    # Set the LED to red and request a confirmation (will throw an error if writing went wrong)
                    # 0x09 = commandId (set LED color),
                    # 0xFF, 0x00, 0x00 = RGB
                    commandCharacteristic[0].write(struct.pack('<bBBB', 0x09, 0xFF, 0x00, 0x00), True)
                    time.sleep(.5)
                    # Cancel the LED override
                    # Note that this code is only meant to demonstrate how to cancel the LED override. The SPIN remote will automatically return to the active profile LED color when the connection is closed.
                    commandCharacteristic[0].write(struct.pack('<b', 0x07), True)
                    time.sleep(.5)

            # Look for the characteristic to receive actions from
            actionCharacteristic = service.getCharacteristics(ACTION_CHARACTERISTIC_UUID)
            if actionCharacteristic and commandCharacteristic:

                # Get config descriptor
                descriptors = actionCharacteristic[0].getDescriptors(UUID_CLIENT_CHARACTERISTIC_CONFIG)

                # Enable notifications
                commandCharacteristic[0].write(struct.pack('<bb', 0x08, 0x01), True)
                descriptors[0].write(struct.pack('<bb', 0x01, 0x00), True)

            # Keep on receiving notifications
            while True:
                peripheral.waitForNotifications(1.0)
            break