# SmartPlug_Example.py
import pyHS100
from pyHS100 import Discover, SmartPlug
# More info on pyHS100, see https://github.com/GadgetReactor/pyHS100

# Discover all available devices
for dev in pyHS100.Discover.discover().values():
    print(dev)
    # Only need IP address from this info

# New plug defined by IP address in local network
plug = SmartPlug("IPaddress")
    # Giving the plug a name
plug.alias = "Name"   # For example
    # Current state of plug:
print(plug.state)
    # Turning the plug on and off
plug.turn_off()
plug.turn_on()
