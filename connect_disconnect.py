# -*- coding: utf-8 -*-
"""
Created on Mon May 10 18:16:15 2021

@author: Yash
"""

from dronekit import connect
import time

print("Waking up")
time.sleep(3)

vehicle = connect('com6', wait_ready=True, baud=57600)
print("Connected")

time.sleep(2)

print("Disconnecting...")
vehicle.close()
print("Connection closed")
