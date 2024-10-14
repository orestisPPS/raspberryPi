// main.cpp
#include <iostream>
#include "LedController.h"
#include <chrono>
#include <thread>

int main(int argc, char* argv[]) {
    if (argc < 2) throw std::invalid_argument("Error: No command provided.");
    std::string command = argv[1];

    unsigned pin = 16;
    LEDController led(pin);

    // Handle the "on" command
    if (command == "on")
        led.on();
    else if (command == "off")
        led.off();
    else if (command == "blink"){
        if (argc < 4) throw std::invalid_argument("Error: Blink command requires interval and cycle parameters.");
        
        unsigned interval_ms = std::atoi(argv[2]);  // Convert interval argument to unsigned int
        unsigned cycles = std::atoi(argv[3]);       // Convert cycles argument to unsigned int
        led.blink(interval_ms, cycles);
    }
    // Handle invalid commands
    else throw std::invalid_argument("Error: Invalid command.");

    return 0;
}