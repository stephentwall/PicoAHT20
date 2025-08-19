import network
import time

def connect2WLAN():
    ssid = '9CDA2'
    password = '5057711982'

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        print('connection failed')
        if wlan.status() == -3:
            print('Wrong Password')
        elif wlan.status() == -2:
            print('AP not found')
        else:
            print(f"Status code: {wlan.status()}")
    else:
        print('connected2wifi')
        print('network config:', wlan.ifconfig())
