import os
import csv
import time
import datetime
import adafruit_dht
import board

# Configuration variables
pin = board.D4
time_interval = 5 * 60  # Time interval between bursts in seconds
read_burst_num = 5  # Number of readings in each burst
read_delay = 2  # Delay between each reading in the burst

def initialize_sensor(pin):
    """Initialize the DHT11 sensor."""
    return adafruit_dht.DHT11(pin), "DHT11"

def burst_read(sensor, read_burst_num, read_delay):
    """Perform a burst of readings from the sensor."""
    temp_measurements = []
    hum_measurements = []
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    for iMeasurement in range(read_burst_num):
        try:
            temperature = sensor.temperature
            humidity = sensor.humidity
            if temperature is not None and humidity is not None:
                temp_measurements.append(temperature)
                hum_measurements.append(humidity)
            else:
                print("Failed to retrieve data from sensor")
        except RuntimeError as error:
            print(error.args[0])
        except Exception as error:
            raise error
        time.sleep(read_delay)
    return current_time, temp_measurements, hum_measurements

def print_measurements(current_time, temp_measurements, hum_measurements, sensor_name):
    """Print the measurements in a scientific and visually appealing way."""
    temp_color, hum_color, reset_color = "\033[91m", "\033[94m", "\033[0m"  # Red, Blue, Reset
    degree_sign = "\u00B0"  # Unicode for degree symbol

    print(f"\nSensor: {sensor_name} | Time: {current_time}")
    
    # Temperature section
    if temp_measurements:
        temp_measurements = [float(temp) for temp in temp_measurements]
        print(f"{temp_color}Temperature [{degree_sign}C]{reset_color}")
        avg_temp = sum(temp_measurements) / len(temp_measurements)
        print(f"  Measurements: {temp_color}{temp_measurements}{reset_color}")
        print(f"  Average: {temp_color}{avg_temp:.2f}{degree_sign}C{reset_color}")
        
    # Humidity section
    if hum_measurements:
        hum_measurements = [float(hum) for hum in hum_measurements]
        print(f"{hum_color}Humidity [%]{reset_color}")
        avg_hum = sum(hum_measurements) / len(hum_measurements)
        print(f"  Measurements: {hum_color}{hum_measurements}{reset_color}")
        print(f"  Average: {hum_color}{avg_hum:.2f}%{reset_color}")
    print("")

def dump_to_csv(directory, current_time, avg_temp, avg_hum, sensor_name):
    """Dump the measurements to a CSV file."""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name = f"{date_str}_{sensor_name}.csv"
    file_path = os.path.join(directory, file_name)
    
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    file_exists = os.path.isfile(file_path)
    
    try:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                print(f"Creating new CSV file: {file_path}")
                writer.writerow(["hour", "min", "sec", "avg_temp", "avg_hum"])
            hour, minute, second = current_time.split(":")
            writer.writerow([hour, minute, second, f"{avg_temp:.2f}", f"{avg_hum:.2f}"])
            print(f"Data written to CSV file: {file_path}")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

def main():
    """Main function to run the sensor reading loop."""
    sensor, name = initialize_sensor(pin)
    try:
        while True:
            current_time, temp_measurements, hum_measurements = burst_read(sensor, read_burst_num, read_delay)
            print_measurements(current_time, temp_measurements, hum_measurements, name)
            
            if temp_measurements and hum_measurements:
                avg_temp = sum(temp_measurements) / len(temp_measurements)
                avg_hum = sum(hum_measurements) / len(hum_measurements)
                print(f"Dumping data to CSV: avg_temp={avg_temp}, avg_hum={avg_hum}")
                dump_to_csv(os.path.expanduser("/home/hal1000/sensor_data"), current_time, avg_temp, avg_hum, name)
            time.sleep(time_interval)
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        sensor.exit()
        print("Sensor de-initialized.")

if __name__ == "__main__":
    main()
