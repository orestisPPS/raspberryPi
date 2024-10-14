#include "LedController.h"
#include <iostream>
#include <chrono>
#include <thread>
#include <stdexcept>


LEDController::LEDController(unsigned pin, const std::string& chip_name)
    : _pin(pin), _chip_name(chip_name), _chip(nullptr), _line(nullptr) {
        if (!_init()) std::cerr << "Failed to initialize LED controller" << std::endl;  
}

LEDController::~LEDController() {
    _cleanup();
}

void LEDController::blink(unsigned interval_ms, unsigned cycles) {
    while (cycles > 0) {
        _setLEDState(true);  // Turn on the LED
        std::this_thread::sleep_for(std::chrono::milliseconds(interval_ms));
        _setLEDState(false); // Turn off the LED
        std::this_thread::sleep_for(std::chrono::milliseconds(interval_ms));
        --cycles;
    }
}

void LEDController::on() { _setLEDState(true); }


// Turn the LED off
void LEDController::off() { _setLEDState(false); }



bool LEDController::_init() {
    _chip = gpiod_chip_open(_chip_name.c_str());
    if (!_chip) {
        std::cerr << "Failed to open GPIO chip: " << _chip_name << std::endl;
        return false;
    }

    _line = gpiod_chip_get_line(_chip, _pin);
    if (!_line) {
        std::cerr << "Failed to get line for GPIO pin " << _pin << std::endl;
        gpiod_chip_close(_chip);
        return false;
    }

    if (gpiod_line_request_output(_line, "LED", 0) < 0) {
        std::cerr << "Failed to request GPIO line as output" << std::endl;
        gpiod_chip_close(_chip);
        return false;
    }

    return true;
}

void LEDController::_setLEDState(bool on) {
    if (_line) {
        gpiod_line_set_value(_line, on ? 1 : 0);
    }
}

void LEDController::_cleanup() {
    if (_line) {
        gpiod_line_release(_line);
    }
    if (_chip) {
        gpiod_chip_close(_chip);
    }
}

