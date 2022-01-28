from dronekit import connect
from dronekit.mavlink import MAVConnection
import time

def connect_to_python():
    global vehicle
    vehicle = connect('/dev/ttyUSB0', wait_ready=False, baud=57600)
    #TCP:
    gcs_tcp = MAVConnection('tcpin:0.0.0.0:49152', source_system=1)
    vehicle._handler.pipe(gcs_tcp)
    gcs_tcp.master.mav.srcComponent = 1
    gcs_tcp.start()
    print("Connected")
    
    #UDP:
    #gcs_udp = MAVConnection('udpin:0.0.0.0:15667', source_system=1)
    #vehicle._handler.pipe(gcs_udp)
    #gcs_udp.master.mav.srcComponent = 1
    #gcs_udp.start()

def disconnect_to_python():
    vehicle.close()
    print("Disconnected")

connect_to_python()
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
    
disconnect_to_python()
