# wifi.py

# default value for wifi timeout = 5000
def connect(ssid, password, timeout=5000):
    import network, time
    wifi = network.WLAN(network.STA_IF)
    
    if not wifi.isconnected():
        print("Connecting to WiFi network...")
        wifi.active(True)
        wifi.connect(ssid, password)
        # Wait until connected
        t = time.ticks_ms()
        while not wifi.isconnected():
            if time.ticks_diff(time.ticks_ms(), t) > timeout:
                wifi.disconnect()
                print("Timeout. Could not connect.")
                return False
        print("Successfully connected to " + ssid)
        return True
    else:
        print("Already connected")
        return True
