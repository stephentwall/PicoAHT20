import utime
import machine
from machine import Pin, I2C
import wlanConnect
import ahtx0

from umqtt.simple import MQTTClient
wlanConnect.connect2WLAN()
led = machine.Pin("LED", machine.Pin.OUT)

# I2C for the Wemos D1 Mini with ESP8266
i2c = I2C(0, scl=Pin(5), sda=Pin(4))

# Create the sensor object using I2C
sensor = ahtx0.AHT10(i2c)

#mqtt variables
mqtt_server = '10.0.0.225'
client_id = 'pico2w'
topic_pub_temp = b'pico/Temp'
topic_pub_humid = b'pico/Humidity'
topic_pub_avgTemp = b'pico/AvgTemp'
topic_pub_avgHumid = b'pico/AvgHumidity'
# Topic to subscribe to for receiving temperature offset
topic_sub_offset = b'pico/offset'
offset = 0

# Define a callback function for received messages
def sub_callback(topic, msg):
    """
    This function is called whenever a message is received.
    - topic: The topic the message was published on.
    - msg: The message payload.
    """
    print(f"New message on topic: {topic.decode('utf-8')}")
    decoded_msg = msg.decode('utf-8')
    print(f"Message: {decoded_msg}")

    # Add logic to act on the message
    global offset
    offset = float(decoded_msg)

# mqtt connection
def mqtt_connect():
   client = MQTTClient(client_id, mqtt_server, port=1883, keepalive=3600)
   client.set_callback(sub_callback)
   client.connect()
   print('Connected to %s MQTT Broker'%(mqtt_server))
   client.subscribe(topic_sub_offset)
   return client
def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   utime.sleep(5)
   machine.reset()
try:
   client = mqtt_connect()
except OSError as e:
   reconnect()
samples = 0
avgTemp = 0
avgHumid = 0
while True:
    led.on()
    utime.sleep(0.15)
    led.off()
    print("\nTemperature: %0.3f C" % sensor.temperature) #formatted_num = "{:.2f}".format(num)  # format to 2 decimal places
    print("Humidity: %0.3f %%" % sensor.relative_humidity)
    #send values to mqtt
    client.check_msg()
    print("offset = " + str(offset))
    temperature = "{:.2F}".format(((sensor.temperature * 9/5) +32) + offset) # sensor runs a bit high, + 1.1 degrees F
    humidity = "{:.2F}".format(sensor.relative_humidity)
    client.publish(topic_pub_temp, str(temperature))
    client.publish(topic_pub_humid, str(humidity))
    avgTemp = avgTemp + float(temperature)
    avgHumid = avgHumid + float(humidity)
    samples += 1
    if samples == 36 :
        avgTemp /= samples
        avgHumid /= samples
        client.publish(topic_pub_avgTemp, str("{:.2F}".format(avgTemp)))
        client.publish(topic_pub_avgHumid, str("{:.2F}".format(avgHumid)))
        avgTemp = int(0)
        avgHumid = int(0)
        samples = int(0)
        print("averages published")
    utime.sleep(5)
