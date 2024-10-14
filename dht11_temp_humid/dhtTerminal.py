import time
import board
import adafruit_dht

# Initialize the DHT device with use_pulseio=False for Raspberry Pi compatibility
dhtDevice = adafruit_dht.DHT11(board.D21)

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temperature [C] {:.1f}  Humidity: {}% ".format(temperature_c, humidity)
        )

    except RuntimeError as error:
        # Errors happen fairly often with DHT sensors, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
