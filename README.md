# import-status-page
 
This script is inspired by: https://github.com/mpepping/solarman-mqtt

The script collects the current data from the status page of your solar panel inverter

```lang=bash
usage: import_request.py

Collect data from your inverter status page and push them to mqtt

```

## How to get all required input for the config file

Create a new config file by copying the [sample config file](config.sample.json) and filling in the required information.

The first part covers your inverter admin page:

```lang=json
{
  "url": "http://10.10.10.255",
  "username": "",
  "password": "",
  [..]
}
```

* **url**: is the base URL of your local inverter page.
* **username**: is the username for the admin page of the inverter.
* **password**: is the password for the admin page, default is also admin


The second section covers the MQTT broker, to where the metrics will be published.

```lang=json
{
  [..]
  "broker": "mqtt.example.com",
  "port": 1883,
  "topic": "solarmanpv/status_page",
  "username": "",
  "password": ""
}
```

## MQTT attributes

The following attributes are published to the MQTT broker. The example output below use `solarmanpv/status_pages` as the topic, configured in the config file.

```lang=text
"webdata_now_p"
"webdata_today_e"
"webdata_total_e"
```

### example data

```lang=json
{"webdata_now_p": 93, "webdata_today_e": 1.3, "webdata_total_e": 2.6}
````

### Using Python

Run `pip install -r requirements.txt` and start `python3 import_status_page.py`.
