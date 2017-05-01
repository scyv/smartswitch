import signal
import sys
import time
import logging
import paho.mqtt.client as mqtt
import json
from rpi_rf import RFDevice

import Codes

GPIO = 27
MQTT_HOST = "192.168.10.23"
TOPIC_SWITCH_STATUS = "de.scyv/smartswitch/status"


# The callback for when the client receives a CONNACK response from the server.
def on_mqtt_connect(client, userdata, flags, rc):
    logging.info("Connected to MQTT with result code " + str(rc))


# pylint: disable=unused-argument
def exithandler(signal, frame):
    mqtt_client.loop_stop()
    rfdevice.cleanup()
    sys.exit(0)


def get_status_from_code(code):
    status = None
    for switch, dict_code in Codes.CODES_ON.items():
        if (dict_code == code):
            status = {
                "switch": switch,
                "status": "on"
            }
            break

    if not status:
        for switch, dict_code in Codes.CODES_OFF.items():
            if (dict_code == code):
                status = {
                    "switch": switch,
                    "status": "off"
                }
                break

    return status


def code_received(code):
    status = get_status_from_code(code)
    mqtt_client.publish(TOPIC_SWITCH_STATUS, json.dumps(status))


# Create an MQTT client and attach our routines to it.
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_mqtt_connect

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

signal.signal(signal.SIGINT, exithandler)
rfdevice = RFDevice(GPIO)
rfdevice.enable_rx()
logging.info("Listening for codes on GPIO " + str(GPIO))
timestamp = None
mqtt_client.loop_start()
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        code_received(rfdevice.rx_code)
        logging.info("Received: " + str(rfdevice.rx_code))
    time.sleep(0.1)
