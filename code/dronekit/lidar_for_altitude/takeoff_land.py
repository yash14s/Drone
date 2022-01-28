from dronekit import connect, VehicleMode, LocationGlobalRelative
from dronekit.mavlink import MAVConnection
import time
import exceptions
import math

def connect_to_vehicle():
    global vehicle
    vehicle = connect('/dev/ttyUSB0', wait_ready=False, baud=57600)
    gcs_tcp = MAVConnection('tcpin:0.0.0.0:49152', source_system=1)
    vehicle._handler.pipe(gcs_tcp)
    gcs_tcp.master.mav.srcComponent = 1
    gcs_tcp.start()
    print("Connected")

def disconnect_to_vehicle():
    vehicle.close()
    print("Disconnected")
    
def arm():
    connect_to_vehicle()
    while vehicle.is_armable!=True:
        print("Undergoing pre-arm checks")
        time.sleep(1)
    print('Drone is now armable')
    vehicle.mode=VehicleMode('GUIDED')
    while vehicle.mode!='GUIDED':
        print("Waiting for drone to enter GUIDED flight mode")
        time.sleep(1)
    print("Drone now in GUIDED MODE.")
    vehicle.armed=True
    while vehicle.armed==False:
        print("Waiting for drone to become armed")
        time.sleep(1)
    print("Caution! Drone is ARMED!")

def disarm():    
    print("Proceeding to disarm")
    vehicle.armed = False
    while(vehicle.armed==True):
        time.sleep(1)
    print("Drone is now DISARMED")
    
def takeoff(targetHeight):
    arm()
    vehicle.simple_takeoff(targetHeight)#meters
    while True:
        print("Lidar: %f"%vehicle.rangefinder.distance)
        if vehicle.rangefinder.distance>=.91*targetHeight:
            break
        time.sleep(1)
    print("Target altitude reached!!")
    
def land():
    vehicle.mode=VehicleMode("LAND")
    while vehicle.mode != 'LAND':
        print("Waiting for drone to enter LAND mode")
        time.sleep(1)
    print("Vehicle in LAND mode")
    disarm()
    
def takeoff_land(targetHeight):
    takeoff(targetHeight)
    land()
    disconnect_to_vehicle()
    
takeoff_land(1.8)
