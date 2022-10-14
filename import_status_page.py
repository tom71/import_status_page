#!/usr/bin/env python3
from distutils.command.config import config
from ssl import VERIFY_CRL_CHECK_LEAF
import requests
import logging
from paho.mqtt import client as mqtt_client
import random
import json
from requests.exceptions import ConnectTimeout


logging.basicConfig(level=logging.INFO)

VERSION = "1.0.0"

def load_config(file):
    """
    Load configuration
    :return:
    """
    with open(file, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        return config

client_id = f'python-mqtt-{random.randint(0, 1000)}'


start = '</script>\r\n<script type="text/javascript">'
end = "function initPageText"

def load_config():
    """
    Load configuration
    :return:
    """
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        return config

def connect_mqtt(config):

    broker = config["broker"]
    port = config["port"]
    username = config["username"]
    password = config["password"]

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT Broker!")
        else:
            logging.info("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def fetch_status(config):
    url = f'{config["url"]}/status.html'
    username = config["username"]
    password = config["password"]
    logging.info(f'Try to fetch status page from: {url}')
    try:
        response = requests.get(url, auth=(username, password), verify=False, timeout=5)
        if response.status_code == 200:
            s = response.text
            vars = s[s.find(start)+len(start):s.rfind(end)]

            webdata_now_p = None
            webdata_today_e = None
            webdata_total_e = None
            found = False
            for line in vars.split('\r\n'):
                if line.strip():
                    key = line.partition('=')[0][3:].strip().strip('\"')
                    value = line.partition('=')[2][:-1].strip().strip('\"')
                    if value:
                        if key == 'webdata_now_p' and value:
                            found = True # if we found one, set it to true 
                            webdata_now_p = int(value)
                        elif key == 'webdata_today_e' and value:
                            webdata_today_e = float(value)
                        elif key == 'webdata_total_e' and value:
                            webdata_total_e = float(value)    

            if found:
                json_body = {
                            "webdata_now_p": webdata_now_p,
                            "webdata_today_e": webdata_today_e,
                            "webdata_total_e": webdata_total_e,
                    }
                return json.dumps(json_body)
    except ConnectTimeout as error:           
        logging.warning(f'TimeoutError on fetch status page') 


def publish(client,topic,msg):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        logging.info(f"Send {msg} to {topic}")
    else:
        logging.error(f"Failed to send message to topic {topic}")

def run():
    config = load_config()
    msg = fetch_status(config)
    if msg:
        topic = config["mqtt"]["topic"]
        client = connect_mqtt(config["mqtt"])
        publish(client,topic,msg)

if __name__ == '__main__':
    run()
