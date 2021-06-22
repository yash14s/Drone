from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
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

def arm_and_takeoff(targetHeight):
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

	print("Virtual props are spinning!!")
	
	vehicle.simple_takeoff(targetHeight)#meters
	while True:
		print("Current Altitude: %d"%vehicle.location.global_relative_frame.alt)
		if vehicle.location.global_relative_frame.alt>=.95*targetHeight:
			break
		time.sleep(1)
	print("Target altitude reached!!")
	return None

def get_distance_meters(targetLocation,currentLocation):
	dLat=targetLocation.lat - currentLocation.lat
	dLon=targetLocation.lon - currentLocation.lon
	dAlt=targetLocation.alt - currentLocation.alt
	return math.sqrt((dLon*dLon)+(dLat*dLat)+(dAlt*dAlt))

def goto(targetLocation):
	distanceToTargetLocation=get_distance_meters(targetLocation,vehicle.location.global_relative_frame)
	vehicle.simple_goto(targetLocation)
	currentDistance = get_distance_meters(targetLocation,vehicle.location.global_relative_frame)
	while currentDistance>distanceToTargetLocation*.01:
		currentDistance = get_distance_meters(targetLocation,vehicle.location.global_relative_frame)
		time.sleep(1)
	print("Reached target location")
	return None
	
###python connection_template.py --connect 127.0.0.1:14550

wp1=LocationGlobalRelative(22.714314,75.899804,1)#1 metres above start point
wp2=LocationGlobalRelative(22.714316,75.899428,1)
wp3=LocationGlobalRelative(22.713519,75.899408,1)
wp4=LocationGlobalRelative(22.713511,75.899820,1) 


vehicle=connectMyCopter()
arm_and_takeoff(1)

goto(wp1)
goto(wp2)
goto(wp3)
goto(wp4)
goto(wp1)

vehicle.mode=VehicleMode("LAND")
while vehicle.mode != 'LAND':
	print("Waiting for drone to enter LAND mode")
	time.sleep(1)
print("Vehicle in LAND mode")

while True:
	time.sleep(1)

