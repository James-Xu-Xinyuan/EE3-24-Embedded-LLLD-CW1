import smbus2
import time
import paho.mqtt.client as mqtt
import json
client = mqtt.Client()
#client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
client.connect("broker.mqttdashboard.com",port=1883)
client.publish("IC.embedded/LLLD/Device","hello")
# Get I2C bus
bus = smbus2.SMBus(1)

# LIS3DHTR address, 0x18(24)
# Select control register1, 0x20(32)
#		0x27(39)	Power ON mode, Data rate selection = 10 Hz
#					X, Y, Z-Axis enabled
bus.write_byte_data(0x18, 0x20, 0x27)
# LIS3DHTR address, 0x18(24)
# Select control register4, 0x23(35)
#		0x00(00)	Continuous update, Full-scale selection = +/-2G
bus.write_byte_data(0x18, 0x23, 0x00)

time.sleep(0.5)
while(1):
        # LIS3DHTR address, 0x18(24)
        # Read data back from 0x28(40), 2 bytes
        # X-Axis LSB, X-Axis MSB
        data0 = bus.read_byte_data(0x18, 0x28)
        data1 = bus.read_byte_data(0x18, 0x29)

        # Convert the data
        xAccl = data1 * 256 + data0
        if xAccl > 32767 :
                xAccl -= 65536

        # LIS3DHTR address, 0x18(24)
        #Read data back from 0x2A(42), 2 bytes
        # Y-Axis LSB, Y-Axis MSB
        data0 = bus.read_byte_data(0x18, 0x2A)
        data1 = bus.read_byte_data(0x18, 0x2B)

        # Convert the data
        yAccl = data1 * 256 + data0
        if yAccl > 32767 :
                yAccl -= 65536

        # LIS3DHTR address, 0x18(24)
        # Read data back from 0x2C(44), 2 bytes
        # Z-Axis LSB, Z-Axis MSB
        data0 = bus.read_byte_data(0x18, 0x2C)
        data1 = bus.read_byte_data(0x18, 0x2D)

        # Convert the data
        zAccl = data1 * 256 + data0
        if zAccl > 32767 :
                zAccl -= 65536
        xAccl -= 128
        yAccl += 1024
        zAccl -= 16320
        # Output data to screen
        '''
        print("Acceleration in X-Axis : %d" %xAccl)
        print("Acceleration in Y-Axis : %d" %yAccl)
        print("Acceleration in Z-Axis : %d" %zAccl)
        '''
        #acc_list = [xAccl,yAccl,zAccl]
        data_to_sent = json.dumps({'x':xAccl,'y':yAccl,'z':zAccl})
        print(data_to_sent)
        client.publish("IC.embedded/LLLD/Device",data_to_sent)
        time.sleep(0.4)
        


