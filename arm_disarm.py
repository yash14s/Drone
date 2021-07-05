from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
import socket
import exceptions

def connect_to_python():
    global vehicle
    vehicle = connect('com6', wait_ready=False, baud=57600)
    print("Connected")

def disconnect_to_python():
    vehicle.close()
    print("Disconnected")
    
def arm_and_disarm():
    while vehicle.is_armable!=True:
        print("Waiting for the vehicle to become armable")
        time.sleep(1)

    print('Vehicle is now armable')
    vehicle.mode=VehicleMode('GUIDED')
    while vehicle.mode!='GUIDED':
        print("Waiting for drone to enter GUIDED flight mode")
        time.sleep(1)

    print("Vehicle now in GUIDED MODE.")

    vehicle.armed=True

    while vehicle.armed==False:
        print("Waiting for vehicle to become armed")
        time.sleep(1)

    print("Caution! Drone is ARMED!")
    time.sleep(5)
    
    print("Proceeding to disarm")
    vehicle.armed = False
    while(vehicle.armed==True):
        time.sleep(1)
    print("Drone is now DISARMED")

connect_to_python()
arm_and_disarm()
disconnect_to_python()
