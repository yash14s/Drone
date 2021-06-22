from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
import socket
import exceptions
import math
import argparse

def connectMyCopter():
    parser=argparse.ArgumentParser(description='commands')
    parser.add_argument('--connect')
    args=parser.parse_args()
    
    connection_string=args.connect
    
    if not connection_string:
        import dronekit_sitl
        sitl=dronekit_sitl.start_default()
        connection_string=sitl.connection_string()
    
    vehicle=connect(connection_string,wait_ready=True)
    return vehicle

vehicle = connect('com6', wait_ready=True, baud=57600)
print("Connected")

def arm_and_disarm(targetHeight):
    while vehicle.is_armable!=True:
        print("Waiting for the vehicle to become armable")
        time.sleep(1)

    print('Vehicle is now armable')
    vehicle.mode=VehicleMode('GUIDED')
    while vehicle.mode!='GUIDED':
        print("Waiting for drone to enter GUIDED flight mode")
        time.sleep(1)

    print("Vehicle now in GUIDED MODE. Have fun!!")

    vehicle.armed=True

    while vehicle.armed==False:
        print("Waiting for vehicle to become armed")
        time.sleep(1)

    print("Look out! Virtual props are spinning!!")
    
    vehicle.simple_takeoff(targetHeight)#meters
    while True:
        print("Current Altitude: %d"%vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt>=.95*targetHeight:
            break
        time.sleep(1)
    print("Target altitude reached!!")
    return None

    vehicle.armed = False
    while(vehicle.armed==True):
        time.sleep(1)
    print("Vehicle disarmed")

arm_and_disarm(10)
