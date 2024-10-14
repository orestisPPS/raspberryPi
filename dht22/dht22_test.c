#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define MAXTIMINGS 85
#define DHTPIN 7

int dht22_dat[5] = {0, 0, 0, 0, 0};

void read_dht22_dat()
{
    uint8_t laststate = HIGH;
    uint8_t counter = 0;
    uint8_t j = 0, i;
    float f;

    dht22_dat[0] = dht22_dat[1] = dht22_dat[2] = dht22_dat[3] = dht22_dat[4] = 0;

    pinMode(DHTPIN, OUTPUT);
    digitalWrite(DHTPIN, LOW);
    delay(18);
    digitalWrite(DHTPIN, HIGH);
    delayMicroseconds(40);
    pinMode(DHTPIN, INPUT);

    for (i = 0; i < MAXTIMINGS; i++)
    {
        counter = 0;
        while (digitalRead(DHTPIN) == laststate)
        {
            counter++;
            delayMicroseconds(1);
            if (counter == 255)
            {
                break;
            }
        }
        laststate = digitalRead(DHTPIN);

        if (counter == 255)
            break;

        if ((i >= 4) && (i % 2 == 0))
        {
            dht22_dat[j / 8] <<= 1;
            if (counter > 16)
                dht22_dat[j / 8] |= 1;
            j++;
        }
    }

    if ((j >= 40) &&
        (dht22_dat[4] == ((dht22_dat[0] + dht22_dat[1] + dht22_dat[2] + dht22_dat[3]) & 0xFF)))
    {
        float h = (dht22_dat[0] << 8 | dht22_dat[1]) / 10.0;
        float c = (dht22_dat[2] << 8 | dht22_dat[3]) / 10.0;
        if (c > 125) // Check if temperature is negative
        {
            c = -(c - 256);
        }
        f = c * 9. / 5. + 32;
        printf("Humidity = %.1f %% Temperature = %.1f C (%.1f F)\n", h, c, f);
    }
    else
    {
        printf("Data not good, skip\n");
    }
}

int main(void)
{
    printf("Raspberry Pi wiringPi DHT22 Temperature test program\n");

    if (wiringPiSetup() == -1)
        exit(1);

    while (1)
    {
        read_dht22_dat();
        delay(2000); // DHT22 requires a longer delay between readings
    }

    return (0);
}