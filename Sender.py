# import argparse
import logging
import Codes

from rpi_rf import RFDevice
import paho.mqtt.client as mqtt
import json

GPIO = 17
PROTOCOL = "default"
PULSELENGTH = "default"
MQTT_HOST = "192.168.10.25"
TOPIC_SWITCH_COMMAND = "de.scyv/smartswitch/cmd"
TOPIC_SWITCH_STATUS = "de.scyv/smartswitch/status"

# The callback for when the client receives a CONNACK response from the server.
def on_mqtt_connect(client, userdata, flags, rc):
    print("Connected to MQTT with result code " + str(rc))
    # listen for commands coming from the mqtt bus
    client.subscribe(TOPIC_SWITCH_COMMAND)


# The callback for when a PUBLISH message is received from the server.
def on_mqtt_message(client, userdata, msg):
    payload_json = json.loads(msg.payload.decode('ascii'))

    switch = payload_json.switch
    status = payload_json.status

    code = None
    if (status == "on"):
        code = Codes.CODES_ON[switch]
    elif (status == "off"):
        code = Codes.CODES_OFF[switch]

    if (code):
        logging.info("Send Code: " + str(code))
        rfdevice.tx_code(code, PROTOCOL, PULSELENGTH)



# Create an MQTT client and attach our routines to it.
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_mqtt_connect
mqtt_client.on_message = on_mqtt_message


logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

# parser = argparse.ArgumentParser(description='Sends a decimal code via a 433/315MHz GPIO device')
# parser.add_argument('code', metavar='CODE', type=int,
#                    help="Decimal code to send")
# parser.add_argument('-g', dest='gpio', type=int, default=17,
#                    help="GPIO pin (Default: 17)")
# parser.add_argument('-p', dest='pulselength', type=int, default=None,
#                    help="Pulselength (Default: 350)")
# parser.add_argument('-t', dest='protocol', type=int, default=None,
#                    help="Protocol (Default: 1)")
# args = parser.parse_args()

rfdevice = RFDevice(GPIO)
rfdevice.enable_tx()

mqtt_client.connect(MQTT_HOST, 1883, 60)

try:
    # Process network traffic and dispatch callbacks.
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    pass

rfdevice.cleanup()
