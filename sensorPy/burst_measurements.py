import time
from dht11.SensorDHT11 import DHT11
from dht22.SensorDHT22 import DHT22
from shtc3.SensorSHTC3 import SHTC3


def main():
    dht11 = DHT11(21)
    dht22 = DHT22(16)
    shtc3 = SHTC3()

    while True:
        dht11.measure(True)
        dht22.measure(True)
        shtc3.measure(True)
        time.sleep(1)
 

if __name__ == "__main__":
    main()