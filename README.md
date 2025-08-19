# Pico W AHT20 Temperature & Humidity MQTT Publisher

This project uses a Raspberry Pi Pico W and an AHT20 sensor to read temperature and humidity data. It then connects to a local WiFi network and publishes this data to an MQTT broker. It also subscribes to a topic to receive a temperature offset value.

## Features

- Reads temperature (in Celsius) and relative humidity from an AHT20 sensor.
- Converts temperature to Fahrenheit.
- Connects to a specified WiFi network.
- Publishes sensor data to distinct MQTT topics.
- Calculates and publishes the average temperature and humidity over a set number of samples (36 samples, or ~3 minutes).
- Subscribes to an MQTT topic (`pico/offset`) to dynamically adjust the temperature reading with an offset.
- Blinks the onboard LED on each reading cycle.

## Hardware Requirements

- Raspberry Pi Pico W
- AHT20 Temperature and Humidity Sensor (on a breakout board)
- Breadboard and jumper wires

### Wiring

The AHT20 sensor communicates over I2C. Connect it to the Pico as follows:

| AHT20 Pin | Pico Pin | Description      |
|-----------|----------|------------------|
| VIN       | 3V3 (OUT)| 3.3V Power       |
| GND       | GND      | Ground           |
| SCL       | GP5      | I2C0 Clock       |
| SDA       | GP4      | I2C0 Data        |

## Software & Dependencies

This project is written in MicroPython.

### Project Files

- `main.py`: The main application logic.
- `wlanConnect.py`: A helper module to connect to WiFi (You must create this file).
- `ahtx0.py`: The driver library for the AHT20 sensor.

### Libraries

You will need to install the following libraries onto your Pico's filesystem:

- `ahtx0.py`: The sensor driver. You can find it here.
- `umqtt.simple`: Part of `micropython-lib`. You can install it using `upip` on the Pico:
  ```python
  import upip
  upip.install('micropython-umqtt.simple')
  ```

## Configuration

1.  **WiFi Credentials**: Create a file named `wlanConnect.py` in the root of your Pico's filesystem with your network's SSID and password.

2.  **MQTT Settings**: In `main.py`, update the following variables to match your environment:
    - `mqtt_server`: The IP address or hostname of your MQTT broker.
    - `client_id`: A unique ID for this MQTT client.
    - `topic_pub_*`: The topics where sensor data will be published.
    - `topic_sub_offset`: The topic to listen on for temperature offset adjustments.

## Usage

1.  Ensure all hardware is wired correctly.
2.  Copy the project files (`main.py`, `ahtx0.py`, `wlanConnect.py`) to your Pico W's filesystem.
3.  Power on the Pico. It will automatically connect to WiFi and the MQTT broker, then begin sending sensor data every 5 seconds.
4.  To apply a temperature offset, publish a numeric value (e.g., `-1.5`) to the `pico/offset` MQTT topic.