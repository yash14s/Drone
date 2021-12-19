from dronekit import connect
from dronekit.mavlink import MAVConnection
import time

def connect_to_python():
    global vehicle
    vehicle = connect('/dev/ttyUSB0', wait_ready=False, baud=57600)
    gcs_tcp = MAVConnection('tcpin:0.0.0.0:49152', source_system=1)
    vehicle._handler.pipe(gcs_tcp)
    gcs_tcp.master.mav.srcComponent = 1
    gcs_tcp.start()
    print("Connected")

def disconnect_to_python():
    vehicle.close()
    print("Disconnected")
    
def print_lidar_reading():
    connect_to_python()
    while True:
        try:
            print("Barometer: ", vehicle.location.global_relative_frame.alt)
            print("LiDAR: ", vehicle.rangefinder.distance)
            time.sleep(1)
        except KeyboardInterrupt:
            disconnect_to_python()
            break

print_lidar_reading()
